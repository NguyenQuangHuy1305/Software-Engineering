from turtle import shape
import pygame
import random
import sqlite3

# import test_ai.py
import test_ai

# import button.py
import button

import tkinter as tk

# import tkinter to display popup dialog box
from tkinter import messagebox
from tkinter import *

from pygame import mixer
pygame.mixer.init()
# background sound
mixer.music.load('sounds\Loonboon.wav')

piece_drop_sound = mixer.Sound('sounds\SFX_PieceSoftDrop.wav')
piece_move_LR = mixer.Sound('sounds\SFX_PieceMoveLR.wav')
piece_rotate_fail = mixer.Sound('sounds\SFX_PieceRotateFail.wav')
piece_rotate_LR = mixer.Sound('sounds\SFX_PieceRotateLR.wav')
piece_move_LR = mixer.Sound('sounds\SFX_PieceMoveLR.wav')
piece_touch_LR = mixer.Sound('sounds\SFX_PieceTouchLR.wav')
piece_touch_down = mixer.Sound('sounds\SFX_PieceTouchDown.wav')
start_sound = mixer.Sound('sounds\gta-san-andreas-ah-shit-here-we-go-again.wav')
dead_sound = mixer.Sound('sounds\Mission Failed Well get em next time.wav')
menu_sound = mixer.Sound('sounds\Graze the Roof.wav')

piece_clear_1 = mixer.Sound('sounds\SFX_SpecialLineClearSingle.wav')
piece_clear_2 = mixer.Sound('sounds\SFX_SpecialLineClearDouble.wav')
piece_clear_3 = mixer.Sound('sounds\SFX_SpecialLineClearTriple.wav')
piece_clear_4 = mixer.Sound('sounds\SFX_SpecialTetris.wav')

root = Tk()
root.title("Submit highscore")
# root.withdraw() # to remove the tk root window

# setting icons
pygame_icon = pygame.image.load('icon.png')
pygame.display.set_icon(pygame_icon)

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T, i
represented in order by 0 - 7
"""

pygame.font.init()

# GLOBALS VARS
s_width = 1200 # width of game window
s_height = 700 # height of game window
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30 # each block has size of 30
click = False

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# the main pygame window
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

# LOAD BUTTON IMAGES
start_img = pygame.image.load('images/start.png').convert_alpha()
configure_img = pygame.image.load('images/configure.png').convert_alpha()
highscore_img = pygame.image.load('images/highscore.png').convert_alpha()
exit_img = pygame.image.load('images/exit.png').convert_alpha()
close_img = pygame.image.load('images/close.png').convert_alpha()
resume_img = pygame.image.load('images/resume.png').convert_alpha()
yes_img = pygame.image.load('images/yes.png').convert_alpha()
no_img = pygame.image.load('images/no.png').convert_alpha()

# CREATE BUTTONS
start_button = button.Button(s_width/2 - start_img.get_width()/2 -4, s_height/2 - start_img.get_height()/2 -50, start_img, 1)
configure_button = button.Button(s_width/2 - configure_img.get_width()/2, s_height/2 - configure_img.get_height()/2, configure_img, 1)
highscore_button = button.Button(s_width/2 - highscore_img.get_width()/2, s_height/2 - highscore_img.get_height()/2 +50, highscore_img, 1)
close_button = button.Button(s_width/2 - close_img.get_width()/2, 400, close_img, 1)
resume_button = button.Button(s_width/2 - resume_img.get_width()/2, s_height/2 - resume_img.get_height()/2 - 25, resume_img, 1)
exit_button = button.Button(s_width/2 - exit_img.get_width()/2, s_height/2 - exit_img.get_height()/2 + 100, exit_img, 1)
yes_button = button.Button(s_width/2 - yes_img.get_width()/2 - 150, s_height/2 - yes_img.get_height()/2, yes_img, 1)
no_button = button.Button(s_width/2 - no_img.get_width()/2 + 150, s_height/2 - no_img.get_height()/2, no_img, 1)

# SHAPE FORMATS
S = [['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....'],
    ['.....',
    '......',
    '..00..',
    '.00...',
    '.....']]

Z = [['.....',
    '.....',
    '.00..',
    '..00.',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '.0...',
    '.....']]

I = [['..0..',
    '..0..',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '0000.',
    '.....',
    '.....',
    '.....']]

O = [['.....',
    '.....',
    '.00..',
    '.00..',
    '.....']]

J = [['.....',
    '.0...',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..00.',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '.00..',
    '.....']]

L = [['.....',
    '..0..',
    '..0..',
    '..00.',
    '.....'],
    ['.....',
    '...0.',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '.0...',
    '.....'],
    ['.....',
    '.00..',
    '..0..',
    '..0..',
    '.....']]

T = [['.....',
    '..0..',
    '..00.',
    '..0..',
    '.....'],
    ['.....',
    '..0..',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '..0..',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '..0..',
    '.....']]

i = [['.....',
    '..0..',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '.000.',
    '.....',
    '.....',
    '.....']]

C = [['.....',
    '.....',
    '..00.',
    '..0..',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '.....',
    '.....'],
    ['.....',
    '.....',
    '.00..',
    '..0..',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '.....',
    '.....']]

# normal_shape = [S, Z, I, O, J, L, T]
# normal_shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

shapes = [S, Z, I, O, J, L, T, i, C]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128), (0, 255, 180), (0, 0, 180)]
# index 0 - 8 represent shape

# create the class for tetris pieces
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape # shape here is a list of lists, for example: list of lists named "O" in line 93
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

# # connect to database
# conn = sqlite3.connect('highscore.db')
# # create a cusor
# c = conn.cursor()

# # c.execute("""CREATE TABLE Player (
# #         name text,
# #         score integer
# #         )""")

# # c.execute("INSERT INTO Player VALUES ('test2', 2000)")
# # order by score
# c.execute("SELECT * from Player ORDER BY score DESC LIMIT 10")

# players = c.fetchall()

# for player in players:
#     print(player[0])
#     # print(player.score)

# # commit the command
# conn.commit()
# # close the connection
# conn.close()

# class Player(object):
#     def __init__(self, name, score):
#         self.name = name
#         self.score = score

# function to create the grid (given locked position as a dict)
def create_grid(locked_positions = {}):
    """
    Takes a dict of locked positions and return a drawn grid
    The dict locked_positions is a dict, key is the location of the cell, value is the colour, ex: {(1,1):(0,0,0), (1,2):...}
    """
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)] # for starter, all grid "elements" are black squares (grid is a list)

    for i in range(len(grid)): # loop through all rows, len(grid) == 20
        for j in range(len(grid[i])): # loop through all column of that row, len(grid[i]) == 10
            if (j, i) in locked_positions: # (x,y) aka (j,i) because j is x value (row) and i is y value (column)
                # loop through the grid, if any positions (ex: (1,1)) is in locked_positions, then get the value (colour) of that position from the locked_positions, and overwrite the current grid's element with that value (colour)
                c = locked_positions[(j,i)]
                grid[i][j] = c

    return grid

