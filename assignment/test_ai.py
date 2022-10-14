import pygame
import copy

class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key

counter = 0
def run_ai(current_piece, grid, locked_positions):
    global counter
    counter += 1
    if counter < 50:
        return []
    counter = 0

    sim_locked_positions = copy.deepcopy(locked_positions)
    sim_grid = copy.deepcopy(grid)
    sim_current_piece = copy.deepcopy(current_piece)

    best_rotation, best_position = best_rotation_position(sim_current_piece, sim_grid, sim_locked_positions)
    # print(best_position)

    if current_piece.rotation != best_rotation:
        e = Event(pygame.KEYDOWN, pygame.K_UP)
    elif current_piece.x < best_position:
        e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    elif current_piece.x > best_position:
        e = Event(pygame.KEYDOWN, pygame.K_LEFT)
    else:
        e = Event(pygame.KEYDOWN, pygame.K_SPACE)
    return [e]

def best_rotation_position(sim_current_piece, sim_grid, sim_locked_positions):
    best_height = 20
    best_holes = 20*10
    best_position = None
    best_rotation = None

    for rotation in range(len(sim_current_piece.shape)):
        sim_current_piece.rotaion = rotation
        for j in range(0, 10):
            holes, height = simulate(sim_current_piece, j, sim_grid, sim_locked_positions)
            # print(height)
            # this is where we will set the condition for what is considered "best"
            # if best_position is None or best_holes > holes or best_holes == holes and best_height < height:
            if height < best_height:
                best_height = height
                best_holes = holes
                best_position = j
                best_rotation = rotation

    return best_rotation, best_position

def simulate(sim_current_piece, j, sim_grid, sim_locked_positions):
    '''
    function to simulate a piece at location x,y, and return the holes and height of the current "tower"
    x: parameter passed in to simulate dropping the piece at which column (horizontally 0-9)
    '''

    # # move sim_current_piece to the passed-in x position
    # while sim_current_piece.x != j:
    #     if sim_current_piece.x < j:
    #         sim_current_piece.x += 1
    #     elif sim_current_piece.x > j:
    #         sim_current_piece.x -= 1
    
    sim_current_piece.x = j

    # while still in valid_space, increase y value of a piece by 1
    while valid_space(sim_current_piece, sim_grid):
        sim_current_piece.y += 1
    # when the piece is no longer in valid_space:
    if not(valid_space(sim_current_piece, sim_grid)) and sim_current_piece.y > 0:
        sim_current_piece.y -= 1

        # convert the current piece into a list of locations
        sim_shape_pos = convert_shape_format(sim_current_piece)
        # # loop through all the pos of the blocks of the shapes, if it's in the play area, change the color accordingly (update the grid)
        # for i in range(len(shape_pos)):
        #     x, y = shape_pos[i]
        #     if y > -1: # we're not above the play area
        #         sim_grid[y][x] = sim_current_piece.color

        clone = copy.deepcopy(sim_locked_positions)

        # update sim_locked_positions, sim_locked_positions is a dict like this: {(1,2), (255,255,255)}, whereas the key is the location, value is the color
        for pos in sim_shape_pos:
            p = (pos[0], pos[1])
            clone[p] = sim_current_piece.color


    height = 0
    holes = 0
    for i in range(len(sim_grid)-1, -1, -1): # loop through all rows, from 19 to 0 (bottom up)
        for j in range(len(sim_grid[i])): # loop through all column of that row 0-9, len(grid[i]) == 10
            if (j, i) in clone:
                height = len(sim_grid) - i
                # print(f'height: {height}')
            if (j, i) not in clone and (j, i-1) in clone:
                holes += 1
                # print(f'holes: {holes}')
    # print(height)
    return holes, height

def convert_shape_format(shape):
    """
    function to convert from a passed-in shape object to an actual shape
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
    """
    # loop through all the possible positions, only add in accepted_pos if the colour is black (0,0,0)
    # accepted_pos is a list of sublists: [ [(1,1)], [(2,2)] ]
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    # this line convert the list of sublists into a list of tuples: [ (1,1), (2,2) ]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    # convert the passed-in shape into the same format as accepted_pos for comparison [ (1,1), (2,2) ], this is a list of blocks that create the shape
    formatted = convert_shape_format(shape)

    # loop through all the blocks (pos) of the shape (formatted)
    for pos in formatted:
        # if any of the blocks (pos) of the shape is not in accepted_pos
        if pos not in accepted_pos:
            # if the x value (current horizontal pos) of the 1st block (left most block) of  shape is > -1, aka the shape is in the play area
            if pos[1] > -1:
                # then return false, aka the shape is in valid space
                return False
    return True