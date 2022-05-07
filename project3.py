# python3
# INFO-F101 : programming
# project3.py : Tetris
# Servais Nikita


from turtle import *
from random import randint
from time import time


################################
# Functions :                  #
#   Regroup all the functions #
#   under different class      #
################################

### miscellaneous functions ###
# unclassified function

def timer(x):
    """
    Return after x second
    """
    debut = time()
    fin = time()
    while fin - debut < x:
        fin = time()
    return


def draw_end(turtle, score):
    """
    Draw the score and ask if the player want to restart or quit
    """
    turtle.begin_fill()
    turtle.fillcolor('grey')
    turtle.penup()
    turtle.goto(-LENGTH * 9, -WIDTH * 9)
    turtle.goto(-LENGTH * 9, WIDTH * 9)
    turtle.goto(LENGTH * 9, WIDTH * 9)
    turtle.goto(LENGTH * 9, -WIDTH * 9)
    turtle.goto(-LENGTH * 9, -WIDTH * 9)
    turtle.end_fill()
    turtle.goto(0, 0)
    turtle.write(str(score) + " rows!", False, 'center',
                 ('Fixedsys', str(SQUARE_SIZE), 'normal'))
    turtle.goto(0, -SQUARE_SIZE)
    turtle.write("New Game : <spacebar>", False, 'center',
                 ('Fixedsys', '17', 'normal'))
    turtle.goto(0, -SQUARE_SIZE * 2)
    turtle.write("Quit : <esc>", False, 'center',
                 ('Fixedsys', '17', 'normal'))
    return


def reset():
    """
    Reset turtles, the board and restart the game
    """
    global BOARD
    board_turtle.clear()
    brick_turtle.clear()
    BOARD = [[0 for _ in range(WIDTH)] for _ in range(LENGTH)]
    tracer(0, 0)
    bgcolor('black')
    run_game()
    return


### main functions ###
# make the game work

def fall():
    """
    Make the brick move 1 square down each second
    """
    test = check_down(COORDINATES[0], COORDINATES[1])
    brick_turtle.clear()
    brick_draw(brick_turtle, COORDINATES[0], COORDINATES[1])
    i = 0
    timedown = time()
    while test:
        # if i%10 == 0 :
        #    COORDINATES[1] -= 1
        # brick_turtle.clear()
        # brick_draw(brick_turtle, COORDINATES[0], COORDINATES[1])
        # test = check_down(COORDINATES[0],COORDINATES[1])
        # timer(SLEEP/10)
        if time() - timedown >= SLEEP:
            timedown = time()
            COORDINATES[1] -= 1
            brick_turtle.clear()
            brick_draw(brick_turtle, COORDINATES[0], COORDINATES[1])
            test = check_down(COORDINATES[0], COORDINATES[1])
        i += 1

    res = board_add(COORDINATES[0], COORDINATES[1])
    board_draw(board_turtle, board2_turtle)
    return res


def run_game():
    """
    Runs the game and bind the controls
    """
    global BRICK
    BRICK = brick_generator()
    board_draw(board_turtle, board2_turtle)
    onkey(brick_rotate, 'Up')
    onkey(brick_left, 'Left')
    onkey(brick_right, 'Right')
    onkeypress(brick_speedup, 'Down')
    onkeyrelease(brick_speedreset, 'Down')
    score = 0
    brick_spawn()
    while fall():
        brick_spawn()
        BRICK = brick_generator()
        score += board_del()
    draw_end(board_turtle, score)
    onkey(reset, 'space')
    onkey(bye, 'Escape')
    return


### Board function ###
# all the functions used to handle the board

