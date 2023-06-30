from pyray import *

class Field:
    rect_color = Color(205, 230, 208, 255)
    rect = None

    title_dots = False
    title_dots_text = ""
    desc_dots = False
    desc_dots_text = ""

    timer = 0

    # Box
    s_box_title = False
    s_box_desc = False

    def __init__(self, title: str, desc: str, points: int):
        self.title = title
        self.desc = desc
        self.points = points

        self.move_by_x = 450
        self.move_by_y = 67

        if measure_text(title, 20) + 10 > 330:
            self.title_dots = True
            i = 0
            while measure_text(self.title_dots_text, 20) + 10 + 6 < 330:
                self.title_dots_text += title[i]
                i += 1
            self.title_dots_text += "..."
            self.texts_title = []
            self.calculate_box(title, "title")
        
        if measure_text(desc, 20) + 10 > 330:
            self.desc_dots = True
            i = 0
            while measure_text(self.desc_dots_text, 20) + 10 + 6 < 330:
                self.desc_dots_text += desc[i]
                i += 1
            self.desc_dots_text += "..."
            self.texts_desc = []
            self.calculate_box(desc, "desc")

    def check_input(self, index_in_list: int, size_of_list: int):
        starting_y = 450 - 33 * size_of_list
        b = index_in_list % 2
        if self.title_dots:
            if check_collision_point_rec(get_mouse_position(), (455 + b * self.move_by_x, starting_y + 5 + index_in_list * self.move_by_y, 350, 20)):
                self.timer += get_frame_time()
            else:
                self.timer = 0
                self.s_box_title = False
            
            if self.timer >= 1:
                self.s_box_title = True
                return 1
        
        if self.desc_dots:
            if check_collision_point_rec(get_mouse_position(), (455 + b * self.move_by_x, starting_y + 25 + index_in_list * self.move_by_y, 350, 20)):
                self.timer += get_frame_time()
            else:
                self.timer = 0
                self.s_box_desc = False
            
            if self.timer >= 1:
                self.s_box_desc = True
                return 2
        
        return 0

    def calculate_rect(self, index_in_list: int, size_of_list: int):
        starting_y = 450 - 33 * size_of_list
        b = index_in_list % 2

        self.rect = Rectangle(450 + b * self.move_by_x, starting_y + index_in_list * self.move_by_y, 350, 67)

    def calculate_box(self, text: str, keyword: str):
        temp_text = ""
        added = False
        if keyword == "title":
            for i in range(len(text)):
                if measure_text(temp_text, 20) + 10 < 330:
                    temp_text += text[i]
                else:
                    self.texts_title.append(temp_text)
                    temp_text = ""
                    added = True
                if i == len(text) - 1 and not added and temp_text != "":
                    self.texts_title.append(temp_text)
                added = False
        
        if keyword == "desc":
            for i in range(len(text)):
                if measure_text(temp_text, 20) + 10 < 330:
                    temp_text += text[i]
                else:
                    self.texts_desc.append(temp_text)
                    temp_text = text[i]
                    added = True
                if i == len(text) - 1 and not added and temp_text != "":
                    self.texts_desc.append(temp_text)
                added = False
    
    def show_box(self, index_in_list: int, size_of_list: int, keyword: str):
        if keyword == "title":
            draw_rectangle(700, 450, 350, 30 * len(self.texts_title), WHITE)
            draw_rectangle_lines(700, 450, 350, 30 * len(self.texts_title), BLACK)
            for i in range(len(self.texts_title)):
                draw_text(self.texts_title[i], 705, 455 + i * 30, 20, BLACK)
        
        if keyword == "desc":
            draw_rectangle(700, 450, 350, 30 * len(self.texts_desc), WHITE)
            draw_rectangle_lines(700, 450, 350, 30 * len(self.texts_desc), BLACK)
            for i in range(len(self.texts_desc)):
                draw_text(self.texts_desc[i], 705, 455 + i * 30, 20, BLACK)

    def show(self, index_in_list: int, size_of_list: int):
        starting_y = 450 - 33 * size_of_list
        b = index_in_list % 2

        self.rect = Rectangle(450 + b * self.move_by_x, starting_y + index_in_list * self.move_by_y, 350, 67)

        # Field
        draw_rectangle(450 + b * self.move_by_x, starting_y + index_in_list * self.move_by_y, 350, 67, Color(205, 230, 208, 255))
        draw_rectangle_lines(450 + b * self.move_by_x, starting_y + index_in_list * self.move_by_y, 350, 67, BLACK)

        # Title
        text = ""
        if self.title_dots:
            text = self.title_dots_text
        else:
            text = self.title
        draw_text(text, 455 + b * self.move_by_x, starting_y + 5 + index_in_list * self.move_by_y, 20, BLACK)

        # Description
        if self.desc_dots:
            text = self.desc_dots_text
        else:
            text = self.desc
        draw_text(text, 455 + b * self.move_by_x, starting_y + 25 + index_in_list * self.move_by_y, 20, BLACK)

        # Points
        draw_text(str(self.points), 455 + b * self.move_by_x, starting_y + 45 + index_in_list * self.move_by_y, 20, BLACK)

    def show_preview(self, index_in_list: int, size_of_list: int):
        starting_y = 450 - 33 * size_of_list
        b = index_in_list % 2

        # Field
        draw_rectangle(100 + b * self.move_by_x, starting_y + index_in_list * self.move_by_y, 200, 67, Color(205, 230, 208, 255))
        draw_rectangle_lines(100 + b * self.move_by_x, starting_y + index_in_list * self.move_by_y, 200, 67, BLACK)

        text_size = measure_text(self.title, 20)
        if text_size > 200:
            text = ""
            i = 0
            while measure_text(text, 20) < 160:
                text += self.title[i]
                i += 1
            text += "..."
            draw_text(text, 100 + b * self.move_by_x + 5, starting_y + index_in_list * self.move_by_y + 5, 20, BLACK)
        else:
            draw_text(self.title, 100 + b * self.move_by_x + 5, starting_y + index_in_list * self.move_by_y + 5, 20, BLACK)
        draw_text("DESC", 100 + b * self.move_by_x + 5, starting_y + index_in_list * self.move_by_y + 25, 20, BLACK)
        draw_text(str(self.points), 100 + b * self.move_by_x + 5, starting_y + index_in_list * self.move_by_y + 45, 20, BLACK)
