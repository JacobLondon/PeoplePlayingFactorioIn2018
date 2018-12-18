import pygame, time, copy

from thread import Thread
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

        # the player id changes depending on client
        self.player = self.p1 if self.client.id == 0 else self.p2

        # hold the missiles until tick, then empty the buffer
        self.missiles = []
        self.missile_buffer = []

        # object which stores the data for the state
        self.gamestate = State(self.p1, self.p2, self.missiles, self.client.id)
        self.fire_ready = True
        self.move_ready = True

        self.key_presses = {pygame.K_LEFT:False, pygame.K_RIGHT:False, pygame.K_UP:False, pygame.K_DOWN:False}

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

    def shoot_cooldown(self):
        time.sleep(settings.shoot_cooldown)
        self.fire_ready = True

    def move_cooldown(self):
        time.sleep(settings.move_cooldown)
        self.move_ready = True

    def move(self, direction, player):

        if not self.move_ready:
            return

        # move left and bounds check
        if direction == Dir.left:
            if 0 <= player.loc[0] - 1:
                player.loc = (player.loc[0] - 1, player.loc[1])

        # move right and bounds check
        elif direction == Dir.right:
            if player.loc[0] + 1 < settings.grid_size:
                self.player.loc = (player.loc[0] + 1, player.loc[1])

        self.move_ready = False
        Thread(target=self.move_cooldown, args=()).start()

    def shoot(self, dir):

        # make a missile player and put it in the missile list
        if self.fire_ready:
            missile = Missile(dir=dir)
            missile.loc = (self.player.loc[0], self.player.loc[1] + missile.dir)
            self.missiles.append(missile)
            self.missile_buffer.append(copy.deepcopy(missile))

            # cannot fire again until the cooldown timer is done
            self.fire_ready = False
            Thread(target=self.shoot_cooldown, args=()).start()

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
        if self.client.id != received_state.id:

            # load the new missiles
            for m in received_state.missile_buffer:
                self.missiles.append(m)

        # set pos of the other player
        if self.client.id == 0:
            self.p2 = received_state.p2
        else:
            self.p1 = received_state.p1

    def update(self):

        # clear screen before drawing
        self.interface.clear()

        # update and draw sprites
        self.draw_missiles()
        self.interface.draw_sprite(self.p1)
        self.interface.draw_sprite(self.p2)

        # set gamestate
        self.gamestate.set_state(self.p1, self.p2, self.missile_buffer)

        # pygame update
        self.interface.update()

    def run(self):

        tick_thread = Thread(target=self.tick, args=())
        tick_thread.start()

        # program loop
        while not self.done:

            # traverse all events occurring that frame
            for event in pygame.event.get():
                self.handle_event(event)

            # update presses and tick
            self.key_actions()
            self.update()

        self.ticking = False
        tick_thread.join()
        self.client.close()
        pygame.quit()

    def handle_event(self, event):

        # top right corner X
        if event.type == pygame.QUIT:
            self.done = True

        # player starts doing actions
        elif event.type == pygame.KEYDOWN:
            self.key_presses[event.key] = True

        # player stops doing actions
        elif event.type == pygame.KEYUP:
            self.key_presses[event.key] = False

    # do actions based on what was pressed
    def key_actions(self):
        if self.key_presses[pygame.K_LEFT]:
            self.move(Dir.left, self.player)

        if self.key_presses[pygame.K_RIGHT]:
            self.move(Dir.right, self.player)

        if self.key_presses[pygame.K_UP]:
            self.shoot(Dir.up)

        if self.key_presses[pygame.K_DOWN]:
            self.shoot(Dir.down)
