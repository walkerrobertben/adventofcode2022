lines = None
with open("Day 22\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

class Vector2:
    def __init__(self, x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

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

def mapr(x, amin, amax, bmin, bmax):
    return int(bmin + (bmax - bmin) * (x - amin) / (amax - amin))

def wrap_infront(infront, facing):
    if facing == Vector2(1, 0):
        if infront.y >= 0 and infront.y <= 49:
            infront = Vector2(
                99,
                mapr(infront.y, 0, 49, 149, 100)
            )
            facing = Vector2(-1, 0)
        elif infront.y >= 50 and infront.y <= 99:
            infront = Vector2(
                mapr(infront.y, 50, 99, 100, 149),
                49
            )
            facing = Vector2(0, -1)
        elif infront.y >= 100 and infront.y <= 149:
            infront = Vector2(
                149,
                mapr(infront.y, 100, 149, 49, 0)
            )
            facing = Vector2(-1, 0)
        elif infront.y >= 150 and infront.y <= 199:
            infront = Vector2(
                mapr(infront.y, 150, 199, 50, 99),
                149
            )
            facing = Vector2(0, -1)

    elif facing == Vector2(0, 1):
        if infront.x >= 0 and infront.x <= 49:
            infront = Vector2(
                mapr(infront.x, 0, 49, 100, 149),
                0
            )
            facing = Vector2(0, 1)
        elif infront.x >= 50 and infront.x <= 99:
            infront = Vector2(
                49,
                mapr(infront.x, 50, 99, 150, 199),
            )
            facing = Vector2(-1, 0)
        elif infront.x >= 100 and infront.x <= 149:
            infront = Vector2(
                99,
                mapr(infront.x, 100, 149, 50, 99),
            )
            facing = Vector2(-1, 0)

    elif facing == Vector2(-1, 0):
        if infront.y >= 0 and infront.y <= 49:
            infront = Vector2(
                0,
                mapr(infront.y, 0, 49, 149, 100),
            )
            facing = Vector2(1, 0)
        elif infront.y >= 50 and infront.y <= 99:
            infront = Vector2(
                mapr(infront.y, 50, 99, 0, 49),
                100
            )
            facing = Vector2(0, 1)
        elif infront.y >= 100 and infront.y <= 149:
            infront = Vector2(
                50,
                mapr(infront.y, 100, 149, 49, 0)
            )
            facing = Vector2(1, 0)
        elif infront.y >= 150 and infront.y <= 199:
            infront = Vector2(
                mapr(infront.y, 150, 199, 50, 99),
                0
            )
            facing = Vector2(0, 1)

    elif facing == Vector2(0, -1):
        if infront.x >= 0 and infront.x <= 49:
            infront = Vector2(
                50,
                mapr(infront.x, 0, 49, 50, 99),
            )
            facing = Vector2(1, 0)
        elif infront.x >= 50 and infront.x <= 99:
            infront = Vector2(
                0,
                mapr(infront.x, 50, 99, 150, 199),
            )
            facing = Vector2(1, 0)
        elif infront.x >= 100 and infront.x <= 149:
            infront = Vector2(
                mapr(infront.x, 100, 149, 0, 49),
                199
            )
            facing = Vector2(0, -1)

    return (infront, facing)

turtle = Vector2(spawn.x, spawn.y)
facing = Vector2(1, 0)

for step in route:
    
    if isinstance(step, int):
        #move in facing direction step times
        #if hit wall, stop
        #if hit edge, wrap
        for i in range(0, step):
            
            infront = turtle + facing

            if infront in world: #move along face
                if world[infront] == "#":
                    break
                else:
                    turtle = infront

            else: #wrap around cube
                wrapped_infront, wrapped_facing = wrap_infront(infront, facing)

                if world[wrapped_infront] == "#":
                    break
                else:
                    turtle = wrapped_infront
                    facing = wrapped_facing

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