def convert_shape_format(shape):
    """
    function to convert from a passed-in shape object to a list of positions
    """
    positions = []
    # shape.shape is a list of lists like this: [[],[]], which is either one of these lists: S, Z, I, O, J, L, T
    # shape.rotation % len(shape.shape) is the index (example: 1, 2, 3, or 4, depend on the current rotation "count", 0%4=0, 1%4=1, 2%4=2, 3%4=3, 4%4=0,...)
    format = shape.shape[shape.rotation % len(shape.shape)]

    # loop through the list called format which we got above
    for i, line in enumerate(format):
        row = list(line)
        # turn line into a list called row, then loop through it
        for j, column in enumerate(row):
            if column == '0':
                # if a 0 is found, add that position to the list positions
                positions.append((shape.x + j, shape.y + i))

    # need to modify the positions list, basically moving the shape left 2 and up 4
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    # return a list of positions, which are all the blocks that create the shape
    return positions

def valid_space(shape, grid):
    """
    function to check the grid if we're moving the shape into an accepted pos
    TRUE == the shape is NOT in valid spaces
    FALSE == the shape is still in valid spaces
    """
    # loop through all the possible positions, only add in accepted_pos if the colour is black (0,0,0)
    # accepted_pos is a list of sublists: [ [(1,1)], [(2,2)] ]
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    # this line convert the above list of sublists into a list of tuples: [ (1,1), (2,2) ]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    # convert the passed-in shape into the same format as accepted_pos for comparison [ (1,1), (2,2) ], formatted is now a list of blocks that are part of the shape
    formatted = convert_shape_format(shape)

    # loop through all the blocks (pos) of the shape (formatted)
    for pos in formatted:
        # if any of the blocks (pos) of the shape is not in accepted_pos
        if pos not in accepted_pos:
            # if the x value (current horizontal pos) of the 1st block (left most block) of the shape is > -1, aka the shape is in the play area
            if pos[1] > -1:
                # then return false, aka the shape is NOT in valid space
                return False
    return True

