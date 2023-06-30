from pyray import *
from raylib import MOUSE_BUTTON_LEFT

class Menu:
    window_width, window_height = 0, 0
    logo, logo_x, logo_y = None, 0, 0
    
    in_menu = True

    game_rect, exit_rect = None, None
    background_color = Color(185, 236, 230, 255)
    button_color = Color(227, 1, 11, 255)

    def __init__(self, window_width: int, window_height: int, logo_path: str):
        self.window_width = window_width
        self.window_height = window_height

        self.logo = load_texture(logo_path)
        self.logo_x = int(self.window_width / 2 - self.logo.width / 2)
        self.logo_y = int(self.window_height / 2 - self.logo.height * 1.2)

        self.game_rect = Rectangle(int(window_width / 2 - 175), int(self.logo_y + self.logo.height * 1.2), 350, 80)
        
        self.exit_rect = Rectangle(int(window_width / 2 - 175), int(self.game_rect.y + self.game_rect.height + 40), 350, 80)

    def __del__(self):
        unload_texture(self.logo)
    
    def check_input(self): # 1 - game ; -1 - exit game
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self.game_rect):
            return 1
        
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self.exit_rect):
            return -1

        return 0        

    def show(self):
        clear_background(self.background_color)

        # Logo
        draw_texture(self.logo, self.logo_x, self.logo_y, WHITE)

        # Game button
        draw_rectangle_rec(self.game_rect, self.button_color)
        draw_rectangle_lines_ex(self.game_rect, 2, BLACK)
        text_size = measure_text("PLAY", 20)
        draw_text("PLAY", int(self.game_rect.x + self.game_rect.width / 2 - text_size / 2), int(self.game_rect.y + self.game_rect.height / 2 - 10),
        20, WHITE)

        # Exit button
        draw_rectangle_rec(self.exit_rect, self.button_color)
        draw_rectangle_lines_ex(self.exit_rect, 2, BLACK)
        text_size = measure_text("EXIT", 20)
        draw_text("EXIT", int(self.exit_rect.x + self.exit_rect.width / 2 - text_size / 2), int(self.exit_rect.y + self.exit_rect.height / 2 - 10),
        20, WHITE)
