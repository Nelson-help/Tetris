import pygame
pygame.init()

import Game

FPS = 15

BOARD_COLS = 10
BOARD_ROWS = 20
BLOCK_SIZE = 10
BORDER_WIDTH = max(1, int(BLOCK_SIZE/30))

BG_COLOR = "#98E5D9"
GRID_COLOR = "#FFFFFF"
WINDOW_BG = "#111111"

BOARD_WIDTH = BOARD_COLS * BLOCK_SIZE + BORDER_WIDTH * (BOARD_COLS - 1)
BOARD_HEIGHT = BOARD_ROWS * BLOCK_SIZE + BORDER_WIDTH * (BOARD_ROWS - 1)

POPULATION_COLS = 4
POPULATION_ROWS = 4
POPULATION_GAP = 3*BORDER_WIDTH

WINDOW_WIDTH = POPULATION_COLS * BOARD_WIDTH + POPULATION_GAP * (POPULATION_COLS - 1)
WINDOW_HEIGHT = POPULATION_ROWS * BOARD_HEIGHT + POPULATION_GAP * (POPULATION_ROWS - 1)

def DrawBoard(b: Game.Board):
    surface = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))

    surface.fill(GRID_COLOR)

    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if b.board[i][j]: # 1st board is class, second board is list
                pygame.draw.rect(surface, b.board[i][j], 
                                (j*(BLOCK_SIZE + BORDER_WIDTH), 
                                i*(BLOCK_SIZE + BORDER_WIDTH), 
                                BLOCK_SIZE - 2*BORDER_WIDTH, 
                                BLOCK_SIZE - 2*BORDER_WIDTH))
            else: 
                pygame.draw.rect(surface, BG_COLOR, 
                                (j*(BLOCK_SIZE + BORDER_WIDTH), 
                                i*(BLOCK_SIZE + BORDER_WIDTH), 
                                BLOCK_SIZE - 2*BORDER_WIDTH, 
                                BLOCK_SIZE - 2*BORDER_WIDTH))
    
    for i in range(b.loadedTiles[0].size):
        for j in range(b.loadedTiles[0].size):
            if b.loadedTiles[0].mass[i][j] == 1:
                pygame.draw.rect(surface, b.loadedTiles[0].color, 
                                    ((b.cursor_x + j)*(BLOCK_SIZE + BORDER_WIDTH), 
                                    (b.cursor_y + i)*(BLOCK_SIZE + BORDER_WIDTH), 
                                    BLOCK_SIZE - 2*BORDER_WIDTH, 
                                    BLOCK_SIZE - 2*BORDER_WIDTH))
    
    return surface

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

    window.fill(WINDOW_BG)

    for i in range(POPULATION_ROWS):
        for j in range(POPULATION_COLS):
            surf = DrawBoard(board)
            window.blit(surf, (j*(BOARD_WIDTH + POPULATION_GAP), i*(BOARD_HEIGHT + POPULATION_GAP)))

    board.update()

    pygame.display.update()
    clock.tick(FPS)
