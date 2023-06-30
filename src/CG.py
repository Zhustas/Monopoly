from pyllist import sllist
from pyray import *
from raylib import KEY_KP_2, KEY_KP_3, MOUSE_BUTTON_LEFT, KEY_BACKSPACE
from functions import get_fields, add_field, delete_field, find_error
from DB import DropBox

class CreatingGame:
    window_width, window_height = 0, 0

    menu_logo, menu_logo_x, menu_logo_y = None, 0, 0
    exit_logo, exit_logo_x, exit_logo_y = None, 0, 0

    in_creating = False

    background_color = Color(217, 176, 131, 255)
    panel_rect, r_panel_rect = None, None
    
    # How many players will play the game
    players_rect, players_text, use_black = None, "", False

    # How many points needed to win the game
    points_rect, points_text, use_black_2 = None, "", False
    whole_number = 0

    # Load fields from the file
    file_rect, file_text, use_black_3 = None, "", False
    file_button = None

    # Move text fields, buttons by 25 pixels (y = y + 25)
    move_by = 25

    # Add fields by hand
    title_rect, desc_rect, pts_rect, use_black_4 = None, None, None, False
    title, desc, pts_text = "", "", ""
    points = 0

    add_button = None
    index_rect, index_text, use_black_5 = None, "", False
    index = 0

    # Delete field by index or name
    delete_rect, delete_text = None, ""
    delete_button = None
    delete_index_button = None

    # Delete all fields
    delete_all_rect = None

    # Play
    play_button = None

    def __init__(self, window_width: int, window_height: int, menu_logo_path: str, exit_logo_path: str):
        self.window_width = window_width
        self.window_height = window_height

        self.menu_logo = load_texture(menu_logo_path)
        self.menu_logo_x = window_width - self.menu_logo.width * 2
        self.menu_logo_y = 0
        
        self.exit_logo = load_texture(exit_logo_path)
        self.exit_logo_x = window_width - self.exit_logo.width
        self.exit_logo_y = 0

        self.panel_rect = Rectangle(int(window_width - window_width / 5), 0, int(window_width / 5), window_height)
        self.r_panel_rect = Rectangle(int(window_width - window_width / 2.5), 0, int(window_width / 5), window_height)

        self.TS = sllist()

    def __del__(self):
        unload_texture(self.menu_logo)
        unload_texture(self.exit_logo)

    def get_information(self):
        return [self.TS, self.players_text, self.whole_number]

    def check_input(self):
        # How many players will play the game
        if check_collision_point_rec(get_mouse_position(), self.players_rect):
            self.use_black = True
        else:
            self.use_black = False

        if self.use_black:
            if len(self.players_text) == 0:
                if is_key_pressed(KEY_KP_2):
                    self.players_text = "2"
                elif is_key_pressed(KEY_KP_3):
                    self.players_text = "3"
            if len(self.players_text) == 1 and is_key_pressed(KEY_BACKSPACE):
                self.players_text = ""

        # How many points needed to win the game
        if check_collision_point_rec(get_mouse_position(), self.points_rect):
            self.use_black_2 = True
        else:
            self.use_black_2 = False
        
        if self.use_black_2:
            number = get_char_pressed()
            if (number >= 48 and number <= 57) and len(self.points_text) < 9:
                self.whole_number = self.whole_number * 10 + (number - 48)
                self.points_text = str(self.whole_number)
            
            if len(self.points_text) != 0 and is_key_pressed(KEY_BACKSPACE):
                self.whole_number = int(self.whole_number / 10)
                self.points_text = self.points_text[:len(self.points_text) - 1]

        # Load fields from the file
        output = self.file_rect.check_input()
        if output == 1:
            self.file_button.y += self.move_by
        elif output == -1:
            self.file_button.y -= self.move_by

        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self.file_button):
            self.file_text = self.file_rect.get_text()
            temp_TS = get_fields(self.file_text)
            if find_error(temp_TS, "file") == 1:
                i = 0
                while temp_TS.nodeat(i).next != None:
                    node = temp_TS.nodeat(i).value
                    self.TS = add_field(self.TS, node.title, node.desc, node.points, self.TS.size)
                    i += 1
                node = temp_TS.nodeat(i).value
                self.TS = add_field(self.TS, node.title, node.desc, node.points, self.TS.size)

                if self.TS.size > 12:
                    while self.TS.size != 12:
                        self.TS.popleft()

                self.file_rect.delete_text()
        
        # Add fields by hand
        output = self.title_rect.check_input()
        output2 = self.desc_rect.check_input()
        if output == 1:
            self.desc_rect.rect.y += self.move_by
        elif output == -1:
            self.desc_rect.rect.y -= self.move_by

        if output == 1 or output2 == 1:
            self.pts_rect.y += self.move_by
            self.add_button.y += self.move_by
            self.index_rect.y += self.move_by
        elif output == -1 or output2 == -1:
            self.pts_rect.y -= self.move_by
            self.add_button.y -= self.move_by
            self.index_rect.y -= self.move_by

        if check_collision_point_rec(get_mouse_position(), self.pts_rect):
            self.use_black_4 = True
        else:
            self.use_black_4 = False
        
        if self.use_black_4:
            number = get_char_pressed()
            if (number >= 48 and number <= 57) and len(self.pts_text) < 9:
                self.points = self.points * 10 + (number - 48)
                self.pts_text = str(self.points)
            
            if len(self.pts_text) != 0 and is_key_pressed(KEY_BACKSPACE):
                self.points = int(self.points / 10)
                self.pts_text = self.pts_text[:len(self.pts_text) - 1]
        
        if check_collision_point_rec(get_mouse_position(), self.index_rect):
            self.use_black_5 = True
        else:
            self.use_black_5 = False

        if self.use_black_5:
            number = get_char_pressed()
            if (number >= 48 and number <= 57) and len(self.index_text) < 2:
                self.index = self.index * 10 + (number - 48)
                self.index_text = str(self.index)
            
            if len(self.index_text) != 0 and is_key_pressed(KEY_BACKSPACE):
                self.index_text = self.index_text[:len(self.index_text) - 1]
                self.index = int(self.index / 10)

        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self.add_button):
            self.title = self.title_rect.get_text()
            self.desc = self.desc_rect.get_text()
            
            if find_error(self.TS, what="add", title=self.title, description=self.desc, points=self.points, index=self.index) == 1:
                self.TS = add_field(self.TS, self.title, self.desc, self.points, self.index)
                if self.index == 12:
                    self.TS.popleft()
                elif self.TS.size > 12:
                    self.TS.popright()
                self.title_rect.delete_text()
                self.desc_rect.delete_text()
                self.points = 0
                self.pts_text = ""
                self.index = 0
                self.index_text = ""

        # Delete field by index or name
        output3 = self.delete_rect.check_input()
        if output == 1 or output2 == 1:
            self.delete_rect.rect.y += self.move_by
            self.delete_button.y += self.move_by
            self.delete_index_button.y += self.move_by
        elif output == -1 or output2 == -1:
            self.delete_rect.rect.y -= self.move_by
            self.delete_button.y -= self.move_by
            self.delete_index_button.y -= self.move_by
        if output3 == 1:
            self.delete_button.y += self.move_by
            self.delete_index_button.y += self.move_by
        elif output3 == -1:
            self.delete_button.y -= self.move_by
            self.delete_index_button.y -= self.move_by

        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self.delete_button):
            self.delete_text = self.delete_rect.get_text()
            if find_error(self.TS, "delete", what_to_delete=self.delete_text,listas_good=self.TS.size) == 1:
                self.TS = delete_field(self.TS, self.delete_text)
                self.delete_rect.delete_text()

        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self.delete_index_button):
            self.delete_text = self.delete_rect.get_text()
            if find_error(self.TS, "delete", what_to_delete=self.delete_text, del_index=True, listas_good=self.TS.size) == 1:
                self.TS = delete_field(self.TS, self.delete_text, index=True)
                self.delete_rect.delete_text()

        # Delete all fields
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self.delete_all_rect):
            if find_error(self.TS, "delete all", listas_good=self.TS.size) == 1:
                while self.TS.size != 0:
                    self.TS.popleft()

        # Menu and exit buttons
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), (self.exit_logo_x, self.exit_logo_y,
        self.exit_logo.width, self.exit_logo.height)):
            return -1
        
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), (self.menu_logo_x, self.menu_logo_y,
        self.menu_logo.width, self.menu_logo.height)):
            return 1

        # Game button
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self.play_button):
            if find_error(self.TS, "game", listas_good=self.TS.size, how_many=self.players_text, points_to_win=self.points_text) == 1:
                return 10

        return 0

    def init(self):
        # How many players will play the game
        self.players_rect = Rectangle(self.panel_rect.x + 20, 100, self.panel_rect.width - 40, 40)

        # How many points needed to win the game
        self.points_rect = Rectangle(self.panel_rect.x + 20, 180, self.panel_rect.width - 40, 40)

        # Load fields from the file
        self.file_rect = DropBox(self.panel_rect.x + 20, 300, self.panel_rect.width - 40, 42)
        self.file_button = Rectangle(self.panel_rect.x + self.panel_rect.width - 85, self.file_rect.rect.y + self.file_rect.rect.height + 20,
        65, 30)

        # Add fields by hand
        self.title_rect = DropBox(self.r_panel_rect.x + 20, 100, self.r_panel_rect.width - 40, 42)
        self.desc_rect = DropBox(self.r_panel_rect.x + 20, 180, self.r_panel_rect.width - 40, 42)
        self.pts_rect = Rectangle(self.r_panel_rect.x + 20, 300, self.r_panel_rect.width - 40, 40)
        self.add_button = Rectangle(self.r_panel_rect.x + self.r_panel_rect.width - 80, self.pts_rect.y + 50, 60, 30)
        self.index_rect = Rectangle(self.r_panel_rect.x + 90, self.pts_rect.y + 50, 70, 30)

        # Delete field by index or name
        self.delete_rect = DropBox(self.r_panel_rect.x + 20, 450, self.r_panel_rect.width - 40, 42)
        self.delete_button = Rectangle(self.r_panel_rect.x + self.r_panel_rect.width - 100, self.delete_rect.rect.y +
        self.delete_rect.rect.height + 20, 80, 30)
        self.delete_index_button = Rectangle(self.r_panel_rect.x + self.r_panel_rect.width - 185, self.delete_rect.rect.y +
        self.delete_rect.rect.height + 20, 80, 30)

        # Delete all fields
        self.delete_all_rect = Rectangle(self.r_panel_rect.x + self.r_panel_rect.width - 120, 30, 100, 30)

        # Play
        self.play_button = Rectangle(self.window_width - 150, self.window_height - 60, 140, 50)

    def show(self):
        clear_background(self.background_color)

        # Show fields preview
        if self.TS.size != 0:
            node = self.TS.first
            i = 0
            while node != None:
                node.value.show_preview(i, self.TS.size)
                node = node.next
                i += 1

        # Panels
        draw_rectangle_rec(self.panel_rect, Color(246, 243, 236, 255))
        draw_rectangle_rec(self.r_panel_rect, Color(247, 235, 202, 255))
        draw_line_ex((int(self.r_panel_rect.x), 0), (int(self.r_panel_rect.x), int(self.window_height)), 2, BLACK)
        draw_line_ex((int(self.panel_rect.x), 0), (int(self.panel_rect.x), int(self.window_height)), 2, BLACK)

        # Menu and exit buttons
        draw_texture(self.menu_logo, self.menu_logo_x, self.menu_logo_y, WHITE)
        draw_texture(self.exit_logo, self.exit_logo_x, self.exit_logo_y, WHITE)

        # Preview
        draw_text("PREVIEW", 10, 10, 30, BLACK)

        # How many players will play the game
        draw_rectangle_rec(self.players_rect, WHITE)
        draw_text("PLAYERS (2 - 3)", int(self.players_rect.x + 35), int(self.players_rect.y - 20), 20, BLACK)
        if self.use_black:
            draw_rectangle_lines_ex(self.players_rect, 2, BLACK)
        else:
            draw_rectangle_lines_ex(self.players_rect, 2, GRAY)
        draw_text(self.players_text, int(self.players_rect.x + 10), int(self.players_rect.y + self.players_rect.height / 2 - 8), 20, BLACK)

        # How many points needed to win the game
        draw_rectangle_rec(self.points_rect, WHITE)
        draw_text("POINTS TO WIN", int(self.points_rect.x + 35), int(self.points_rect.y - 20), 20, BLACK)
        if self.use_black_2:
            draw_rectangle_lines_ex(self.points_rect, 2, BLACK)
        else:
            draw_rectangle_lines_ex(self.points_rect, 2, GRAY)
        draw_text(self.points_text, int(self.points_rect.x + 10), int(self.points_rect.y + self.points_rect.height / 2 - 8), 20, BLACK)

        # Load fields from the file
        draw_text("FILE NAME", int(self.file_rect.rect.x + 60), int(self.file_rect.rect.y - 20), 20, BLACK)
        self.file_rect.show()
        draw_rectangle_rec(self.file_button, Color(249, 233, 208, 100))
        draw_rectangle_lines_ex(self.file_button, 2, BLACK)
        draw_text("LOAD", int(self.file_button.x + 6), int(self.file_button.y + 6), 20, BLACK)
        
        # Add fields by hand
        draw_text("TITLE", int(self.title_rect.rect.x + 85), int(self.title_rect.rect.y - 20), 20, BLACK)
        self.title_rect.show()

        draw_text("DESCRIPTION", int(self.desc_rect.rect.x + 50), int(self.desc_rect.rect.y - 20), 20, BLACK)
        self.desc_rect.show()

        draw_rectangle_rec(self.pts_rect, WHITE)
        draw_text("POINTS", int(self.pts_rect.x + 80), int(self.pts_rect.y - 20), 20, BLACK)
        if self.use_black_4:
            draw_rectangle_lines_ex(self.pts_rect, 2, BLACK)
        else:
            draw_rectangle_lines_ex(self.pts_rect, 2, GRAY)
        draw_text(self.pts_text, int(self.pts_rect.x + 10), int(self.pts_rect.y + self.pts_rect.height / 2 - 8), 20, BLACK)

        draw_rectangle_rec(self.add_button, Color(249, 233, 208, 100))
        draw_rectangle_lines_ex(self.add_button, 2, BLACK)
        draw_text("ADD", int(self.add_button.x + 10), int(self.add_button.y + 6), 20, BLACK)

        draw_rectangle_rec(self.index_rect, WHITE)
        if self.use_black_5:
            draw_rectangle_lines_ex(self.index_rect, 2, BLACK)
        else:
            draw_rectangle_lines_ex(self.index_rect, 2, GRAY)
        draw_text(self.index_text, int(self.index_rect.x + 10), int(self.index_rect.y + self.index_rect.height / 2 - 8), 20, BLACK)
        draw_text("INDEX", int(self.r_panel_rect.x + 20), int(self.add_button.y + 6), 20, BLACK)

        # Delete field by index or name
        draw_text("DEL (INDEX OR NAME)", int(self.delete_rect.rect.x + 6), int(self.delete_rect.rect.y - 20), 20, BLACK)
        self.delete_rect.show()

        draw_rectangle_rec(self.delete_button, Color(249, 233, 208, 100))
        draw_rectangle_lines_ex(self.delete_button, 2, BLACK)
        draw_text("DEL N", int(self.delete_button.x + 10), int(self.delete_button.y + 6), 20, BLACK)

        draw_rectangle_rec(self.delete_index_button, Color(249, 233, 208, 100))
        draw_rectangle_lines_ex(self.delete_index_button, 2, BLACK)
        draw_text("DEL I", int(self.delete_index_button.x + 12), int(self.delete_index_button.y + 6), 20, BLACK)

        # Delete all fields
        draw_rectangle_rec(self.delete_all_rect, Color(249, 233, 208, 100))
        draw_rectangle_lines_ex(self.delete_all_rect, 2, BLACK)
        draw_text("DEL ALL", int(self.delete_all_rect.x + 9), int(self.delete_all_rect.y + 6), 20, BLACK)

        # Play
        draw_rectangle_rec(self.play_button, Color(205, 230, 208, 100))
        draw_rectangle_lines_ex(self.play_button, 2, BLACK)
        draw_text("PLAY", int(self.play_button.x + 45), int(self.play_button.y + 17), 20, BLACK)
