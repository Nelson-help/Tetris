import pygame
pygame.init()

import Game

import Brain

FPS = 10

BOARD_COLS = 10
BOARD_ROWS = 20
BLOCK_SIZE = 10
BORDER_WIDTH = 0.1

BG_COLOR = "#98E5D9"
GRID_COLOR = "#FFFFFF"
WINDOW_BG = "#111111"

BOARD_WIDTH = BOARD_COLS * BLOCK_SIZE + BORDER_WIDTH * (BOARD_COLS - 1)
BOARD_HEIGHT = BOARD_ROWS * BLOCK_SIZE + BORDER_WIDTH * (BOARD_ROWS - 1)

POPULATION_COLS = 12
POPULATION_ROWS = 4
POPULATION_GAP = 3

WINDOW_WIDTH = POPULATION_COLS * BOARD_WIDTH + POPULATION_GAP * (POPULATION_COLS - 1)
WINDOW_HEIGHT = POPULATION_ROWS * BOARD_HEIGHT + POPULATION_GAP * (POPULATION_ROWS - 1)

trainer = Brain.Trainer(POPULATION_ROWS*POPULATION_COLS, [1]*8) # Create a trainer for the population, [] = not written yet

players = trainer.initializePlayers(w=BOARD_COLS, h=BOARD_ROWS)

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

direction = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    if not running: break

    window.fill(WINDOW_BG)

    if all([not p.alive for p in players]):
        players = trainer.naturalSelection(players) # Override original
        for p in players: p.reset() # score, clearCount = 0, re-alive

    for i in range(POPULATION_ROWS):
        for j in range(POPULATION_COLS):
            playerIndex = POPULATION_COLS*i + j

            surf = DrawBoard(players[playerIndex])
            window.blit(surf, (j*(BOARD_WIDTH + POPULATION_GAP), i*(BOARD_HEIGHT + POPULATION_GAP)))

            if players[playerIndex].alive:
                if not players[playerIndex].moves:
                    players[playerIndex].moves = brain.TetrisAI().Think(
                        cursor_x = players[playerIndex].cursor_x,
                        state = players[playerIndex].board,
                        cur_tile = players[playerIndex].loadedTiles[0],
                        hold = players[playerIndex].heldTile
                        weights = players[playerIndex].weights
                        )
                move = players[playerIndex].moves.pop(0)

                if move == "ML": 
                    players[playerIndex].move(-1)
                if move == "MR":
                    players[playerIndex].move(1)
                if move == "RL":
                    players[playerIndex].rotate(-1)
                if move == "RR":
                    players[playerIndex].rotate(1)
                if move == "HD":
                    players[playerIndex].hold()
                if move == "DP":
                    players[playerIndex].drop()
                players[playerIndex].update()

    pygame.display.update()
    clock.tick(FPS)
