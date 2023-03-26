import arcade
import math

class Hex():
    def __init__(self, type: str):
        self.type = type
        self.sprite: arcade.Sprite = None

        match self.type:
            case "grass":
                self.sprite = arcade.Sprite("assets/grass.png")
            case "stone":
                self.sprite = arcade.Sprite("assets/stone.png")
            case _:
                raise ValueError("Type is not valid.")
    
    def position_sprite(self, coords: tuple[int, int, int]):
        size = self.sprite.height / 2
        self.sprite.center_x = size * (math.sqrt(3) * coords[0] + math.sqrt(3) / 2 * coords[1])
        self.sprite.center_y = size * (1.5 * coords[1])