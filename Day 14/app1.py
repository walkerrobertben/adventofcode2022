lines = None
with open("Day 14\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

class _V2:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

v2s = {}

def V2(x, y):
    k = str(x) + "," + str(y)
    if not k in v2s:
        v2s[k] = _V2(x, y)
    return v2s[k]


world = {}

AIR  = "."
ROCK = "#"
SAND = "O"

world[V2(500,0)] = "+"

for line in lines:

    positions = line.split(" -> ")
    
    p1 = positions.pop(0)
    for p2 in positions:
        p1s = p1.split(",")
        p2s = p2.split(",")
        v1 = V2(int(p1s[0]), int(p1s[1]))
        v2 = V2(int(p2s[0]), int(p2s[1]))

        if v1.x == v2.x:
            x = v1.x
            y1 = min(v1.y, v2.y)
            y2 = max(v1.y, v2.y)
            for y in range(y1, y2+1):
                world[V2(x, y)] = ROCK

        elif v1.y == v2.y:
            y = v1.y
            x1 = min(v1.x, v2.x)
            x2 = max(v1.x, v2.x)
            for x in range(x1, x2+1):
                world[V2(x, y)] = ROCK

        p1 = p2

def printWorld():

    minX = None
    maxX = None
    minY = None
    maxY = None

    for v2 in world.keys():
        if minX == None or v2.x < minX: minX = v2.x
        if maxX == None or v2.x > maxX: maxX = v2.x
        if minY == None or v2.y < minY: minY = v2.y
        if maxY == None or v2.y > maxY: maxY = v2.y

    for y in range(minY, maxY+1):
        line = ""
        for x in range(minX, maxX+1):
            v2 = V2(x, y)
            if v2 in world:
                line += world[v2]
            else:
                line += AIR
        print(line)

def dropSand():

    lowestPoint = None
    for v2 in world.keys():
        if lowestPoint == None or v2.y > lowestPoint:
            lowestPoint = v2.y

    sand = V2(500, 0)

    while True:

        moved = False

        check = [
            V2(sand.x, sand.y + 1),
            V2(sand.x - 1, sand.y + 1),
            V2(sand.x + 1, sand.y + 1)
        ]
        
        for move in check:
            if not move in world:
                sand = move
                moved = True
                break

        if moved == False: #this sand has come to rest
            world[sand] = SAND
            return True

        elif sand.y > lowestPoint: #this sand has fell
            return False




printWorld()

drops = 0
dropAnother = True
while dropAnother:
    dropAnother = dropSand()
    drops += 1

print(drops-1)
printWorld()