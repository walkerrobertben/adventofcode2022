lines = None
with open("Day 12\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]


class Tile:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.elevation = 0
        self.pathValue = None
        
map = {}

start = None
end = None

def getKey(x, y):
    return "(" + str(x) + ", " + str(y) + ")"

def getAdjacent(x, y):
    adjacents = []
    for check in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
        [cx, cy] = check
        key = getKey(cx, cy)
        if key in map:
            adjacents.append(map[key])
    return adjacents

def canTraverse(tileFrom, tileTo):
    return tileTo.elevation <= tileFrom.elevation + 1

width = 0
height = 0

for y, line in enumerate(lines):
    height = y+1
    for x, point in enumerate(line):
        width = x+1

        tile = Tile()
        tile.x = x
        tile.y = y

        elevation = ord(point)

        if point == "S":
            start = tile
            elevation = ord("a")
        elif point == "E":
            end = tile
            elevation = ord("z")

        tile.elevation = elevation

        map[getKey(x, y)] = tile



end.pathValue = 0
search = [end]

while len(search) > 0:

    tile = search.pop(0)

    for adjacent in getAdjacent(tile.x, tile.y):
        if canTraverse(adjacent, tile):
            if adjacent.pathValue == None or adjacent.pathValue > tile.pathValue + 1:
                adjacent.pathValue = tile.pathValue + 1
                search.append(adjacent)


out = []
for y in range(0, height):
    row = []
    for x in range(0, width):
        row.append("-")
    out.append(row)

out[start.y][start.x] = "S"
out[end.y][end.x] = "E"

steps = 0

p = start
while p != end:

    next = None
    for adjacent in getAdjacent(p.x, p.y):
        if adjacent.pathValue != None and adjacent.pathValue < p.pathValue:
            if canTraverse(p, adjacent):
                if next == None or adjacent.pathValue < next.pathValue:
                    next = adjacent

    if p != start:
        if next.x > p.x:
            out[p.y][p.x] = ">"
        elif next.x < p.x:
            out[p.y][p.x] = "<"
        elif next.y > p.y:
            out[p.y][p.x] = "v"
        elif next.y < p.y:
            out[p.y][p.x] = "^"

    p = next

    steps += 1
    
for row in out:
    print("".join(row))

print(steps)