def check_lost(positions):
    """
    func to check if the player is lost or not, required a parameter locked_positions
    basically check if any of the locked positions has y < 1  (aka the highest locked positions has touched the ceiling), then return True (lost), if not, return False
    """
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape(game_mode):
    """
    function to get a random Piece (shape)
    """
    if game_mode == 'normal':
        return Piece(5, 0, random.choice(shapes[0:7]))
    if game_mode == 'extended':
        return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    """
    simple function to draw text in the middle of the screen
    """
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + 80 - label.get_height()/2))

def draw_grid(surface, grid):
    """
    function to draw the grid lines, given the actual grid (a list of colours) and the surface to draw the grid on
    """
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        # for each row, draw a line(surface = where to draw, (128,128,128) = draw in what colour, (sx, sy + i*block_size) = start drawing at which location, (sx + play_width, sy + i*block_size) = stop drawing at which location)
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx + play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            # similar to the above note, but for each columns
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))

def clear_rows(grid, locked):
    """
    function to clear row from the bottom up, require a grid and locked_positions as parameter
    """
    inc = 0 # to count how many row do we need to move "the above rows" down
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def draw_next_shape(shape, surface):
    """
    func to draw the next shape to the right of the play area
    """
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))
    
    sx = top_left_x + play_width +50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column, in enumerate(row):
            if column =='0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
    
    surface.blit(label, (sx, sy - 40))


def update_score(nscore, name):
    """
    func to update the scores.txt file with the 10 highest scores
    """
    # connect to database
    conn = sqlite3.connect('highscore.db')
    # create a cusor
    c = conn.cursor()

    c.execute("INSERT INTO Player (name, score) VALUES (?, ?)", (name, nscore))

    # commit the command
    conn.commit()
    # close the connection
    conn.close()

    # # open the file, append new highscore, sort the list, only take [0:10]
    # with open('scores.txt', 'r') as f:
    #     data = f.readlines()
    #     scores.append(str(nscore) + "\n")
    #     scores = sorted(scores, key=int, reverse=True)
    #     scores = scores[0:10]

    # # write the length 10 list back to the file
    # with open('scores.txt', 'w') as f:
    #     for score in scores:
    #         f.write(str(score))

def draw_window(surface, grid, score=0, inc=0, level=1):
    """
    function to draw the game window, given the grid (a list of colours) and the surface to draw the grid on, along with some other stats (score, level,...)
    """

    # fill the window with black
    surface.fill((0,0,0))

    pygame.font.init()

    # game title
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render("Group 5", 1, (255,255,255))
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 10))

    # current score
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Current score: ' + str(score), 1, (255,255,255))
    sx = top_left_x + play_width +50
    sy = top_left_y + play_height/2 -100
    surface.blit(label, (sx, sy + 120))

    # lines cleared
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Lines cleared: ' + str(inc), 1, (255,255,255))
    sx = top_left_x + play_width +50
    sy = top_left_y + play_height/2 -100
    surface.blit(label, (sx, sy + 160))

    # current level
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Current level: ' + str(level), 1, (255,255,255))
    sx = top_left_x + play_width +50
    sy = top_left_y + play_height/2 -100
    surface.blit(label, (sx, sy + 200))

    # current game mode
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Current game mode: normal', 1, (255,255,255))
    sx = top_left_x + play_width +50
    sy = top_left_y + play_height/2 -100
    surface.blit(label, (sx, sy + 240))

    #  AI or human
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Player mode: player', 1, (255,255,255))
    sx = top_left_x + play_width +50
    sy = top_left_y + play_height/2 -100
    surface.blit(label, (sx, sy + 280))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)

