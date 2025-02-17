import pygame
pygame.init()

import Game

FPS = 40

BOARD_COLS = 10
BOARD_ROWS = 20
BLOCK_SIZE = 40
BORDER_WIDTH = int(BLOCK_SIZE/30)

"""
1. 
First set WINDOW_WIDTH, WINDOW_HEIGHT
then calc BOARD_COLS, BOARD_ROWS

2. 
First set BOARD_COLS, BOARD_ROWS, BLOCK_SIZE
then calc WINDOW_WIDTH, WINDOW_HEIGHT
"""

WINDOW_WIDTH = BOARD_COLS*BLOCK_SIZE
WINDOW_HEIGHT = BOARD_ROWS*BLOCK_SIZE

running = True

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

board = Game.Board(BOARD_COLS, BOARD_ROWS)

cursor = [WINDOW_WIDTH - BLOCK_SIZE*2, 0]

direction = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                board.drop()
    if not running: break

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_DOWN]:
        board.fall()
    if pressed[pygame.K_LEFT]:
        board.move(-1)
    if pressed[pygame.K_RIGHT]:
        board.move(+1)
    if pressed[pygame.K_x]:
        board.rotate(+1)
    if pressed[pygame.K_z]:
        board.rotate(-1)
    if pressed[pygame.K_LSHIFT]:
        board.hold()

    window.fill("#98E5D9")

    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board.board[i][j]: # 1st board is class, second board is list
                pygame.draw.rect(window, board.board[i][j], 
                                (j*BLOCK_SIZE + BORDER_WIDTH, 
                                i*BLOCK_SIZE + BORDER_WIDTH, 
                                BLOCK_SIZE - 2*BORDER_WIDTH, 
                                BLOCK_SIZE - 2*BORDER_WIDTH))

    for i in range(1, BOARD_COLS): # Vertical grid lines
        pygame.draw.line(window, "#FFFFFF", 
                            (BLOCK_SIZE*i, 0), 
                            (BLOCK_SIZE*i, WINDOW_HEIGHT),
                            )
        
    for j in range(1, BOARD_ROWS): # Horizontal grid lines
        pygame.draw.line(window, "#FFFFFF", 
                            (0, BLOCK_SIZE*j), 
                            (WINDOW_WIDTH, BLOCK_SIZE*j),
                            )
    
    for i in range(board.loadedTiles[0].size):
        for j in range(board.loadedTiles[0].size):
            if board.loadedTiles[0].mass[i][j] == 1:
                pygame.draw.rect(window, board.loadedTiles[0].color, 
                                    ((board.cursor_x + j)*BLOCK_SIZE + BORDER_WIDTH, 
                                    (board.cursor_y + i)*BLOCK_SIZE + BORDER_WIDTH, 
                                    BLOCK_SIZE - 2*BORDER_WIDTH, 
                                    BLOCK_SIZE - 2*BORDER_WIDTH))
    
    board.update(1)

    pygame.display.update()
    clock.tick(FPS)
