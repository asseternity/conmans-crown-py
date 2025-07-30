class GameState:
    def __init__ (self, current_element, player_object):
        self.current_element = current_element
        self.player_object = player_object
        self.flags = set()