lines = None
with open("Day 17\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

jets = [*lines[0]]

WALL_LEFT = 0
WALL_RIGHT = 8
FLOOR = 0

shapes = (
    ("####", ),

    (" # ",
     "###",
     " # ", ),

    ("  #", 
     "  #",
     "###", ),

    ("#",
     "#", 
     "#", 
     "#", ),

     ("##",
      "##", ),
)

rocks = []

class View2D():

    def __init__(self, air):
        self.air = air
        self.values = {}
        self.minx = None
        self.maxx = None
        self.miny = None
        self.maxy = None

    def key(self, x, y):
        return str(x) + ":" + str(y)

    def set(self, x, y, v):
        self.minx = x if self.minx is None else min(self.minx, x)
        self.maxx = x if self.maxx is None else max(self.maxx, x)
        self.miny = y if self.miny is None else min(self.miny, y)
        self.maxy = y if self.maxy is None else max(self.maxy, y)

        key = self.key(x, y)
        self.values[key] = v

    def get(self):
        lines = []

        for y in range(self.miny, self.maxy+1):
            line = ""

            for x in range(self.minx, self.maxx+1):
                key = self.key(x, y)

                if key in self.values:
                    line += self.values[key]
                else:
                    line += self.air

            lines.append(line)

        return "\n".join(lines)




class Rock():

    def __init__(self, shape):
        self.x = 0
        self.y = 0

        self.shape = shape

        self.w = len(self.shape[0])
        self.h = len(self.shape)

    def isrock(self, dx, dy):
        if dx >= 0 and dx < self.w:
            if dy >= 0 and dy < self.h:
                return self.shape[dy][dx] == "#"

    def intersects(self, other):

        if self == other: 
            print("testing rock against itself. probably done something wrong")
        
        #test aabb
        if self.x + self.w - 1 < other.x or self.x > other.x + other.w - 1:
            return False
        if self.y + self.h - 1 < other.y or self.y > other.y + other.h - 1:
            return False

        for dx in range(0, self.w):
            for dy in range(0, self.h):
                if self.isrock(dx, dy):
                    odx = self.x - other.x + dx
                    ody = self.y - other.y + dy
                    if other.isrock(odx, ody):
                        return True

    def trypush(self, dx, dy):

        self.x += dx
        self.y += dy

        def undo():
            self.x -= dx
            self.y -= dy

        if self.x <= WALL_LEFT:
            undo()
            return False
        if self.x + self.w - 1 >= WALL_RIGHT:
            undo()
            return False
        if self.y + self.h - 1 >= FLOOR:
            undo()
            return False

        for other in reversed(rocks):
            if other == self: continue
            if self.intersects(other):
                undo()
                return False

        return True

    def draw(self, view):
        for dx in range(0, self.w):
            for dy in range(0, self.h):
                if self.isrock(dx, dy):
                    view.set(self.x + dx, self.y + dy, "#")

def render():
    view = View2D(" ")

    for x in range(0, 9):
        view.set(x, 0, "=")

    for y in range(-5, 0):
        view.set(0, y, "|")
        view.set(8, y, "|")

    for rock in rocks:
        rock.draw(view)


    print(view.get())

def getJet():
    jet = jets.pop(0)
    jets.append(jet)
    if jet == ">":
        return 1
    else:
        return -1

def dropRock(i):

    highestPoint = 0
    for other in rocks:
        highestPoint = min(other.y, highestPoint)

    rock = Rock(shapes[i])

    rock.x = 3
    rock.y = highestPoint - 4 - (rock.h - 1)

    while True:

        #push by jet
        jet = getJet()
        rock.trypush(jet, 0)

        #push by gravity
        pushed = rock.trypush(0, 1)
        if not pushed:
            break

    rocks.append(rock)


for i in range(0, 2022):
    print("dropping", i)
    dropRock(i % len(shapes))

render()

highestPoint = 0
for rock in rocks:
    highestPoint = min(rock.y, highestPoint)

print(-highestPoint)