from const import *
import pygame

def num_to_color(num):
    if num == 0: # space
        return WHITE
    elif num == 1: # wall
        return BLACK
    elif num == 2: # start
        return GREEN
    elif num == 3: # target
        return RED
    elif num == 4: # path
        return BLUE
    elif num == 5: # visited
        return GRAY
    elif num == 6: # current
        return DARK_GRAY
    else:
        return WHITE
    
def get_mouse_pos():
    pos = pygame.mouse.get_pos()
    x = pos[0]//NODE_SIZE
    y = pos[1]//NODE_SIZE
    return x,y

def check_if_in_bounds(x, y):
    if x >= 0 and x < NUM_OF_ELEMENTS and y >= 0 and y < NUM_OF_ELEMENTS:
        return True
    else:
        return False

def check_if_space(board,x, y):
    if board[y][x] == 0:
        return True
    else:
        return False

def check_if_target(board,x, y):
    if check_if_in_bounds(x, y) and board[y][x] == 3:
        return True
    else:
        return False

def queue_is_not_empty(queue):
    if len(queue) > 0:
        return True
    else:
        return False