def board_draw(turtle, turtle2):
    """
    draw the board
    """
    global START
    if START:
        for i in range(len(BOARD) + 1):
            turtle2.penup()
            turtle2.goto(X * SQUARE_SIZE - SQUARE_SIZE,
                         (i + Y) * SQUARE_SIZE - SQUARE_SIZE)
            turtle2.pendown()
            draw_square(turtle2, 'grey')

        for i in range(len(BOARD) + 2):
            turtle2.penup()
            turtle2.goto((X + WIDTH + 1) * SQUARE_SIZE - SQUARE_SIZE,
                         (i + Y) * SQUARE_SIZE - SQUARE_SIZE)
            turtle2.pendown()
            draw_square(turtle2, 'grey')
        for i in range(len(BOARD[0]) + 1):
            turtle2.penup()
            turtle2.goto((i + X) * SQUARE_SIZE - SQUARE_SIZE,
                         Y * SQUARE_SIZE - SQUARE_SIZE)
            turtle2.pendown()
            draw_square(turtle2, 'grey')

        for i in range(len(BOARD[0]) + 1):
            turtle2.penup()
            turtle2.goto((i + X) * SQUARE_SIZE - SQUARE_SIZE,
                         (Y + LENGTH + 1) * SQUARE_SIZE - SQUARE_SIZE)
            turtle2.pendown()
            draw_square(turtle2, 'grey')
    else:
        for i, row in enumerate(BOARD):
            for j, elem in enumerate(row):
                turtle.penup()
                turtle.goto((j + X) * SQUARE_SIZE, (i + Y) * SQUARE_SIZE)
                turtle.pendown()
                if elem != 0:
                    draw_square(turtle, elem)
    START = False
    update()
    return


def board_add(x, y):
    """
    Add a brick to the board 
    Return False if the brick is out of the board 
    """
    test = True
    for i in range(len(BRICK)):
        if i + y < len(BOARD):
            for j in range(len(BRICK[i])):
                if BRICK[i][j] != 0 and BOARD[i + y][j + x] == 0:
                    BOARD[i + y][j + x] = BRICK[i][j]
        else:
            test = False
    return test


def board_del():
    """
    Delete a row of the board if it's full
    """
    score = 0
    for i in reversed(range(len(BOARD))):
        test = True
        j = 0
        while j < len(BOARD[0]) and test:
            if BOARD[i][j] == 0:
                test = False
            j += 1
        if test:
            score += 1
            BOARD.pop(i)
            BOARD.append([0 for _ in range(WIDTH)])
            board_turtle.clear()
            board_draw(board_turtle, board2_turtle)
    return score


### Brick functions ###
# all the functions used to handle the brick

def draw_square(turtle, color):
    """
    Draw a square at the current location and
    fill it with the color given
    """
    turtle.width(2)
    turtle.pencolor('black')
    turtle.begin_fill()
    turtle.fillcolor(color)
    for i in range(4):
        turtle.forward(SQUARE_SIZE)
        turtle.left(90)
    turtle.end_fill()
    return


def brick_draw(turtle, x, y):
    """
    draw a brick at the given position
    """
    for i, row in enumerate(BRICK):
        for j, elem in enumerate(row):
            turtle.penup()
            turtle.goto((j + X + x) * SQUARE_SIZE, (i + Y + y) * SQUARE_SIZE)
            turtle.pendown()
            if BRICK[i][j] != 0:
                draw_square(turtle, BRICK[i][j])
    update()
    return


def brick_generator():
    """
    Generate a random brick from a list 
    and a random color from a list
    Return a brick colored
    """
    all_colors = ['red', 'magenta', 'green1', 'blue', 'cyan',
                  'yellow', 'darkorange3']
    color = all_colors[randint(0, len(all_colors) - 1)]
    bricks = [[[color, color],
               [color, color]],
              [[color, 0, 0],
               [color, color, color]],
              [[color, color, color, color]],
              [[0, color, 0],
               [color, color, color]],
              [[color, color, 0],
               [0, color, color]]]
    brick = bricks[randint(0, len(bricks) - 1)]
    return brick


def brick_rotate():
    """
    Rotate a brick 
    """
    global BRICK
    brick_test = [[BRICK[i][j] for i in range(len(BRICK))]
                  for j in reversed(range(len(BRICK[0])))]
    test = check_rotate(brick_test, COORDINATES[0], COORDINATES[1])
    if test:
        BRICK = brick_test
        brick_turtle.clear()
        brick_draw(brick_turtle, COORDINATES[0], COORDINATES[1])
    return


