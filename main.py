import arcade
import sys

from view_manager import GameView
from view_manager import views

TITLE = "Map Generator"

def main():
    window: arcade.Window
    if "--windowed" in sys.argv:
        window = arcade.Window(title=TITLE, resizable=True)
        window.maximize()
    else:
        window = arcade.Window(title=TITLE, fullscreen=True, vsync=True)
    views["game_view"] = GameView()
    views["game_view"].setup()
    window.show_view(views["game_view"])
    arcade.run()

if __name__ == "__main__":
    main()