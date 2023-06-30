from pyray import *
from menu import Menu
from CG import CreatingGame
from game import Game

WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
WINDOW_NAME = "Monopoly"

init_window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_NAME)

output = 0

menu = Menu(WINDOW_WIDTH, WINDOW_HEIGHT, "data\Logo.png")
cg = CreatingGame(WINDOW_WIDTH, WINDOW_HEIGHT, "data\To_menu.png", "data\To_exit.png")
cg.init()
game = Game(WINDOW_WIDTH, WINDOW_HEIGHT)

set_target_fps(60)
while not window_should_close():
    if menu.in_menu:
        output = menu.check_input()

        if output == 1:
            menu.in_menu = False
            cg.in_creating = True
        elif output == -1:
            break
    
    if cg.in_creating:
        output = cg.check_input()

        if output == 1:
            menu.in_menu = True
            cg.in_creating = False
            cg = CreatingGame(WINDOW_WIDTH, WINDOW_HEIGHT, "data\To_menu.png", "data\To_exit.png")
            cg.init()
        elif output == 10:
            cg.in_creating = False
            game.in_game = True
            game.set_information(cg.get_information())
            cg = CreatingGame(WINDOW_WIDTH, WINDOW_HEIGHT, "data\To_menu.png", "data\To_exit.png")
            cg.init()
        elif output == -1:
            break
    
    if game.in_game:
        output = game.check_input()

        if output == 1:
            menu.in_menu = True
            game.in_game = False
            game = Game(WINDOW_WIDTH, WINDOW_HEIGHT)
        elif output == -1:
            break

    begin_drawing()

    if menu.in_menu:
        menu.show()
    
    if cg.in_creating:
        cg.show()
    
    if game.in_game:
        game.show()

    end_drawing()

close_window()
