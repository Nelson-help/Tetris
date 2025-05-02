from Game import Board
from copy import deepcopy
from Cost import costFunctions
import random 
import json
import os

class Player(Board):
    moves: list
    weights: list

    def __init__(self, w, h, weights):
        self.moves = []
        self.weights = weights
        super().__init__(w, h)

class TetrisAI:
    def getFuture(self, x, state, tile): # "Left-most block in tile"'s x coord
        simulator = Board(len(state[0]), len(state))
        simulator.loadedTiles[0] = tile
        simulator.board = state
        simulator.cursor_x = x
        simulator.drop() # Cursor is on the newest block, so sim = latest block
        return simulator.board

    def Think(self, cursor_x, state, cur_tile=None, hold=None, weights=[]):
        bestMove = []
        bestCost = float("inf")

        starting = [
            (cur_tile, []),
            (hold, ["HD"])
        ]    
        for tile, moves in starting:
            if tile is None or tile == "": continue
            for rotate in range(4):
                for x in range(-tile.offsetL, len(state[0]) + tile.offsetR - tile.size + 1): # +1 Cuz range exclude last, x is the cursor_x for each pos. sim.
                    cost = 0
                    future = self.getFuture(x, deepcopy(state), tile)
                    for i in range(len(costFunctions)):
                        cost += costFunctions[i](future) * weights[i]
                    if cost < bestCost:
                        bestCost = cost
                        if x == cursor_x: bestMove= moves + ["RR"]*rotate
                        elif x > cursor_x: bestMove= moves + ["RR"]*rotate + ["MR"]*(x - cursor_x)
                        elif x < cursor_x: bestMove= moves + ["RR"]*rotate + ["ML"]*(cursor_x - x)
                tile.rotate(+1)
        return bestMove + ["DP", ]


    
class Trainer:
    mutateRate = 0.1 # 越小 -> 訓練較慢但更精準 ， 越大 -> 訓練更快但偏差大

    path = "best.json"

    def __init__(self, population):
        if os.path.exists(self.path): # Does it exist
            with open(self.pat, "r") as f:
                initWeight = json.load(f) # Load in previous weight
            assert len(initWeight) == len(costFunctions)
        else:
            initWeight = [1]*len(costFunctions)
        self.population = population # 16
        self.initWeight = initWeight
        self.bestWeight = initWeight
        self.bestFitness = 0 # score
        self.generations = 0

    def initializePlayers(self, **kwargs): 
        players = [Player(**kwargs, weights=self.initWeight), ] # kwargs = keyboard arguments
        for i in range(self.population - 1):
            weights = [n*(random.randint(50, 150)/100) for n in self.initWeight]
            players.append(Player(**kwargs, weights=weights))
        return players


    def mutate(self, weights):
        newWeights = []
        for i in range(len(weights)):
            if(random.random() < self.mutateRate): # Chance to mutate
                newWeights.append(weights[i] * (random.randint(95,105)/100))
            else:
                newWeights.append(weights[i])
        return newWeights


    def naturalSelection(self, players):
        bestPlayerIndex = 0
        for i in range(len(players)):
            if(players[i].score > players[bestPlayerIndex].score):
                bestPlayerIndex = i

        newPlayers = [players.pop(bestPlayerIndex), ]

        for p in players: # population - 1
            p.weights = self.mutate(newPlayers[0].weights)
            newPlayers.append(p)

        self.generations += 1

        with open(self.path, "w") as f:
            json.dump(newPlayers[0].weights, f)

        text = ""
        text += f"\nGeneration {self.generations}"
        text += f"\n- Best Score {newPlayers[0].score}"
        text += f"\n- Best Weights {newPlayers[0].weights}"
        print(text)

        return newPlayers
