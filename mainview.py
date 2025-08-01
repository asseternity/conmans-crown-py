import arcade
import arcade.gui
from views.startup import StartupView

# Constants
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
WINDOW_TITLE = "The Conman's Crown"
PLAYER_MOVEMENT_SPEED = 5

class MainView(arcade.View):
    def __init__(self):
        # Call the parent class
        super().__init__()

        # Init GUI manager
        self.manager = arcade.gui.UIManager()

        # Create an anchor-layout *for each* panel
        self.dialogue_panel = arcade.gui.UIAnchorLayout()
        self.dialogue_box = arcade.gui.UIBoxLayout(vertical=True, align="center", space_between=20)
        self.dialogue_label = arcade.gui.UILabel(text="Hello, traveler. What brings you here?", font_size=18, width=400, align="center")
        self.dialogue_box.add(self.dialogue_label)
        self.dialogue_next = arcade.gui.UIFlatButton(
            text="Continue",
            width=100
        )   
        self.dialogue_box.add(self.dialogue_next)
        @self.dialogue_next.event("on_click")
        def advance_dialogue(event):
            self.dialogue_label.text = "Let me tell you a tale of the Conman’s Crown."
        self.dialogue_panel.add(
            child=self.dialogue_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.duel_panel = arcade.gui.UIAnchorLayout()
        self.duel_box = arcade.gui.UIBoxLayout(vertical=True, align="center", space_between=20)
        self.duel_label = arcade.gui.UILabel(text="Duel time!", font_size=18, width=400, align="center")
        self.duel_box.add(self.duel_label)
        self.duel_next = arcade.gui.UIFlatButton(
            text="Attack",
            width=100
        )   
        self.duel_box.add(self.duel_next)
        @self.duel_next.event("on_click")
        def advance_duel(event):
            self.duel_label.text = "Duel continues!"
        self.duel_panel.add(
            child=self.duel_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.dialogue_open = False
        self.duel_open     = False

        # Init objects
        self.player_sprite = None
        self.player_list = None
        self.npc_sprite = None
        self.npc_list = None
        self.background_sprite = None
        self.background_list = None
        self.camera = None

        self.engine = None  # set later by StartupView

    def setup(self):
        # Set up the game here. Call this function to restart the game.

        # create camera
        self.camera = arcade.Camera2D()

        # create sprites from file
        self.player_sprite = arcade.Sprite("assets/player_idle.png")
        self.player_sprite.center_x = 22
        self.player_sprite.center_y = 60
        
        self.npc_sprite = arcade.Sprite("assets/npc1.png")
        self.npc_sprite.center_x = 500
        self.npc_sprite.center_y = 60

        self.background_sprite = arcade.Sprite("assets/bg1.png")
        self.background_sprite.left = 0
        self.background_sprite.bottom = 0
        
        # use SpriteList - it's a lot more GPU efficient
        # put objects for which you will need collision utility separately - like Unity layers 
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.npc_list = arcade.SpriteList()
        self.npc_list.append(self.npc_sprite)
        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background_sprite)

        # Init physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False

        # Track the state of which menus are open
        self.dialogue_open = False
        self.duel_open = False

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        # Render the screen.

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()

        # Code to draw other things  
        self.camera.use()
        self.background_list.draw()
        self.player_list.draw()
        self.npc_list.draw()

        # Draw the manager.
        self.manager.draw()

    def update_player_speed(self):
        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_update(self, delta_time):
        # Movement and Game Logic
        self.physics_engine.update()
        self.camera.position = (self.player_sprite.center_x, self.player_sprite.center_y + (WINDOW_HEIGHT // 2) - 50)

    def on_key_press(self, key, modifiers):
        # movement
        if not self.dialogue_open and not self.duel_open:
            if key == arcade.key.LEFT or key == arcade.key.A:
                self.left_pressed = True
                self.update_player_speed()
            elif key == arcade.key.RIGHT or key == arcade.key.D:
                self.right_pressed = True
                self.update_player_speed()

        # reset
        if key == arcade.key.ESCAPE:
            self.setup()
        
        # duel and dialogue UI testing
        if key == arcade.key.T and not self.duel_open:
            self.toggle_dialogue_ui()
        if key == arcade.key.F and not self.dialogue_open:
            self.toggle_duel_ui()
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
            self.update_player_speed()

    def toggle_dialogue_ui(self):
        if self.dialogue_open:
            self.manager.remove(self.dialogue_panel)
            self.dialogue_open = False
        else:
            self.manager.add(self.dialogue_panel)
            self.dialogue_open = True

    def toggle_duel_ui(self):
        if self.duel_open:
            self.manager.remove(self.duel_panel)
            self.duel_open = False
        else:
            self.manager.add(self.duel_panel)
            self.duel_open = True

def main():
    # Entry point for Python. When you run a program, Python looks for a main() function and runs it.
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    main_game_view = MainView()
    start_view = StartupView(main_game_view)
    window.show_view(start_view)
    arcade.run() # run the engine

# Checks whether the script is being run directly (e.g., python arcadeUI.py) or is being imported as a module from another script.
# If run directly: filename literally changes to __ main__, so the below evaluates to True, and the block runs.
# If imported: __name__ == "arcadeUI" (i.e., the module name), and the block does not run.
if __name__ == "__main__":
    main()

# --- ARCHITECTURE ---
# GameState is the core state (current dialogue or duel, player object, flags).
# Engine owns and manipulates a GameState instance.
# MainView owns the Engine and uses it to drive the UI.
# StartupView (your main menu) can create and pass initial GameState to MainView via a loader function.

# --- ROADMAP ---
# [v] main menu
# [v] make sure the tasks in Engine are addressed, and everything is cleanly separate
# [v] create a MainView method to show dialogue and options
# [v] create a MainView method to show battle UI 
# [_] connect the Engine with the dialogue and options UI, keeping things cleanly separate
# [_] connect the Engine with the dueling UI, keeping things cleanly separate
# [_] attach storyline stubs in JSON to NPC objects
# [_] add the frame around the whole window
# [_] game UI
# [_] saving and loading
# [_] block camera from going offscreen