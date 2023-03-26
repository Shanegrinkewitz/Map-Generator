import arcade
import arcade.gui
from pyglet.math import Vec2

import map_generator
from hex import Hex

views: dict[str, arcade.View] = {
    "main_menu_view": None,
    "game_view": None,
    "pause_view": None
}

class MainMenuView(arcade.View):
    """ The view that represents the main menu of the game """

    def __init__(self):
        super().__init__()

        arcade.set_background_color((180, 180, 180))

        self.manager = arcade.gui.UIManager()

        self.layout = arcade.gui.UIBoxLayout()

        start_button = arcade.gui.UIFlatButton(text="Start Game", width=300)
        self.layout.add(start_button.with_space_around(bottom=30))

        options_button = arcade.gui.UIFlatButton(text="Options", width=300)
        self.layout.add(options_button.with_space_around(bottom=30))

        exit_button = arcade.gui.UIFlatButton(text="Exit to Desktop", width=300)
        self.layout.add(exit_button)

        start_button.on_click = self.on_click_start_game
        options_button.on_click = self.on_click_options
        exit_button.on_click = self.on_click_exit

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.layout))

    def on_click_start_game(self, event):
        if not views["game_view"]:
            views["game_view"] = GameView()
        views["game_view"].setup()
        self.window.show_view(views["game_view"])

    def on_click_options(self, event):
        pass

    def on_click_exit(self, event):
        arcade.exit()
    
    def on_draw(self):
        self.clear()
        self.manager.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()
    
    def on_show_view(self):
        self.manager.enable()
    
    def on_hide_view(self):
        self.manager.disable()

class GameView(arcade.View):
    """ The view that represents the running game """

    def __init__(self):
        super().__init__()

        self.width = 0
        self.height = 0
        
        self.grid: dict[tuple[int, int, int], Hex] = None
        self.hex_sprite_list: arcade.SpriteList = None

        self.up_key_down = False
        self.down_key_down = False
        self.left_key_down = False
        self.right_key_down = False

        self.camera: arcade.Camera = None

        arcade.set_background_color((0, 0, 0))

    def setup(self):
        self.width, self.height = self.window.get_size()

        self.camera = arcade.Camera(self.width, self.height)

        self.hex_sprite_list = arcade.SpriteList()

        self.grid = map_generator.generate_map(radius=10, num_lands=180)

        for item in self.grid.items():
            coords = item[0]
            hex = item[1]
            self.hex_sprite_list.append(hex.sprite)
            hex.position_sprite(coords)

        self.up_key_down = False
        self.down_key_down = False
        self.left_key_down = False
        self.right_key_down = False

    def on_draw(self):
        self.clear()

        self.camera.use()

        self.hex_sprite_list.draw()

    def on_update(self, delta_time):
        cam_speed = 10
        cam_change_x = 0
        cam_change_y = 0
        if self.up_key_down and not self.down_key_down:
            cam_change_y = 1
        elif self.down_key_down and not self.up_key_down:
            cam_change_y = -1
        if self.left_key_down and not self.right_key_down:
            cam_change_x = -1
        elif self.right_key_down and not self.left_key_down:
            cam_change_x = 1
        #self.camera.position.x += cam_change_x * cam_speed
        #self.camera.position.y += cam_change_y * cam_speed
        self.camera.goal_position = self.camera.position + Vec2(cam_change_x * cam_speed, cam_change_y * cam_speed)
        #self.camera.move(Vec2(cam_change_x * cam_speed, cam_change_y * cam_speed))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_key_down = True
        elif key == arcade.key.DOWN:
            self.down_key_down = True
        elif key == arcade.key.LEFT:
            self.left_key_down = True
        elif key == arcade.key.RIGHT:
            self.right_key_down = True
        elif key == arcade.key.P:
            if not views["pause_view"]:
                views["pause_view"] = PauseView()
            self.window.show_view(views["pause_view"])
        elif key == arcade.key.ESCAPE:
            arcade.exit()
    
    def on_key_release(self, key, _modifiers):
        if key == arcade.key.UP:
            self.up_key_down = False
        elif key == arcade.key.DOWN:
            self.down_key_down = False
        elif key == arcade.key.LEFT:
            self.left_key_down = False
        elif key == arcade.key.RIGHT:
            self.right_key_down = False

class PauseView(arcade.View):
    
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()

        self.layout = arcade.gui.UIBoxLayout()

        resume_button = arcade.gui.UIFlatButton(text="Resume", width=300)
        self.layout.add(resume_button.with_space_around(bottom=30))

        exit_button = arcade.gui.UIFlatButton(text="Exit to Main Menu", width=300)
        self.layout.add(exit_button)

        resume_button.on_click = self.on_click_resume
        exit_button.on_click = self.on_click_exit

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.layout))

    def on_click_resume(self, event):
        self.window.show_view(views["game_view"])
    
    def on_click_exit(self, event):
        self.window.show_view(views["main_menu_view"])
    
    def on_draw(self):
        self.clear()

        # Draw all sprites from the game view
        views["game_view"].hex_list.draw()

        self.manager.draw()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.window.show_view(views["game_view"])
        elif key == arcade.key.ESCAPE:
            arcade.exit()
    
    def on_show_view(self):
        self.manager.enable()
    
    def on_hide_view(self):
        self.manager.disable()