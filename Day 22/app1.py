lines = None
with open("Day 22\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

class Vector2:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return str(self.x) + ", " + str(self.y)

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        else:
            return False

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

def split_route(line):
    route = []
    num = ""
    for char in line:
        if char.isdigit():
            num += char
        else:
            route.append(int(num))
            route.append(char)
            num = ""
    if num != "":
        route.append(int(num))
    return route

world = {}
spawn = None
route = None

readingWorld = True
for y, line in enumerate(lines):
    if readingWorld:
        if line == "":
            readingWorld = False
        else:
            for x, c in enumerate(line):
                if c != " ":
                    pos = Vector2(x, y)
                    world[pos] = c
                    if spawn == None and y == 0 and c == ".":
                        spawn = pos
    else:
        route = split_route(line)


#1,0 is right
#0,1 is down


turtle = Vector2(spawn.x, spawn.y)
facing = Vector2(1, 0)

for step in route:
    
    if isinstance(step, int):
        #move in facing direction step times
        #if hit wall, stop
        #if hit edge, wrap
        for i in range(0, step):
            infront = turtle + facing

            if not infront in world:
                infront -= facing
                while infront in world:
                    infront -= facing
                infront += facing

            if world[infront] == "#":
                break
            else:
                turtle = infront

    else:
        if facing == Vector2(1, 0):
            facing = Vector2(0, 1) if step == "R" else Vector2(0, -1)
        elif facing == Vector2(0, 1):
            facing = Vector2(-1, 0) if step == "R" else Vector2(1, 0)
        elif facing == Vector2(-1, 0):
            facing = Vector2(0, -1) if step == "R" else Vector2(0, 1)
        elif facing == Vector2(0, -1):
            facing = Vector2(1, 0) if step == "R" else Vector2(-1, 0)

col = turtle.x + 1
row = turtle.y + 1

dir = None
if facing == Vector2(1, 0):
    dir = 0
if facing == Vector2(0, 1):
    dir = 1
if facing == Vector2(-1, 0):
    dir = 2
if facing == Vector2(0, -1):
    dir = 3

print(1000 * row + 4 * col + dir)