def main(win):
    """
    main func to run the game
    """
    locked_positions = {} # initiate the locked_position dict
    grid = create_grid(locked_positions) # call create_grid fuction with given (blank) locked_positions dict
    game_paused = False # pretty much self-explanatory
    
    change_piece = False # default is false, will be changed whenever a shape hit a locked_position
    run = True # while  True -> while run so that we can flip this bool var later

    game_mode = 'normal'
    current_piece = get_shape(game_mode) # get a random current piece
    next_piece = get_shape(game_mode) # get a random next piece
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.25 # how long it take for a piece to move 1 row down
    level_time = 0
    score = 0
    inc = 0
    level = 1

    AI = False
    mixer.music.play(-1)
    start_sound.play()
    menu_sound.stop()
    while run:
        # create the grid based on locked_positions
        grid = create_grid(locked_positions)
        
        # while game_paused == False, increment time as usual, of not, time stops
        if game_paused == False:
            fall_time += clock.get_rawtime() # gradually increase fall_time
            level_time += clock.get_rawtime() # gradually increase level_time
            clock.tick()

        # if level_time reach 5 (secs), increase level by 1
        if level_time/1000 > 5:
            level_time = 0
            level += 1
            if fall_speed > 0.12: # min speed is going to be 0.12
                fall_speed -= 0.005 # took 1m40s before hitting fall_speed = 0.12

        # if fall_time (auto increase) > fall speed, then move the piece down 1 row
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            # if the (just moved down 1 row) piece hit an invalid space, then move the piece back up 1 row, and change_piece 
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        events = []
        if AI == True:
            events = list(pygame.event.get()) + test_ai.run_ai(current_piece, grid, locked_positions)
        if AI == False:
            events = pygame.event.get()

        for event in events:
        # for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            
            # in the event the user press a key
            if event.type == pygame.KEYDOWN:
                # in the event the user press left key -> move piece to the left aka current_piece.x -= 1
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    piece_move_LR.play()
                    # if the new place of the piece is not a valid space, then just undo the previous movement
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                        piece_touch_LR.play()
                # in the event the user press right key -> move piece to the right aka current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    piece_move_LR.play()
                    # if the new place of the piece is not a valid space, then just undo the previous movement
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                        piece_touch_LR.play()
                # in the event the user press down key -> move piece down aka current_piece.y += 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    # if the new place of the piece is not a valid space, then just undo the previous movement
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1

                # in the event the user press space key -> move piece down until it hits (overlaps) an invalid space (in another word: move the piece down continuously as long as it's still in valid space)
                if event.key == pygame.K_SPACE:
                    piece_drop_sound.play()
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1

                # in the event the user press up key -> rotate the piece
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    piece_rotate_LR.play()
                    # if the new place of the piece is not a valid space, then just undo the previous rotation
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                        piece_rotate_fail.play()
                # in the event the user press P key -> stop time increment
                if event.key == pygame.K_p:
                    game_paused = not game_paused
                # in the event the user press esc key
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
                    draw_text_middle("Paused", 120, (255,255,255), win)
                    pygame.display.update()
                    response = messagebox.askyesno("Confirmation", "Do you want to finish the game?")
                    if response == True:
                        run = False
                        pygame.display.quit()
                    if response == False:
                        game_paused = not game_paused

        # convert the object "current_piece" from Piece to a list of positions
        shape_pos = convert_shape_format(current_piece)
        # print(shape_pos)

        # loop through all the pos of the blocks of the shapes, if it's in the play area, change the color accordingly
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: # we're not above the play area
                grid[y][x] = current_piece.color # update the grid with correct color

        # in the event change_piece was changed to true:
        if change_piece:
            # update locked_positions, locked_positions is a dict like this: {(1,2), (255,255,255)}, whereas the key is the location, value is the color
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece # replace the current piece with next piece
            next_piece = get_shape(game_mode) # initiate the new piece
            change_piece = False # turn the var back to False

            # only clear_rows when the previous piece hits the ground (when change_piece)
            x = clear_rows(grid, locked_positions)
            if x == 1:
                score += 100
                inc += 1
                piece_clear_1.play()
            elif x == 2:
                score += 300
                inc += 2
                piece_clear_2.play()
            elif x == 3:
                score += 600
                inc += 3
                piece_clear_3.play()
            elif x == 4:
                score += 1000
                inc += 4
                piece_clear_4.play()
            # inc += clear_rows(grid, locked_positions)

        draw_window(win, grid, score, inc, level)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if game_paused == True:
            draw_text_middle("Paused", 120, (255,255,255), win)
            pygame.display.update()

        # in case of losing
        if check_lost(locked_positions):
            mixer.music.stop()
            dead_sound.play()
            if AI == False:
                # by default, we will not update user's score
                record_new_player_score = False

                draw_text_middle('You lost', 80, (255,255,255), win)
                pygame.display.update()

                # connect to database
                conn = sqlite3.connect('highscore.db')
                # create a cusor
                c = conn.cursor()

                # get a list of tuples, tuple[0] = name, tuple[1] = score, order by score
                c.execute("SELECT * from Player ORDER BY score DESC LIMIT 10")
                players = c.fetchall()

                for player in players:
                    if player[1] < score:
                        record_new_player_score = True
                    else:
                        record_new_player_score = False

                # commit the command
                conn.commit()
                # close the connection
                conn.close()

                if record_new_player_score == True:
                    root.title("Submit highscore")
                    root.iconbitmap('icon.ico')

                    e = Entry(root, width=50)
                    e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

                    def submit(name):
                        print(f'Updateing score for: {name}')
                        update_score(score, name)
                        main_menu(win)

                    def restart():
                        main(win)
                        root.withdraw()

                    submitButton = Button(root, text='Submit', command=lambda: submit(e.get()))
                    reStartButton = Button(root, text='Restart', command=lambda: restart())
                    quitButton = Button(root, text="Quit", command=root.destroy)

                    submitButton.grid(row=1, column=0)
                    reStartButton.grid(row=1, column=1)
                    quitButton.grid(row=1, column=2)

                    root.mainloop()
                pygame.time.delay(1500)
                run = False
            elif AI == True:
                draw_text_middle('The AI lost', 80, (255,255,255), win)
                pygame.display.update()

                response = messagebox.askyesno("What now?", "You want to restart?")
                update_score(score, 'AI')
                if response == True:
                    main(win)
                if response == False:
                    main_menu(win)

