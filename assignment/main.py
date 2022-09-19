import pygame
import random

# import button.py
import button

# import tkinter to display popup dialog box
from tkinter import messagebox
import tkinter as tk
root = tk.Tk()
root.withdraw() # to remove the tk root window

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
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
    '......',
    '..00..',
    '.00...',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '...0.',
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
    '...0.',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '..00.',
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
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '..0..',
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

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

# create the class for tetris pieces
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

# function to create the grid (gived locked position as a library)
def create_grid(locked_positions = {}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)] # for starter, all grid "elements" are black squares

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c

    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + 80 - label.get_height()/2))

def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx + play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128,128,128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))

def clear_rows(grid, locked):
    inc = 0 # to count how many row do we need to move "the above rows" down
    for i in range(len(grid)-1, -1,  -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def draw_next_shape(shape, surface):
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


def update_score(nscore):
    with open('scores.txt', 'r') as f:
        scores = f.readlines()
        scores.append(str(nscore) + "\n")
        scores = sorted(scores, key=int, reverse=True)
        scores = scores[0:10]

    with open('scores.txt', 'w') as f:
        for score in scores:
            f.write(str(score))

def draw_window(surface, grid, score=0, inc=0, level=1):
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
    locked_positions = {}
    grid = create_grid(locked_positions)
    print(grid)
    game_paused = False
    
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.25
    level_time = 0
    score = 0
    inc = 0
    level = 1

    while run:
        grid = create_grid(locked_positions)
        
        if game_paused == False:
            fall_time += clock.get_rawtime() # gradually increase fall_time
            level_time += clock.get_rawtime() # gradually increase level_time
            clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            level += 1
            if fall_speed > 0.12: # min speed is going to be 0.12
                fall_speed -= 0.005 # took 1m40s before hitting fall_speed = 0.12

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_p:
                    game_paused = not game_paused
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
                    draw_text_middle("Paused", 120, (255,255,255), win)
                    pygame.display.update()
                    response = messagebox.askyesno("Confirmation", "U sure you wanna quit?")
                    if response == True:
                        run = False
                        pygame.display.quit()
                    if response == False:
                        game_paused = not game_paused

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            # only clear_rows when the previous piece hits the ground (when change_piece)
            if clear_rows(grid, locked_positions) == 1:
                score += 100
            elif clear_rows(grid, locked_positions) == 2:
                score += 300
            elif clear_rows(grid, locked_positions) == 3:
                score += 600
            elif clear_rows(grid, locked_positions) == 4:
                score += 1000
            inc += clear_rows(grid, locked_positions)

        draw_window(win, grid, score, inc, level)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if game_paused == True:
            draw_text_middle("Paused", 120, (255,255,255), win)
            pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle('You lost', 80, (255,255,255), win)
            pygame.display.update()
            pygame.time.delay(1500)
            update_score(score)
            run = False

# def yes_or_no(win):
#     run = True
#     while run:
#         win.fill((0,0,0))
#         draw_text_middle("You sure you want to quit?", 60, (255,255,255), win)

#         if yes_button.draw(win):
#             run = False
#             pygame.display.quit()
#         if no_button.draw(win):
#             main(win)

#         # event handler
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.display.quit()
        
#         pygame.display.update()

def main_menu(win):
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

    with open('scores.txt', 'r') as f:
        scores = f.readlines()

    run = True
    while run:
        win.fill((0,0,0))

        font = pygame.font.SysFont('comicsans', 100)
        label = font.render("High scores", 1, (255,255,255))

        win.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), 10))

        # draw highscore #1
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(scores[0].strip(), 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 - 200
        win.blit(label, (sx, sy))

        # draw highscore #2
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(scores[1].strip(), 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 - 150
        win.blit(label, (sx, sy))

        # draw highscore #3
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(scores[2].strip(), 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 - 100
        win.blit(label, (sx, sy))

        # draw highscore #4
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(scores[3].strip(), 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 - 50
        win.blit(label, (sx, sy))

        # draw highscore #5
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(scores[4].strip(), 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2
        win.blit(label, (sx, sy))

        # draw highscore #6
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(scores[5].strip(), 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 + 50
        win.blit(label, (sx, sy))

        # draw highscore #7
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(scores[6].strip(), 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 + 100
        win.blit(label, (sx, sy))

        # draw highscore #8
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(scores[7].strip(), 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 + 150
        win.blit(label, (sx, sy))

        # draw highscore #9
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(scores[8].strip(), 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 + 200
        win.blit(label, (sx, sy))

        # draw highscore #10
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render(scores[9].strip(), 1, (255,255,255))
        sx = s_width/2 - label.get_width()/2
        sy = s_height/2 + 250
        win.blit(label, (sx, sy))

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

# def pause_menu(win):
#     run = True
#     game_paused = False
#     while run:
#         win.fill((0,0,0))
#         # draw_text_middle("Press anything to start", 60, (255,255,255), win)

#         click = False

#         if game_paused == True:
#             if resume_button.draw(win):
#                 game_paused = False
#             if exit_button.draw(win):
#                 run = False
#         else:
#             pass # run the game like normal

#         # event handler
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     game_paused = True
#             if event.type == pygame.QUIT:
#                 run = False
#                 pygame.display.quit()
#         pygame.display.update()

#     main(win)

main_menu(win)  # start game