import pygame, time, copy
from threading import Thread

from sprite import Player, Missile
from client import Client
from gamestate import State, json_to_obj
from config import settings
from constants import Color, Dir
from display_interface import Interface

class Controller(object):

    def __init__(self):

        # game tools
        self.ticking = True
        self.done = False
        self.interface = Interface()
        self.client = Client()

        # load players
        self.p1 = Player.create_playerone()
        self.p2 = Player.create_playertwo()
        # the player changes depending on client or server
        self.player = self.p1 if self.client.id == 0 else self.p2

        self.missiles = []
        # hold the missiles until tick, then empty the buffer
        self.missile_buffer = []
        # object which stores the data for the state
        self.gamestate = State(self.p1.loc, self.p2.loc, self.missiles, self.client.id)
        self.fire_ready = True

    def draw_missiles(self):

        # update each missile
        for m in self.missiles:

            # update to next pos
            m.loc = (m.loc[0], m.loc[1] + m.dir)

            # remove if it went off the screen
            if m.loc[1] < 0 or m.loc[1] > settings.grid_size:
                self.missiles.remove(m)
                continue

            self.interface.draw_sprite(m)

    def move(self, direction, player):

        # move left and bounds check
        if direction == Dir.left:
            if 0 <= player.loc[0] - 1:
                player.loc = (player.loc[0] - 1, player.loc[1])

        # move right and bounds check
        elif direction == Dir.right:
            if player.loc[0] + 1 < settings.grid_size:
                self.player.loc = (player.loc[0] + 1, player.loc[1])

    def reload(self):
        time.sleep(settings.cooldown)
        self.fire_ready = True

    def shoot(self, dir):

        # make a missile player and put it in the missile list
        if self.fire_ready:
            missile = Missile(dir=dir)
            missile.loc = (self.player.loc[0], self.player.loc[1] + missile.dir)
            self.missiles.append(missile)
            self.missile_buffer.append(copy.deepcopy(missile))

            # cannot fire again until the cooldown timer is done
            self.fire_ready = False
            Thread(target=self.reload, args=()).start()

    def tick(self):
        while self.ticking:

            # interface with network every tick
            Thread(target=self.send, args=()).start()
            Thread(target=self.receive, args=()).start()
            time.sleep(1 / settings.tick_rate)

    def send(self):

        # send gamestate as a json
        try:
            self.client.send(self.gamestate.to_json())
        # the host was forcibly closed, end the program
        except:
            self.done = True
            return

        # empty the buffer because it will have been sent
        self.missile_buffer = []

    def receive(self):

        try:
            received_data = self.client.receive()
        # the host was forcibly closed, end the program
        except:
            self.done = True
            return

        # convert json to object if there is data
        received_state = json_to_obj(received_data)
        if received_state == None:
            return

        # player cannot receive their own missiles
        if self.player.number != received_state.number:

            # load the new missiles
            for m in received_state.missile_buffer:
                self.missiles.append(m)

        # set pos of the other player
        if self.player.number == 0:
            self.p2.loc = received_state.p2_loc
        else:
            self.p1.loc = received_state.p1_loc

    def update(self):

        # clear screen before drawing
        self.interface.clear()

        # update and draw sprites
        self.draw_missiles()
        self.interface.draw_sprite(self.p1)
        self.interface.draw_sprite(self.p2)

        # set gamestate
        self.gamestate.set_state(self.p1.loc, self.p2.loc, self.missile_buffer)

        # pygame update
        self.interface.update()

    def run(self):

        tick_thread = Thread(target=self.tick, args=())
        tick_thread.start()

        # program loop
        while not self.done:

            # traverse all events occurring that frame
            for event in pygame.event.get():
                Thread(target=self.handle_event, args=(event,)).start()
                break

            # update screen/tick clock
            self.update()

        self.ticking = False
        tick_thread.join()
        self.client.close()
        pygame.quit()

    def handle_event(self, event):

        # top right corner X
        if event.type == pygame.QUIT:
            self.done = True

        #  player moves left
        elif pygame.key.get_pressed()[pygame.K_LEFT] != 0:
            self.move(Dir.left, self.player)

        #  player moves right
        elif pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
            self.move(Dir.right, self.player)

        # player shoots up
        elif pygame.key.get_pressed()[pygame.K_UP] != 0:
            self.shoot(Dir.up)

        # player shoots down
        elif pygame.key.get_pressed()[pygame.K_DOWN] != 0:
            self.shoot(Dir.down)
