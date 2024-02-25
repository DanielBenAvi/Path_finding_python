from queue import PriorityQueue
import pygame
from const import BLACK, BLANK_SPACE, BLUE, BORDER_COLOR, DARK_GRAY, GRAY, GREEN, NODE_SIZE, NUM_OF_ELEMENTS, RED, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE
from Node import Node
from button import My_Button
from help_fn import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH ,SCREEN_HEIGHT + 2*BLANK_SPACE))
pygame.display.set_caption("Pathfinding Visualizer")
clock = pygame.time.Clock()
running = True

# game setup
board = [[0 for i in range(NUM_OF_ELEMENTS)] for j in range(NUM_OF_ELEMENTS)]   
        

flag_start = False  # start flag for drawing the start node
flag_target = False  # target flag for drawing the target node
run_bfs = False
run_dfs = False
run_best_first = False
find_path = False
target_x:int
target_y:int
target:Node
bfs_queue:list[Node] = []
dfs_stack:list[Node] = []
best_first_queue = PriorityQueue()

  
def draw_board(screen, board):
    for i in range(NUM_OF_ELEMENTS):
        for j in range(NUM_OF_ELEMENTS):
            # draw node
            pygame.draw.rect(screen, num_to_color(board[j][i]), (i*NODE_SIZE, j*NODE_SIZE, NODE_SIZE, NODE_SIZE))
            # draw border
            pygame.draw.rect(screen, BORDER_COLOR, (i*NODE_SIZE, j*NODE_SIZE, NODE_SIZE, NODE_SIZE), 1)

def set_walls(board):
    x, y = get_mouse_pos()
    if check_if_in_bounds(x, y):
        if board[y][x] == 1:
            
            board[y][x] = 0
        else:
            board[y][x] = 1

def create_start(get_mouse_pos) -> bool:
    x, y = get_mouse_pos()
    global flag_start
    if not flag_start:
        board[y][x] = 2
        flag_start = True         
        # put the start node in the queue
        bfs_queue.append(Node(x, y))
        dfs_stack.append(Node(x, y))
        best_first_queue.put(Node(x, y))
        
    return flag_start

def create_target(get_mouse_pos) -> bool:
    x, y = get_mouse_pos()
    global flag_target
    if not flag_target:
        board[y][x] = 3
        global target_x
        global target_y
        target_x = x
        target_y = y
        flag_target = True
    return flag_target

def bfs_check_neighbor(x, y, parent):   
    if check_if_target(board, x, y):
        global run_bfs
        global find_path
        global target
        run_bfs = False
        find_path = True
        target = Node(x, y)
        target.set_parent(parent)
    
    
    if check_if_in_bounds(x, y) and check_if_space(board, x, y):
        node = Node(x, y)
        node.set_parent(parent)
        bfs_queue.append(node) # add to queue
        print(bfs_queue)
        board[y][x] = 6 # current

def best_first_check_neighbor(x, y, parent):
    if check_if_target(board, x, y):
        global run_best_first
        global find_path
        global target
        run_best_first = False
        find_path = True
        target = Node(x, y)
        target.set_parent(parent)
        
    if check_if_in_bounds(x, y) and check_if_space(board, x, y):
        node = Node(x, y)
        node.set_parent(parent)
        node.claculate_h(target_x, target_y)
        best_first_queue.put(node)
        

def dfs_check_neighbor(x, y, parent):
    if check_if_target(board, x, y):
        global run_dfs
        global find_path
        global target
        run_dfs = False
        find_path = True
        target = Node(x, y)
        target.set_parent(parent)
    
    if check_if_in_bounds(x, y) and check_if_space(board, x, y):
        node = Node(x, y)
        node.set_parent(parent)
        dfs_stack.insert(0, node) # add to stack
        print(dfs_stack)
        board[y][x] = 6 # current
    
    
def restore_path():
    current = target
    while current.parent != None:
        if board[current.y][current.x] != 2 and board[current.y][current.x] != 3:
            board[current.y][current.x] = 4 # path
        current = current.parent

