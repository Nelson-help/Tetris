from . import Tiles # . => means this folder

from .Constants import FALL_DELAY, LOCK_DELAY

import random

class Board:
    def __init__(self, w:int, h:int, tileRandomizer=None) -> None: # Types of random tiles
        self.w = w
        self.h = h
        self.tileRandomizer = tileRandomizer
        self.reset()
        
    def reset(self) -> None:
        self.alive = True
        self.score = 0
        self.clearCount = 0

        self.board = [] # Empty board
        self.fillEmptyRows()
        
        self.loadedTiles = []
        self.fillPreloadTiles()

        self.fallCounter = 0
        self.lockCounter = 0

        self.heldTile = None

        self.cursor_x = 0
        self.cursor_y = 0

        self.cursor_x = int((self.w - self.loadedTiles[0].size)/2)
        self.cursor_y = 0 - self.loadedTiles[0].offsetT

        self.fillEmptyRows()

    def fillEmptyRows(self) -> None: # Create empty board
        for i in range(self.h - len(self.board)): # Needed rows - current rows
            self.board.insert(0, [""]*self.w)

    def fillPreloadTiles(self):
        if len(self.loadedTiles) < len(Tiles.ALL):
            a = [random.shuffle(Tiles.ALL)]
            self.loadedTiles.extend([tile() for tile in Tiles.ALL]) # Add rand sequence of tiles 

    def checkCollision(self, x:int, y:int, checkD:bool = True, checkL:bool = True, checkR:bool = True) -> bool:
        if checkD: 
            if y + self.loadedTiles[0].size - self.loadedTiles[0].offsetD > self.h: return True
        if checkL: 
            if x + self.loadedTiles[0].offsetL < 0: return True
        if checkR: 
            if x + self.loadedTiles[0].size - self.loadedTiles[0].offsetR > self.w: return True
        
        for xx in range(max(0, x), min(self.w, x + self.loadedTiles[0].size)): # Check if go into wall
            for yy in range(max(0, y), min(self.h, y + self.loadedTiles[0].size)):
                if self.board[yy][xx] and self.loadedTiles[0].mass[yy - y][xx - x]: # xx, yy = relative x, y
                    return True
        
        return False
    
    def checkClear(self):
        count = 0

        for i in range(len(self.board)-1, -1, -1):
            filled = True
            for j in range(self.w):
                if not self.board[i][j]:
                    filled = False
                    break
            
            if filled: 
                self.board.pop(i)
                count += 1
    
        self.clearCount += count
        self.score = self.clearCount
        self.fillEmptyRows()

    def lock(self, instant):
        self.lockCounter += 1
        if instant or self.lockCounter == LOCK_DELAY:
            self.lockCounter = 0

            for xx in range(max(0, self.cursor_x), min(self.w, self.cursor_x + self.loadedTiles[0].size)):
                for yy in range(max(0, self.cursor_y), min(self.h, self.cursor_y + self.loadedTiles[0].size)):
                    if self.loadedTiles[0].mass[yy - self.cursor_y][xx - self.cursor_x]: 
                        self.board[yy][xx] = self.loadedTiles[0].color
                
            self.loadedTiles.pop(0)
            self.fillPreloadTiles()
            self.checkClear()

            self.cursor_x = int((self.w - self.loadedTiles[0].size)/2)
            self.cursor_y = 0 - self.loadedTiles[0].offsetT

            if self.checkCollision(self.cursor_x, self.cursor_y, checkD=True, checkL=True, checkR=True): self.alive = False
    
    def fall(self):
        if self.checkCollision(self.cursor_x, self.cursor_y + 1, checkD = True, checkL = True, checkR = True): # Pretend go down
            return self.lock(instant = False)
        self.cursor_y += 1

    def drop(self):
        while not self.checkCollision(self.cursor_x, self.cursor_y + 1, checkD = True, checkL = True, checkR = True):
            self.cursor_y += 1
        self.lock(instant = True)

    def update(self):
        self.fallCounter += 1 # Time
        if self.fallCounter == FALL_DELAY: # Means time to fall
            self.fallCounter = 0
            self.fall()
        
    def move(self, direction: int):
        if not self.checkCollision(self.cursor_x + direction, self.cursor_y, checkD = True, checkL = True, checkR = True):
            self.cursor_x += direction
    
    def kick(self, direction: int):
        # No kick needed
        if not self.checkCollision(self.cursor_x, self.cursor_y):
            return True
        # Check down
        if not self.checkCollision(self.cursor_x, self.cursor_y+1):
            self.cursor_y += 1
            return True
        # Check opposite side of rotation
        if not self.checkCollision(self.cursor_x - direction, self.cursor_y):
            self.cursor_x -= direction
            return True
        # Check same side of rotation
        if not self.checkCollision(self.cursor_x + direction, self.cursor_y):
            self.cursor_x += direction
            return True
        return False # No kick needed

    def hold(self):
        if self.heldTile:
            self.loadedTiles[0], self.heldTile = self.heldTile, self.loadedTiles[0]
        else:
            self.heldTile = self.loadedTiles.pop(0)
        self.cursor_x = int((self.w - self.loadedTiles[0].size)/2)
        self.cursor_y = 0 - self.loadedTiles[0].offsetT
        
    def rotate(self, direction: int):
        self.loadedTiles[0].rotate(direction)
        if self.kick(direction): return
        self.loadedTiles[0].rotate(-direction) # If not possible, spin back