def brick_left():
    """
    Move a brick to the left
    """
    test = check_left(COORDINATES[0], COORDINATES[1])
    if test:
        COORDINATES[0] -= 1
        brick_turtle.clear()
        brick_draw(brick_turtle, COORDINATES[0], COORDINATES[1])
    return


def brick_right():
    """
    Move a brick to the right
    """
    test = check_right(COORDINATES[0], COORDINATES[1])
    if test:
        COORDINATES[0] += 1
        brick_turtle.clear()
        brick_draw(brick_turtle, COORDINATES[0], COORDINATES[1])
    return


def brick_speedreset():
    """
    Reset SLEEP to the initial value
    """
    global SLEEP
    SLEEP = 1
    return


def brick_speedup():
    """
    Reduce SLEEP which is inversely proportional to the speed
    """
    global SLEEP
    SLEEP = 0.01
    return


def brick_spawn():
    """
    Set the coordinates of the brick to the spawn position
    """
    COORDINATES[0] = WIDTH // 2
    COORDINATES[1] = LENGTH
    return


### Checking functions ###
# all the functions used to verify conditions of the bricks movements

def check_rotate(brick, x, y):
    """
    Check if the brick can rotate
    Return False if it can't
    """
    test = True
    i = 0
    if i + y + len(brick) > len(BOARD):
        test = False
    while i < len(brick) and i + y < len(BOARD) and test:
        j = 0
        if j + x + len(brick[0]) > len(BOARD[0]):
            test = False
        while j < len(brick[i]) and test:
            if brick[i][j] != 0 and BOARD[i + y][j + x] != 0:
                test = False
            j += 1
        i += 1
    return test


def check_down(x, y):
    """
    Check if the brick can go down
    Return False if it can't
    """
    test = True
    i = 0
    while i < len(BRICK) and i + y - 1 < len(BOARD) and test:
        j = 0
        while j < len(BRICK[i]) and test:
            if (BRICK[i][j] != 0 and BOARD[i + y - 1][j + x] != 0) or y == 0:
                test = False
            j += 1
        i += 1
    return test


def check_right(x, y):
    """
    Check if the brick can go right 
    Return False if it can't
    """
    test = False
    i = 0
    j = len(BRICK[0]) - 1
    if j + x + 1 < len(BOARD[0]):
        test = True
    while i < len(BRICK) and i + y < len(BOARD) and test:
        if BRICK[i][j - 1] != 0 and BOARD[i + y][j + 1 + x] != 0:
            test = False
        i += 1
    return test


def check_left(x, y):
    """
    Check if the brick can go left
    Return False if it can't
    """
    test = False
    i = 0
    j = 0
    if j + x > 0:
        test = True
    while i < len(BRICK) and i + y < len(BOARD) and test:
        if BRICK[i][j] != 0 and BOARD[i + y][j - 1 + x] != 0:
            test = False
        i += 1
    return test


##############################
# Global variables :         #
#   all the global variables #
##############################

### reference ###
# used to measure scale, can be changed to suit your needs
START = True
SQUARE_SIZE = 25
WIDTH = 14
LENGTH = 20
X = -WIDTH // 2
Y = -LENGTH // 2
BOARD = [[0 for i in range(WIDTH)] for j in range(LENGTH)]
### init variables ###
COORDINATES = [0, 0]
SLEEP = 1
BRICK = "tetrimino"
### Setup turtles ###
# setup the turtle function and the screen functions

title("TETRIS")
tracer(0, 0)
bgcolor('black')
setup((SQUARE_SIZE * WIDTH) * 1.2, (SQUARE_SIZE * LENGTH) * 1.2)
board_turtle = Turtle()
board2_turtle = Turtle()
brick_turtle = Turtle()
board_turtle.hideturtle()
board2_turtle.hideturtle()
brick_turtle.hideturtle()

############################
#  Main loop :             #
#   where the magic happen #
############################
listen()
run_game()
mainloop()
