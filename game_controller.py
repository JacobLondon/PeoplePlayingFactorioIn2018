import pygame, numpy as np, time, threading, copy
from sprite import Player, Missile
from client import Client
from gamestate import State, json2obj
from enum import Enum

class Dir(Enum):
    RIGHT = 0
    LEFT = 1

class Controller(object):

    """
    @param square: size of each tile in pixels
    @param size: number of squares wide the screen is
    """
    def __init__(self, square, size, p1, p2, client_num, cooldown):

        self.square = square
        self.size = square * size
        self.BLACK = (0,0,0)

        # pygame tools
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption('PPFI18')
        pygame.display.update()

        self.clock = pygame.time.Clock()
        self.refresh_rate = 60
        self.tick_rate = 20
        self.ticking = True
        self.done = False
        #self.drawing_missiles = False

        self.client_num = client_num
        self.client = Client(client_num)

        # load players
        self.p1 = p1
        self.p2 = p2
        # the player changes depending on client or server
        self.player = self.p1 if self.client_num == 0 else self.p2

        self.missiles = []
        # hold the missiles until tick, then empty the buffer
        self.missile_buffer = []
        # object which stores the data for the state
        self.gamestate = State(self.p1, self.p2, self.missiles, self.client_num)
        # control the speed of the player shooting
        self.cooldown = cooldown
        self.fire_ready = True

    def draw_tile(self, x, y, color):

        # [left, top, width, height]
        pygame.draw.rect(self.display, color, \
            [self.square * x, self.square * y, self.square, self.square])

    def draw_sprite(self, sprite):

        self.draw_tile(sprite.loc[0], sprite.loc[1], sprite.color)

    def draw_missiles(self):

        #while not self.drawing_missiles:
        #    pass

        # only update missiles which were not still being received
        temp_missiles = self.missiles[0:-1]

        # update each missile
        for m in temp_missiles:

            # remove the previous missile square
            self.draw_tile(m.loc[0], m.loc[1], self.BLACK)

            # update to next pos
            temp = list(m.loc)
            temp[1] = temp[1] + m.dir
            m.loc = tuple(temp)

            # remove if it went off the screen
            if m.loc[1] < 0 or m.loc[1] > self.size:
                self.missiles.remove(m)
                continue

            self.draw_sprite(m)

        #self.drawing_missiles = False

    def move(self, direction, player):

        # move left and bounds check
        if direction == Dir.LEFT:
            if 0 <= player.loc[0] - 1:
                self.draw_tile(player.loc[0], player.loc[1], self.BLACK)
                player.loc = (player.loc[0] - 1, player.loc[1])

        # move right and bounds check
        elif direction == Dir.RIGHT:
            if player.loc[0] + 1 < self.size / self.square:
                self.draw_tile(player.loc[0], player.loc[1], self.BLACK)
                self.player.loc = (player.loc[0] + 1, player.loc[1])

    def reload(self):
        time.sleep(self.cooldown)
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
            t = threading.Thread(target=self.reload, args=())
            t.start()

    def tick(self):
        while self.ticking:

            # interface with network every tick
            s_thread = threading.Thread(target=self.send, args=())
            s_thread.start()
            r_thread = threading.Thread(target=self.receive, args=())
            r_thread.start()
            time.sleep(1 / self.tick_rate)

    def send(self):

        # send gamestate as a json
        self.client.send(self.gamestate.get_json())

        # empty the buffer because it will have been sent
        self.missile_buffer = []

    def receive(self):

        received_data = self.client.receive()
        print(received_data)

        # convert json to object
        received_state = json2obj(received_data)

        #while self.drawing_missiles:
        #    pass

        # load the new missiles
        for m in received_state.missile_buffer:

            # player cannot receive their own missiles
            if self.player.number != received_state.number:
                self.missiles.append(m)

        #self.drawing_missiles = True

        # set pos of the other player
        if self.player.number == 0:
            self.p2.loc = received_state.p2_loc
        else:
            self.p1.loc = received_state.p1_loc

    def update(self):

        # update players
        t = threading.Thread(target=self.draw_missiles, args=())
        t.start()
        self.draw_sprite(self.p1)
        self.draw_sprite(self.p2)

        # set gamestate
        self.gamestate.set_state(self.p1, self.p2, self.missile_buffer)

        #print(threading.active_count())

        pygame.display.update()
        self.clock.tick(self.refresh_rate)

    def run(self):

        tick_thread = threading.Thread(target=self.tick, args=())
        tick_thread.start()

        # program loop
        while not self.done:

            # traverse all events occurring that frame
            for event in pygame.event.get():
                t = threading.Thread(target=self.handle_event, args=(event,))
                t.start()
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
        if pygame.key.get_pressed()[pygame.K_LEFT] != 0:
            self.move(Dir.LEFT, self.player)

        #  player moves right
        elif pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
            self.move(Dir.RIGHT, self.player)

        # player shoots up
        elif pygame.key.get_pressed()[pygame.K_UP] != 0:
            self.shoot(-1)

        # player shoots down
        elif pygame.key.get_pressed()[pygame.K_DOWN] != 0:
            self.shoot(1)
