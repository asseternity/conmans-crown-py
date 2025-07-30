# v modularize - put Combatant, Duel, StoryLine and DialogueOption in their own modules
# v import them here, and make a GameState class, which will: the current story or duel, player object, and list of story variable strings
# v GameState will make it WAY easier to save too
# v Modularize GameState itself

from modules.combatant import Combatant
from modules.duel import Duel
from modules.storyline import StoryLine
from modules.dialogueoption import DialogueOption
from modules.gamestate import GameState
from modules.load_json import load_game_from_json

# Make a class, element, which can be either a StoryLine or a Duel
# Modularize it
    
# Then create an Engine class, the goal of which it to uncouple game logic from GameGUI:
# - just callback any logs or logger
# - combine all "battle round" logic into one step that can be called
# - make methods to change storyLine to duel and vise verse in GameState
# - use gamestate for everything

class Engine:
    def __init__ (self, gs: GameState, logging_function: callable):
        self.gs = gs
        self.logging_function = logging_function

    #  a "round" method that will run that callback on all the returned strings from Duel's helper functions 
    def duel_round(self, player_action):
        if isinstance(self.gs.current_element, Duel):
            # 1) parameter the player's action
            p = player_action

            # 2) get enemy's action
            e = self.gs.current_element.choose_enemy_action()
            
            # 3) run and log a round using both actions
            self.logging_function(self.gs.current_element.damage_phase(self.gs.player_object, p, e))
            
            # 4) log callback: f"You spent {p}, enemy spent {e}.\n{res}"
            self.logging_function(f"You spent {p}, enemy spent {e}.")
                      
            # 5) check if player or enemy is dead, call next_element if so
            if not self.gs.player_object.is_alive():
                # [_] need to raise an event or something for the UI to update
                return

            elif not self.gs.current_element.enemy.is_alive():
                # [_] need to raise an event or something for the UI to update
                return
            
            # 6) log callback: current_duel.tactic_hint(current_duel.enemy
            self.logging_function(self.gs.current_element.tactic_hint(self.gs.current_element.enemy))
            
            # 7) run restore after on gs.current_element
            self.gs.current_element.restore_after(self.gs.player_object, p, e)
        else:
            return

    # "Next element" on the GameState - check win or loss the duel, check what type the next element is, etc.
    def progress_element(self, wonDuel=False):
        # [_] this will be called to START the next thing
        if isinstance(self.gs.current_element, Duel):
            if wonDuel:
                return
            else:
                return
        else:
            return
        
    def choose_option(self, next_id):
        # [_] implement this
        return
        
# RUNNING THE GAME
# 1) Load the JSON
player, first_element = load_game_from_json("story.json")

# 2) Wrap in a GameState
gs = GameState(current_element=first_element, player_object=player)

# 3) Instantiate the Engine with whatever UI’s logging callback you have
# engine = Engine(gs, logging_function=whatever)

# 4) Now hand off `engine` to the UI framework