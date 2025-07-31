import arcade
import arcade.gui
from modules.load_json import load_game_from_json
from modules.gamestate import GameState
from engine import Engine 

class StartupView(arcade.View):
    def __init__ (self, main_view):
        self.main_view = main_view

        # Call the parent class
        super().__init__()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        self.window.background_color = arcade.csscolor.DARK_SLATE_BLUE

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        self.window.default_camera.use()

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("The Conman's Crown", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to start ", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        
        # Load the game
        player, starting_element = load_game_from_json("story.json")

        # Create GameState
        gs = GameState(current_element=starting_element, player_object=player)

        # Pass GameState into Engine
        engine = Engine(gs=gs, logging_function=print) # [_] print is temporary

        # Give both to MainView
        self.main_view.engine = engine
        self.main_view.setup()
        self.window.show_view(self.main_view)