def main_menu(win):
    """
    the main menu with some options and information
    """
    menu_sound.stop()
    menu_sound.play(-1)
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle("Tetris", 120, (255,255,255), win)

        if start_button.draw(win):
            main(win)
        if configure_button.draw(win):
            configure_menu(win)
        if highscore_button.draw(win):
            highscore_menu(win)
        if exit_button.draw(win):
            run = False
            pygame.display.quit()

        # year and course code
        font = pygame.font.SysFont('comicsans', 20)
        label = font.render('Year: 2022, course code: 7805ICT', 1, (255,255,255))
        sx = 10
        sy = s_height - label.get_height() -10
        win.blit(label, (sx, sy))

        # Student list
        font = pygame.font.SysFont('comicsans', 20)
        label = font.render('Group members: Yen-Cheng Chen, Quang Huy Nguyen, Xinghan TAi', 1, (255,255,255))
        sx = s_width - label.get_width() -10
        sy = s_height - label.get_height() -10
        win.blit(label, (sx, sy))

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

        pygame.display.update()

def configure_menu(win):
    """
    The configure menu, for now it's only hard coded string being displayed
    """
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle("Configuration", 100, (255,255,255), win)

        # draw size option within configuration page
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Size of the field: 10x20', 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 -100
        win.blit(label, (sx, sy))

        # draw game level option within configuration page
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Game level: 1, increase after every 5s', 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 -100
        win.blit(label, (sx, sy + 50))

        # draw game mode option within configuration page
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Game mode: normal', 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 -100
        win.blit(label, (sx, sy + 100))

        # draw player mode option within configuration page
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Player mode: player', 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 -100
        win.blit(label, (sx, sy + 150))

        # recreate the exit button
        close_button = button.Button(s_width/2 - close_img.get_width()/2, s_height/2 - close_img.get_height()/2 + 150, close_img, 1)

        if close_button.draw(win):
            main_menu(win)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

        pygame.display.update()

def highscore_menu(win):
    """
    the appearance of high score menu
    """
    run = True
    while run:
        win.fill((0,0,0))

        font = pygame.font.SysFont('comicsans', 100)
        label = font.render("High scores", 1, (255,255,255))

        win.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 10))

        # connect to database
        conn = sqlite3.connect('highscore.db')
        # create a cusor
        c = conn.cursor()

        # order by score
        c.execute("SELECT * from Player ORDER BY score DESC LIMIT 10")

        players = c.fetchall()

        distance = 200
        ranking = 0
        for player in players:
            ranking += 1
            font = pygame.font.SysFont('comicsans', 30)
            label = font.render(f'Rank {ranking}: {player[0]} - {player[1]}', 1, (255,255,255))
            sx = s_width/2 - label.get_width()/2
            sy = s_height/2 - distance
            win.blit(label, (sx, sy))
            distance -= 50

        # commit the command
        conn.commit()
        # close the connection
        conn.close()

        # recreate the exit button
        close_button = button.Button(s_width/2 - close_img.get_width()/2, s_height/2 - close_img.get_height()/2 + 320, close_img, 1)

        if close_button.draw(win):
            main_menu(win)

        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

        pygame.display.update()

main_menu(win)  # start game