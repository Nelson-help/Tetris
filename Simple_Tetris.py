import pygame
pygame.init()

import Game

FPS = 7

BOARD_COLS = 10
BOARD_ROWS = 20
BLOCK_SIZE = 30
BORDER_WIDTH = max(1, int(BLOCK_SIZE/30))

BG_COLOR = "#98E5D9"
GRID_COLOR = "#FFFFFF"

"""
1. 
First set WINDOW_WIDTH, WINDOW_HEIGHT
then calc BOARD_COLS, BOARD_ROWS

2. 
First set BOARD_COLS, BOARD_ROWS, BLOCK_SIZE
then calc WINDOW_WIDTH, WINDOW_HEIGHT
"""

WINDOW_WIDTH = BOARD_COLS * BLOCK_SIZE + BORDER_WIDTH * (BOARD_COLS - 1)
WINDOW_HEIGHT = BOARD_ROWS * BLOCK_SIZE + BORDER_WIDTH * (BOARD_ROWS - 1)

running = True

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

board = Game.Board(BOARD_COLS, BOARD_ROWS)

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

    if pressed[pygame.K_DOWN] or pressed[pygame.K_s]:
        board.fall()
    if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
        board.move(-1)
    if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
        board.move(+1)
    if pressed[pygame.K_UP] or pressed[pygame.K_x]:
        board.rotate(+1)
    if pressed[pygame.K_RCTRL] or pressed[pygame.K_z]:
        board.rotate(-1)
    if pressed[pygame.K_RSHIFT] or pressed[pygame.K_c]:
        board.hold()

    window.fill(GRID_COLOR)

    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board.board[i][j]: # 1st board is class, second board is list
                pygame.draw.rect(window, board.board[i][j], 
                                (j*(BLOCK_SIZE + BORDER_WIDTH), 
                                i*(BLOCK_SIZE + BORDER_WIDTH), 
                                BLOCK_SIZE - 2*BORDER_WIDTH, 
                                BLOCK_SIZE - 2*BORDER_WIDTH))
            else: 
                pygame.draw.rect(window, BG_COLOR, 
                                (j*(BLOCK_SIZE + BORDER_WIDTH), 
                                i*(BLOCK_SIZE + BORDER_WIDTH), 
                                BLOCK_SIZE - 2*BORDER_WIDTH, 
                                BLOCK_SIZE - 2*BORDER_WIDTH))
    
    for i in range(board.loadedTiles[0].size):
        for j in range(board.loadedTiles[0].size):
            if board.loadedTiles[0].mass[i][j] == 1:
                pygame.draw.rect(window, board.loadedTiles[0].color, 
                                    ((board.cursor_x + j)*(BLOCK_SIZE + BORDER_WIDTH), 
                                    (board.cursor_y + i)*(BLOCK_SIZE + BORDER_WIDTH), 
                                    BLOCK_SIZE - 2*BORDER_WIDTH, 
                                    BLOCK_SIZE - 2*BORDER_WIDTH))
    
    board.update()

    pygame.display.update()
    clock.tick(FPS)
