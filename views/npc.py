import arcade
from modules.storyline import StoryLine

class NPC(arcade.Sprite):
    def __init__ (self, image_path, center_x, center_y, storyline: StoryLine):
        super().__init__(image_path)
        self.center_x = center_x
        self.center_y = center_y
        self.storyline = storyline