
def getHoleCount(future): # No. of holes
    return 0
def getPillarCount(future): # No. of empty columns (peak at one)
    return 0

def getShapeHeight(future): # Max height
    return 0

def getBumpiness(future): # Sum of differences
    return 0

def getFillCount(future): # No. tiles to fill to clear all
    return 0

def getBlockCountAboveHoles(future): # Blocks above hole 
    return 0

def getHolesDist(future): # Sum of roof to hole
    return 0

def getClearedCost(future): # No. of lines I can clear after added block
    count = 0
    for i in range(len(future)):
        if all(future[i]): count -= 1
    return count
            
costFunctions = [
    getHoleCount,
    getPillarCount,
    getShapeHeight,
    getBumpiness,
    getFillCount,
    getBlockCountAboveHoles,
    getHolesDist,
    getClearedCost,
]