def bfs():
    if queue_is_not_empty(bfs_queue):
        current_node = bfs_queue.pop(0)
        x = current_node.get_x()
        y = current_node.get_y()
        
        if board[y][x] != 2:
            board[y][x] = 5 # visited
        
        bfs_check_neighbor(x, y-1, current_node) # up
        bfs_check_neighbor(x, y+1, current_node) # down
        bfs_check_neighbor(x-1, y, current_node) # left
        bfs_check_neighbor(x+1, y, current_node) # right
    
def dfs():
    if queue_is_not_empty(dfs_stack):
        current_node = dfs_stack.pop()
        x = current_node.get_x()
        y = current_node.get_y()
        
        if board[y][x] != 2:
            board[y][x] = 5 # visited
            
        dfs_check_neighbor(x, y-1, current_node) # up
        dfs_check_neighbor(x, y+1, current_node)
        dfs_check_neighbor(x-1, y, current_node)
        dfs_check_neighbor(x+1, y, current_node)
        
def best_first():
    if not best_first_queue.empty():
        current_node = best_first_queue.get()
        x = current_node.get_x()
        y = current_node.get_y()
        
        if board[y][x] != 2:
            board[y][x] = 5 # visited
        
        best_first_check_neighbor(x, y-1, current_node) # up
        best_first_check_neighbor(x, y+1, current_node)
        best_first_check_neighbor(x-1, y, current_node)
        best_first_check_neighbor(x+1, y, current_node)
     
def reset_game():
    global flag_start
    global flag_target
    global run_bfs
    global run_dfs
    global find_path
    global bfs_queue
    global dfs_stack
    global board
    board = [[0 for i in range(NUM_OF_ELEMENTS)] for j in range(NUM_OF_ELEMENTS)]
    flag_start = False
    flag_target = False
    run_bfs = False
    run_dfs = False
    find_path = False
    
    bfs_queue = []
    dfs_stack = []
    
button_reset = My_Button("Reset", 1*BUTTON_SPACE, SCREEN_HEIGHT + BUTTON_SPACE, BUTTON_WIDTH, BUTTON_HEIGHT)
button_reset.set_callback(reset_game)

button_bfs = My_Button("BFS", 2*BUTTON_SPACE + BUTTON_WIDTH, SCREEN_HEIGHT + BUTTON_SPACE, BUTTON_WIDTH, BUTTON_HEIGHT)
button_bfs.set_callback(bfs)

button_dfs = My_Button("DFS", 3*BUTTON_SPACE + 2*BUTTON_WIDTH, SCREEN_HEIGHT + BUTTON_SPACE, BUTTON_WIDTH, BUTTON_HEIGHT)
button_dfs.set_callback(dfs)


button_best_first = My_Button("Best First", 4*BUTTON_SPACE + 3*BUTTON_WIDTH, SCREEN_HEIGHT + BUTTON_SPACE, BUTTON_WIDTH, BUTTON_HEIGHT)
button_best_first.set_callback(best_first)


button_astar = My_Button("A*", 5*BUTTON_SPACE + 4*BUTTON_WIDTH, SCREEN_HEIGHT + BUTTON_SPACE, BUTTON_WIDTH, BUTTON_HEIGHT)
# button_astar.set_callback(astar)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                flag_start = create_start(get_mouse_pos)
            if event.key == pygame.K_t:
                flag_target = create_target(get_mouse_pos)
            if event.key == pygame.K_w:
                set_walls(board)

        if button_reset.is_mouse_over():
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Button clicked")
                button_reset.on_click()
        
        if button_bfs.is_mouse_over():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flag_start and flag_target:
                    run_bfs = True
                    
        if button_dfs.is_mouse_over():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flag_start and flag_target:
                    run_dfs = True
            
        if button_best_first.is_mouse_over():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if flag_start and flag_target:
                    run_best_first = True
        
    if flag_start and flag_target:
        if run_bfs: bfs()
        if run_dfs: dfs()
        if run_best_first: best_first()
        
        
    if find_path:
        restore_path()
        pass

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(BLACK)

    button_reset.draw(screen)
    button_bfs.draw(screen)
    button_dfs.draw(screen)
    button_best_first.draw(screen)
    button_astar.draw(screen)
    
    # RENDER YOUR GAME HERE
    draw_board(screen, board)
    
    
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()