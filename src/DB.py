from pyray import *
from raylib import KEY_BACKSPACE

class DropBox:
    rect = None
    use_black = False
    text = ""
    rows = 1
    final_text = ""

    text_push_x = 10
    text_push_y = 9
    starting_height = 0
    add_to_height = 17
    add_h_to_draw = 25

    def __init__(self, x, y, w, h):
        self.texts = []
        self.rect = Rectangle(x, y, w, h)
        self.starting_height = h
    
    def get_text(self):
        self.final_text = ""
        for i in range(len(self.texts)):
            self.final_text = self.final_text + self.texts[i]
        self.final_text = self.final_text + self.text

        if self.final_text == "":
            return ""
        else:
            return self.final_text

    def delete_text(self):
        self.text = ""
        self.texts.clear()
        self.rect.height = self.starting_height

    def check_input(self):
        if check_collision_point_rec(get_mouse_position(), self.rect):
            self.use_black = True
        else:
            self.use_black = False

        if self.use_black:
            c = get_char_pressed()
            moved = 0

            all_text_length = 0
            for t in self.texts:
                all_text_length = all_text_length + len(t)
            all_text_length = all_text_length + len(self.text)

            if (c >= 32 and c <= 126) and all_text_length < 224:
                self.text = self.text + chr(c)

            if measure_text(self.text, 20) > (self.rect.width - self.text_push_x * 2):
                moved = 1
                self.rect.height = self.rect.height + self.starting_height - self.add_to_height
                self.rows += 1
                self.texts.append(self.text[:len(self.text) - 1])
                self.text = self.text[len(self.text) - 1]
            
            if is_key_pressed(KEY_BACKSPACE):
                if len(self.text) != 0:
                    self.text = self.text[:len(self.text) - 1]
                if len(self.texts) != 0 and len(self.text) == 0:
                    moved = -1
                    self.text = self.texts[len(self.texts) - 1]
                    self.texts.pop()
                    self.rect.height = self.rect.height - self.starting_height + self.add_to_height
            
            return moved
        
    def show(self):
        draw_rectangle_rec(self.rect, WHITE)
        if self.use_black:
            draw_rectangle_lines_ex(self.rect, 2, BLACK)
        else:
            draw_rectangle_lines_ex(self.rect, 2, GRAY)
        
        if len(self.texts) != 0:
            for i in range(len(self.texts)):
                draw_text(self.texts[i], int(self.rect.x + self.text_push_x), int((self.rect.y + self.starting_height / 2 -
                self.text_push_y) + self.add_h_to_draw * i), 20, BLACK)
            draw_text(self.text, int(self.rect.x + self.text_push_x), int((self.rect.y + self.starting_height / 2 - self.text_push_y) +
            self.add_h_to_draw * len(self.texts)), 20, BLACK)
        else:
            draw_text(self.text, int(self.rect.x + self.text_push_x), int(self.rect.y + self.starting_height / 2 - self.text_push_y), 20, BLACK)
