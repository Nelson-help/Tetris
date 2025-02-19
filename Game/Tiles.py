from copy import deepcopy # Copy = same object (linked), deepcopy = same object (unlinked)

class Tile:
    color:str

    def __init__(self) -> None:
        self.rotation = 0
        self.name = self._name # Underscore means private
        self.w, self.h = self._w, self._h # Later while rendering, only see in the range of w and h => less processing
        self.size = self._size
        self.mass = deepcopy(self._mass) # Copy the mass array to avoid modify the original
        self.setOffset()

    def setOffset(self): # Skip n rows in x direction to render less
        self.offsetT = self.size 
        self.offsetD = self.size
        self.offsetL = self.size
        self.offsetR = self.size
        for i in range(self.size):
            for j in range(self.size):
                if not self.mass[i][j]: continue # If mass at (i, j) is 0 => skip
                self.offsetT = min(self.offsetT, i) # Replace offset until reach block
                self.offsetD = min(self.offsetD, self.size - i - 1)
                self.offsetL = min(self.offsetL, j)
                self.offsetR = min(self.offsetR, self.size - j - 1)

    def rotateL(self):
        self.rotation = (self.rotation - 1 + 4) % 4 # Rotate value
        new_mass = deepcopy(self.mass)
        self.w, self.h = self.h, self.w # Swap current w and h
        for i in range(self.size):
            for j in range(self.size):
                new_mass[i][j] = self.mass[j][self.size - i - 1] # Discovered pattern
        self.mass = new_mass
        self.setOffset()
    
    def rotateR(self):
        for i in range(3):
            self.rotateL()
    
    def rotate(self, direction: int):
        if direction == -1:
            self.rotateL()
        elif direction == 1:
            self.rotateR()

    def clone(self):
        new = self.__class__()
        new.mass = deepcopy(self.mass)
        new.w, new.h, new.size = self.w, self.h, self.size
        new.setOffset()
        return new

class Tile_I(Tile):
    _name = "I"
    _w, _h = 4, 1
    _size = 4 # Rotation centre is on grid line, but we dont draw, so OK, size means the smallest square that can fit shape
    _mass = [ # Actual shape
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    color = "#00F0F0"

class Tile_J(Tile):
    _name = "J"
    _w, _h = 2, 3
    _size = 3
    _mass = [ 
        [0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]
    ]
    color = "#0000F0"

class Tile_L(Tile):
    _name = "L"
    _w, _h = 2, 3
    _size = 3
    _mass = [ 
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 1]
    ]
    color = "#F0A100"

class Tile_O(Tile):
    _name = "O"
    _w, _h = 2, 2
    _size = 2 
    _mass = [ 
        [1, 1],
        [1, 1]
    ]
    color = "#F8F87C"

class Tile_S(Tile):
    _name = "S"
    _w, _h = 3, 2
    _size = 3
    _mass = [ 
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ]
    color = "#00F000"

class Tile_T(Tile):
    _name = "T"
    _w, _h = 3, 3
    _size = 3
    _mass = [ 
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]
    color = "#A100F0"

class Tile_Z(Tile):
    _name = "Z"
    _w, _h = 3, 2
    _size = 3
    _mass = [ 
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]
    color = "#D90000"

ALL = [
    Tile_I,
    Tile_J,
    Tile_L,
    Tile_O,
    Tile_S,
    Tile_T,
    Tile_Z,  # All tiles are stored here
]
