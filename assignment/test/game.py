import pygame
import random
from menu import *


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = 'comicsans'
        #self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        self.locked_positions = {}
        self.grid = self.create_grid(self.locked_positions)
        self.game_paused = False
        self.clock = pygame.time.Clock()
        self.change_piece = False
        self.game_mode = 'normal'
        self.current_piece = self.get_shape(self.game_mode)
        self.next_piece = self.get_shape(self.game_mode)
        self.fall_time = 0
        self.fall_speed = 0.25 # how long it take for a piece to move 1 row down
        self.level_time = 0
        self.score = 0
        self.inc = 0
        self.level = 1

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing= False
            self.display.fill(self.BLACK)
            # self.draw_text('Thanks for Playing', 20, self.DISPLAY_W/2, self.DISPLAY_H/2)
            self.window.blit(self.display, (0,0))

            # create the grid based on locked_positions
            grid = self.create_grid(self.locked_positions)
            
            # while game_paused == False, increment time as usual, of not, time stops
            if self.game_paused == False:
                fall_time += self.clock.get_rawtime() # gradually increase fall_time
                level_time += self.clock.get_rawtime() # gradually increase level_time
                self.clock.tick()

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
                pygame.display.update()
                self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.SysFont(self.font_name,size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

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
    
    def get_shape(game_mode):
        """
        function to get a random Piece (shape)
        """
        if game_mode == 'normal':
            return Piece(5, 0, random.choice(shapes[0:7]))
        if game_mode == 'extended':
            return Piece(5, 0, random.choice(shapes))

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