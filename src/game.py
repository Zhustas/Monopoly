from pyray import *
from raylib import MOUSE_BUTTON_LEFT, KEY_BACKSPACE, KEY_Q

class Game:
    window_width, window_height = 0, 0
    background_color = Color(169, 221, 255)

    in_game = False

    # When winner is found
    winner_found = False
    show_winner_page = False
    winner_index = 0
    second_place_index = 0
    third_place_index = 0

    # Rolling the dice
    whose_turn = ""
    whose_turn_kint = 0
    whose_turn_rect = None
    information_rect = None
    roll_dice_rect = None

    # Rolling for set time
    disable_rolling = False
    frame_width = 0
    maxFrames = 0
    timer = 0
    all_timer = 0
    rolling = False
    random_value = 0
    frame = 0

    update = False

    show_box_index = 0
    show_box_output = 0
    show_box = False

    # Figures
    figures_moving = False
    car_x = 0
    car_y = 0
    dog_x = 0
    dog_y = 0
    hat_x = 0
    hat_y = 0

    def __init__(self, window_w: int, window_h: int):
        self.window_width = window_w
        self.window_height = window_h

        self.players = ["Player 1", "Player 2", "Player 3"]
        self.figures = ["Car", "Dog", "Hat"]
        self.points = [0, 0, 0]
        self.positions = [0, 0, 0]

        self.whose_turn = self.players[self.whose_turn_kint]

        self.information_rect = Rectangle(0, 0, 300, window_h)
        self.whose_turn_rect = Rectangle(int(self.information_rect.width / 2) - 112, 395, 226, 30)
        self.roll_dice_rect = Rectangle(200, 440, 80, 30)

        self.dice = load_texture("data\Dices.png")
        self.frame_width = int(self.dice.width / 6)
        self.maxFrames = int(self.dice.width / self.frame_width)

        # Menu and exit logo
        self.go_to_menu = load_texture("data\To_menu.png")
        self.go_to_menu_x = 5
        self.go_to_menu_y = window_h - self.go_to_menu.height - 5

        self.exit = load_texture("data\To_exit.png")
        self.exit_x = 5 + self.exit.width
        self.exit_y = window_h - self.exit.height - 5

        # Figures
        self.car = load_texture("data\Car.png")
        self.dog = load_texture("data\Dog.png")
        self.hat = load_texture("data\Hat.png")

    def __del__(self):
        unload_texture(self.go_to_menu)
        unload_texture(self.exit)
        unload_texture(self.dice)
        unload_texture(self.car)
        unload_texture(self.dog)
        unload_texture(self.hat)

    def set_information(self, information: list):
        self.TS = information[0]
        self.players_count = int(information[1])
        self.points_to_win = information[2]

        node = self.TS.first
        i = 0
        while node != None:
            node.value.calculate_rect(i, self.TS.size)
            i += 1
            node = node.next

        self.car_x = 450 + 350 - self.hat.width - self.dog.width - self.car.width
        self.car_y = self.TS.first.value.rect.y - 30
        self.dog_x = 450 + 350 - self.hat.width - self.dog.width
        self.dog_y = self.TS.first.value.rect.y - 45
        self.hat_x = 450 + 350 - self.hat.width
        self.hat_y = self.TS.first.value.rect.y - 30

    def check_input(self):
        # Menu and exit buttons
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), (self.go_to_menu_x, self.go_to_menu_y,
        self.go_to_menu.width, self.go_to_menu.height)) and self.rolling == False:
            return 1
        
        if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), (self.exit_x, self.exit_y,
        self.exit.width, self.exit.height)) and self.rolling == False:
            return -1

        # Roll the dice
        if self.rolling == False and not self.winner_found:
            if is_mouse_button_pressed(MOUSE_BUTTON_LEFT) and check_collision_point_rec(get_mouse_position(), self.roll_dice_rect):
                self.random_value = get_random_value(1, 6)
                self.rolling = True
        
        if self.rolling:
            self.timer = self.timer + get_frame_time()

            if self.timer >= 0.25:
                self.timer = 0
                self.frame += 1
                self.all_timer += 0.25
            
            self.frame = self.frame % self.maxFrames
        
        if self.all_timer >= 1.5:
            if self.frame == self.random_value - 1:
                self.rolling = False
                self.timer = 0
                self.all_timer = 0
                self.update = True
        
        if self.update:
            self.positions[self.whose_turn_kint] += self.random_value

            if self.positions[self.whose_turn_kint] >= self.TS.size:
                self.positions[self.whose_turn_kint] %= self.TS.size
            
            self.points[self.whose_turn_kint] += self.TS.nodeat(self.positions[self.whose_turn_kint]).value.points

            if self.figures[self.whose_turn_kint] == "Car":
                self.car_x = self.TS.nodeat(self.positions[self.whose_turn_kint]).value.rect.x + 350 - self.hat.width - self.dog.width - self.car.width
                self.car_y = self.TS.nodeat(self.positions[self.whose_turn_kint]).value.rect.y - 30
            elif self.figures[self.whose_turn_kint] == "Dog":
                self.dog_x = self.TS.nodeat(self.positions[self.whose_turn_kint]).value.rect.x + 350 - self.hat.width - self.dog.width
                self.dog_y = self.TS.nodeat(self.positions[self.whose_turn_kint]).value.rect.y - 45
            elif self.figures[self.whose_turn_kint] == "Hat":
                self.hat_x = self.TS.nodeat(self.positions[self.whose_turn_kint]).value.rect.x + 350 - self.hat.width
                self.hat_y = self.TS.nodeat(self.positions[self.whose_turn_kint]).value.rect.y - 30

            if self.points[self.whose_turn_kint] >= self.points_to_win:
                self.winner_found = True
                self.show_winner_page = True
                self.winner_index = self.whose_turn_kint
                sk1, sk2 = -1, -1
                for i in range(self.players_count):
                    if sk1 == -1 and i != self.winner_index:
                        sk1 = i
                    elif sk2 == -1 and i != self.winner_index:
                        sk2 = i
                
                if self.players_count == 2:
                    self.second_place_index = sk1
                else:
                    if self.points[sk1] >= self.points[sk2]:
                        self.second_place_index = sk1
                        self.third_place_index = sk2
                    else:
                        self.second_place_index = sk2
                        self.third_place_index = sk1

            # Whose turn it is to roll the dice
            self.whose_turn_kint += 1
            if self.whose_turn_kint == self.players_count:
                self.whose_turn_kint = 0
            self.whose_turn = self.players[self.whose_turn_kint]

            self.update = False
        
        # Change names
        if self.rolling == False and not self.winner_found:
            for i in range(self.players_count):
                if check_collision_point_rec(get_mouse_position(), (10, 10 + i * 110, 300, 30)):
                    if measure_text(self.players[i], 30) < 250:
                        c = get_char_pressed()

                        if c >= 32 and c <= 126:
                            self.players[i] += chr(c)

                    if is_key_pressed(KEY_BACKSPACE) and len(self.players[i]) != 0:
                        self.players[i] = self.players[i][:len(self.players[i]) - 1]
            
            self.whose_turn = self.players[self.whose_turn_kint]
        
        # Field
        first_time = True
        sum_output = 0
        if self.rolling == False:
            node = self.TS.first
            i = 0
            while node != None:
                output = node.value.check_input(i, self.TS.size)
                if output == 1 or output == 2:
                    if first_time:
                        if output == 1:
                            self.show_box_output = "title"
                        elif output == 2:
                            self.show_box_output = "desc"
                        self.show_box_index = i
                        self.show_box = True
                        first_time = False
                sum_output += output
                i += 1
                node = node.next
            
            if sum_output == 0:
                self.show_box = False

        # Winner found
        if self.winner_found:
            self.disable_rolling = True

            changed = False
            if is_key_pressed(KEY_Q):
                if self.show_winner_page:
                    self.show_winner_page = False
                    changed = True
                if not self.show_winner_page and not changed:
                    self.show_winner_page = True

    def show(self):
        if not self.show_winner_page:
            clear_background(self.background_color)

            draw_rectangle_rec(self.information_rect, WHITE)
            draw_line_ex((int(self.information_rect.width), 0), (int(self.information_rect.width), int(self.window_height)), 2, BROWN)

            # Points to win
            draw_text("Points to win", 5, 500, 30, BLACK)
            draw_text(str(self.points_to_win), 5, 540, 30, BLACK)

            # Menu and exit buttons
            draw_texture(self.go_to_menu, self.go_to_menu_x, self.go_to_menu_y, WHITE)
            draw_texture(self.exit, self.exit_x, self.exit_y, WHITE)

            # Players information
            draw_text(self.players[0], 10, 10, 30, BROWN)
            draw_text("POINTS: {0}".format(self.points[0]), 10, 50, 20, BLACK)
            draw_text("FIGURE: {0}".format(self.figures[0]), 10, 80, 20, BLACK)

            draw_text(self.players[1], 10, 120, 30, BROWN)
            draw_text("POINTS: {0}".format(self.points[1]), 10, 160, 20, BLACK)
            draw_text("FIGURE: {0}".format(self.figures[1]), 10, 190, 20, BLACK)

            if self.players_count == 3:
                draw_text(self.players[2], 10, 230, 30, BROWN)
                draw_text("POINTS: {0}".format(self.points[2]), 10, 270, 20, BLACK)
                draw_text("FIGURE: {0}".format(self.figures[2]), 10, 300, 20, BLACK)

            turn_size = measure_text(self.whose_turn, 20)
            draw_rectangle_rec(self.whose_turn_rect, Color(243, 46, 46, 255))
            draw_rectangle_lines_ex(self.whose_turn_rect, 2, BLACK)
            draw_text("Your turn", int(self.whose_turn_rect.x + self.whose_turn_rect.width / 2 - 71), int(self.whose_turn_rect.y - 35), 30, BLACK)
            draw_text(self.whose_turn, int(self.information_rect.width / 2 - turn_size / 2), 400, 20, BLACK)

            draw_rectangle_rec(self.roll_dice_rect, Color(169, 221, 254, 255))
            draw_rectangle_lines_ex(self.roll_dice_rect, 2, BLACK)
            draw_text("ROLL", int(self.roll_dice_rect.x + 17), int(self.roll_dice_rect.y + 6), 20, BLACK)

            # Dice
            if self.rolling:
                draw_texture_rec(self.dice, Rectangle(self.frame_width * self.frame, 0, self.frame_width, self.dice.height),
                (self.window_width - self.frame_width - 10, 10), WHITE)
            else:
                draw_texture_rec(self.dice, Rectangle(self.frame_width * self.frame, 0, self.frame_width, self.dice.height),
                (self.window_width - self.frame_width - 10, 10), WHITE)
            
            # Field
            node = self.TS.first
            i = 0
            while node != None:
                node.value.show(i, self.TS.size)
                i += 1
                node = node.next

            # Figures 
            if self.players_count == 3:
                draw_texture(self.hat, int(self.hat_x), int(self.hat_y), WHITE)
            draw_texture(self.dog, int(self.dog_x), int(self.dog_y), WHITE)
            draw_texture(self.car, int(self.car_x), int(self.car_y), WHITE)

            # Field
            if self.show_box:
                self.TS.nodeat(self.show_box_index).value.show_box(self.show_box_index, self.TS.size, self.show_box_output)

        # Winner found
        if self.winner_found:
            if self.show_winner_page:
                clear_background(Color(183, 225, 250, 255))
                draw_text("WE HAVE A WINNER!!!", 30, 30, 30, BLACK)

                draw_rectangle(int(self.window_width / 2 - 300 / 2), int(self.window_height / 2 - 200), 300, 200, Color(252, 213, 94, 255))
                draw_rectangle_lines_ex((int(self.window_width / 2 - 300 / 2), int(self.window_height / 2 - 200), 300, 200), 2, BLACK)
                draw_text("1", int(self.window_width / 2 - 5), int(self.window_height / 2 - 180), 50, BLACK)
                text_size = measure_text(self.players[self.winner_index], 30)
                draw_text(self.players[self.winner_index], int(self.window_width / 2 - text_size / 2), int(self.window_height / 2 - 240), 30, BLACK)

                draw_rectangle(int(self.window_width / 2 - 460), int(self.window_height / 2 - 120), 300, 120, Color(182, 186, 197, 255))
                draw_rectangle_lines_ex((int(self.window_width / 2 - 460), int(self.window_height / 2 - 120), 300, 120), 2, BLACK)
                draw_text("2", int(self.window_width / 2 - 310 - 5), int(self.window_height / 2 - 100), 50, BLACK)
                text_size = measure_text(self.players[self.second_place_index], 30)
                draw_text(self.players[self.second_place_index], int(self.window_width / 2 - 310 - text_size / 2),
                int(self.window_height / 2 - 160), 30, BLACK)

                if self.players_count == 3:
                    draw_rectangle(int(self.window_width / 2 + 160), int(self.window_height / 2 - 60), 300, 60, Color(237, 127, 52, 255))
                    draw_rectangle_lines_ex((int(self.window_width / 2 + 160), int(self.window_height / 2 - 60), 300, 60), 2, BLACK)
                    draw_text("3", int(self.window_width / 2 + 310 - 5), int(self.window_height / 2 - 50), 50, BLACK)
                    text_size = measure_text(self.players[self.third_place_index], 30)
                    draw_text(self.players[self.third_place_index], int(self.window_width / 2 + 310 - text_size / 2),
                    int(self.window_height / 2 - 100), 30, BLACK)
                
                draw_text("1. {0} with {1} points".format(self.players[self.winner_index], self.points[self.winner_index]),
                int(self.window_width / 2 - 200), int(self.window_height / 2 + 100), 30, BLACK)
                draw_text("2. {0} with {1} points".format(self.players[self.second_place_index], self.points[self.second_place_index]),
                int(self.window_width / 2 - 200), int(self.window_height / 2 + 140), 30, BLACK)

                if self.players_count == 3:
                    draw_text("3. {0} with {1} points".format(self.players[self.third_place_index], self.points[self.third_place_index]),
                    int(self.window_width / 2 - 200), int(self.window_height / 2 + 180), 30, BLACK)
