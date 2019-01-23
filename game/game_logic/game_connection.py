import re

from game.utils.config import settings
from game.game_logic.game_objects import MissileInfo

from game.game_logic.gamestate import json_to_obj

class GameConnection(object):

    def __init__(self, actions, controller):
        self.controller = controller
        self.actions = actions

        self.receiving = False
        self.received_state = None

    def send(self):

        # send gamestate as a json
        try:
            self.controller.client.send(self.actions.gamestate.to_json())
        # the host was forcibly closed, end the program
        except Exception as e:
            print('failed to send\n', e)
            self.controller.done = True
            return

        # empty the buffer because it will have been sent
        self.actions.missile_buffer = []

    def receive(self):

        # do not try to receive more if there is nothing to receive
        if self.receiving:
            return

        self.receiving = True
        try:
            # get the data as a string from the server
            received_data = self.controller.client.receive()
        # the host was forcibly closed, end the program
        except Exception as e:
            print('failed to receive\n', e)
            self.controller.done = True
            self.receiving = False
            return
        finally:
            self.receiving = False

        # remove a player who disconnects
        if settings.disconnect in received_data:

            # get just the id from the disconnect message
            id_to_remove = int(re.sub('\D', '', received_data))
            match = self.player_in_list(check_id=id_to_remove, in_list=self.actions.player_infos)
            
            # player was found, remove it
            if match is not False:
                #del self.actions.player_images[match.id]
                self.actions.player_infos.remove(match)

        # convert json to object if there is data
        self.received_state = json_to_obj(received_data)
        if self.received_state is None:
            return

        # data was successfully received and decoded, so load it
        self.load_gamestate()
    
    def load_gamestate(self):
        for player in self.received_state.players:
            
            # match is a PlayerInfo
            match = self.player_in_list(check_id=player.id, in_list=self.actions.player_infos)
            if match == False:
                self.actions.load_player(player)
            elif not match.id == self.actions.player.id:
                self.update_player(current=match.player, received=player)

        # update state from other clients
        if not self.actions.gamestate.id == self.received_state.id:

            # load the new missiles
            for missile in self.received_state.missile_buffer:
                self.actions.missile_infos.append(MissileInfo(missile, self.controller.interface))

    # return the list player if given player is in list, players are unique by id
    def player_in_list(self, check_id=None, in_list=None):
        if check_id is None or in_list is None:
            return

        # given player id, return player with matching id
        for match in in_list:
            if match.id == check_id:
                return match
        return False

    # update player with the received player
    def update_player(self, current=None, received=None):
        if current is None or received is None:
            return
        current.loc = received.loc
        current.vel = received.vel
        current.health = received.health