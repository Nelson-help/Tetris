def getHoleClusters(future): # No. of holes
    visited = [[False]*len(future[0]) for _ in range(len(future))]
    count = 0
    for i in range(len(future)):
        for j in range(len(future[i])):
            if visited[i][j]: continue
            visited[i][j] = True
            if not future[i][j]:
                count += 1
                pending = [(i, j), ]
                while pending:
                    y, x = pending.pop(0)
                    visited[y][x] = True
                    for dy, dx in [(1, 0), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if nx < len(future[0]) and ny < len(future):
                            if not visited[ny][nx] and not future[ny][nx]:
                                visited[ny][nx] = True
                                pending.append((ny, nx))
    return count - 1

def getPillarCount(future): # No. of empty columns (peak at one)
    count = 0
    for c in range(len(future[0])):
        if all(not row[c] for row in future):
            count += 1
    return -1 if count == 1 else count + (count == 0)

def getShapeHeight(future): # Max height
    count = len(future)
    for row in range(len(future)):
        if any(block for block in future[row]): # Only if block exists
            count = row
            break
    return len(future) - count

def getBumpiness(future): # Sum of differences
    heights = []
    for col in range(len(future[0])):
        y = len(future)
        for row in range(len(future)):
            if future[row][col]:
                y = row
                break
        heights.append(len(future) - y)
    count = 0
    for i in range(1, len(heights)):
        count += abs(heights[i]-heights[i-1])
    return count
    
def getFillCount(future): # No. tiles to fill to clear all
    index = len(future) # Max Height from top
    count = 0
    for row in range(len(future)):
        if any(block for block in future[row]) and index == len(future): # Only if block exists
            index = row
        for col in range(len(future[0])):
            if future[row][col]:
                count += 1
    return (len(future)-index)*len(future[0]) - count

def getBlockCountAboveHoles(future): # Blocks above hole 
    count = 0
    for row in range(len(future)):
        for col in range(len(future[0]) - 1):
            if row + 1 < len(future)and future[row][col] and not future[row + 1][col]:
                    count += 1
    return count

def getHolesDist(future): # Sum of roof to hole
    top = []
    bottom = []
    for col in range(len(future[0])):
        for row in range(len(future)):
            if future[row][col]:
                top.append(len(future) - row)
                break
        else:
            top.append(row)

        for row in range(len(future) - 1, -1, -1):
            if not future[row][col]:
                bottom.append(len(future) - row)
                break
        else:
            bottom.append(row)
    return sum(abs(top[i] - bottom[i]) if top[i] < bottom[i] else 0 for i in range(len(future[0]))) # Empty block can be higher

def getClearedCost(future): # No. of lines I can clear after added block
    count = 0
    for i in range(len(future)):
        if all(future[i]): count -= 1
    return count
            
costFunctions = [
    getHoleClusters,
    getPillarCount,
    getShapeHeight,
    getBumpiness,
    getFillCount,
    getBlockCountAboveHoles,
    getHolesDist,
    getClearedCost,
]
