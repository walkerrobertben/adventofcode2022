lines = None
with open("Day 17\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

import math

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



class Space2D():
    def __init__(self, air):
        self.air = air
        self.values = {}
        self.minx = None
        self.maxx = None
        self.miny = None
        self.maxy = None

    def key(self, x, y):
        return str(x) + ":" + str(y)

    def get(self, x, y):
        key = self.key(x, y)
        if key in self.values:
            return self.values[key]
        else:
            return None

    def set(self, x, y, v):
        self.minx = x if self.minx is None else min(self.minx, x)
        self.maxx = x if self.maxx is None else max(self.maxx, x)
        self.miny = y if self.miny is None else min(self.miny, y)
        self.maxy = y if self.maxy is None else max(self.maxy, y)

        key = self.key(x, y)
        self.values[key] = v

    def get_all(self):
        return self.values

    def render(self, delim="\n"):
        lines = []

        if not(self.minx is None or self.maxx is None or self.miny is None or self.maxy is None):
            for y in range(self.miny, self.maxy+1):
                line = ""

                for x in range(self.minx, self.maxx+1):
                    key = self.key(x, y)

                    if key in self.values:
                        line += self.values[key]
                    else:
                        line += self.air

                lines.append(line)

        return delim.join(lines)


#hash world state (world space, rock index, jet index)

#if we encountered this hash before:
# we found a cycle, use it to extrapolate
# add on height difference caused by this cycle to get us just below target

#simulate dropping a rock
#any cell in the new world that has 4 neighbours gets culled


history = {}

world = Space2D(" ")

iteration = 0
jetIndex = 0
done_jump = False

iteration_target = 1000000000000

def get_world_height():
    return FLOOR if world.miny is None else -world.miny

def drop_rock(rockIndex):

    global jetIndex

    #build rock from shape
    shape = shapes[rockIndex]
    rw = len(shape[0])
    rh = len(shape)

    rock = []
    for dx in range(0, rw):
        for dy in range(0, rh):
            if shape[dy][dx] == "#":
                rock.append((dx, dy))
    
    #spawn rock 2-air to left wall and 3-air to highest point
    x = WALL_LEFT + 3
    y = (-get_world_height()) - rh - 3

    #simulate jet + gravity pushes
    def test_intersect():
        for [dx, dy] in rock:
            wx, wy = x + dx, y + dy
            if wx <= WALL_LEFT or wx >= WALL_RIGHT:
                return True
            if wy >= FLOOR:
                return True
            if world.get(wx, wy) == "#":
                return True

    def try_push(px, py):
        nonlocal x, y
        x += px
        y += py
        if test_intersect():
            x -= px
            y -= py
            return False
        return True

    while True:

        #push by jet
        jet = jets[jetIndex]
        try_push(1 if jet == ">" else -1, 0)

        #increment jet index for next push
        jetIndex = (jetIndex + 1) % len(jets) 

        #push by gravity
        if not try_push(0, 1):
            break
    
    #write rock to world
    for [dx, dy] in rock:
        world.set(x + dx, y + dy, "#")

def cull_cells():

    #bfs from spawn location. any cell not hit can never be reached by a falling rock so cull it.

    cx = WALL_LEFT + 3
    cy = (FLOOR if world.miny is None else world.miny) - 1 - 3

    explore = [(cx, cy)]
    visited = set()

    new_world = Space2D(" ")

    def key(cell):
        return str(cell[0]) + "," + str(cell[1])

    def is_visited(cell):
        return key(cell) in visited

    while len(explore) > 0:
        this = explore.pop(0)

        if not is_visited(this):
            visited.add(key(this))

            adjacent = ( #possible adjacent cells to check
                (this[0] + 1, this[1]),
                (this[0] - 1, this[1]),
                (this[0], this[1] + 1),
                #(this[0], this[1] - 1),  #no point checking up (undersides of things dont matter since rocks always fall)
            )

            for other in adjacent:
                if other[0] > WALL_LEFT and other[0] < WALL_RIGHT:
                    if other[1] >= cy and other[1] < FLOOR:
                        if not is_visited(other):
                            if world.get(other[0], other[1]) == "#":
                                new_world.set(other[0], other[1], "#")
                            else:
                                explore.append(other)

    return new_world

def do_jump(iter1, iter2, height1, height2):
    global iteration, done_jump

    #there is cycle between iter1 and iter2
    #that takes height from height1 to height2
    cycle_length = iter2 - iter1
    cycle_height = height2 - height1

    #iteration + m * cycle_length = iteration_target
    #rearrange for m, and round down to nearest integer
    m = math.floor((iteration_target - iteration) / cycle_length)
    n = m * cycle_length
    h = m * cycle_height

    #jump iteration
    iteration += n

    #jump height
    new_world = Space2D(" ")
    for cell, value in world.get_all().items():
        [x, y] = map(int, cell.split(":"))
        new_world.set(x, y-h, value) #shift every cell up by h

    done_jump = True

    return new_world

def do_iteration():
    global world, iteration

    iteration += 1
    rockIndex = (iteration-1) % len(shapes)

    if not done_jump:

        stateHash = world.render(":") + ":" + str(rockIndex) + ":" + str(jetIndex)
        world_height = get_world_height()
    
        if stateHash in history:
            #we've encountered this state before, we can use it to jump forward
            world = do_jump(history[stateHash][0], iteration, history[stateHash][1], world_height)

        else:
            #save this state hash to the history
            history[stateHash] = (iteration, world_height)

    drop_rock(rockIndex) #drop rock
    world = cull_cells() #cull world nodes not hit by a bfs from the next spawn pos
    
while iteration < iteration_target:
    do_iteration()

print(get_world_height())