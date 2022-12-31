lines = None
with open("Day 18\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

class Vector3:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + ", " + str(self.z)
    def __hash__(self):
        return hash(str(self))
    def __eq__(self, other):
        if isinstance(other, Vector3):
            return self.x == other.x and self.y == other.y and self.z == other.z
        else:
            return False
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

class Cube:
    def __init__(self, position):
        self.position = position
        self.exposed = 6

world = {}

def add_cube(pos):
    # global world

    #add cube to world
    world[pos] = Cube(pos)

    #remove exposed from any adjacent
    adjacents = (
        pos + Vector3(1, 0, 0),
        pos + Vector3(-1, 0, 0),
        pos + Vector3(0, 1, 0),
        pos + Vector3(0, -1, 0),
        pos + Vector3(0, 0, 1),
        pos + Vector3(0, 0, -1)
    )
    for adjacent in adjacents:
        if adjacent in world:
            world[pos].exposed -= 1
            world[adjacent].exposed -= 1

#add cubes to world
for line in lines:
    pos = Vector3(*map(int, line.split(",")))
    add_cube(pos)


#find region containing cubes
AA = None
BB = None
for pos, cube in world.items():
    if AA == None:
        AA = pos
    else:
        AA = Vector3(min(AA.x, pos.x), min(AA.y, pos.y), min(AA.z, pos.z))
    if BB == None:
        BB = pos
    else:
        BB = Vector3(max(BB.x, pos.x), max(BB.y, pos.y), max(BB.z, pos.z))
AA -= Vector3(1,1,1)
BB += Vector3(1,1,1)


#bfs and add 'EXTERIOR' to world
#iterate over every cube with >0 adjacent. check if those adjacent are now EXTERIOR
EXTERIOR = "ext"
explore = [AA]

while len(explore) > 0:
    this = explore.pop(0)
    if not this in world:

        world[this] = EXTERIOR

        adjacents = (
            this + Vector3(1, 0, 0),
            this + Vector3(-1, 0, 0),
            this + Vector3(0, 1, 0),
            this + Vector3(0, -1, 0),
            this + Vector3(0, 0, 1),
            this + Vector3(0, 0, -1)
        )
        for adjacent in adjacents:
            if adjacent.x >= AA.x and adjacent.y >= AA.y and adjacent.z >= AA.z:
                if adjacent.x <= BB.x and adjacent.y <= BB.y and adjacent.z <= BB.z:
                    if not adjacent in world:
                        explore.append(adjacent)

#recalculate exposed based on adjacency to EXTERIOR objects
for pos, object in world.items():
    if isinstance(object, Cube):
        if object.exposed > 0:
            
            exterior_exposed = 0

            adjacents = (
                pos + Vector3(1, 0, 0),
                pos + Vector3(-1, 0, 0),
                pos + Vector3(0, 1, 0),
                pos + Vector3(0, -1, 0),
                pos + Vector3(0, 0, 1),
                pos + Vector3(0, 0, -1)
            )
            for adjacent in adjacents:
                if adjacent in world:
                    if world[adjacent] == EXTERIOR:
                        exterior_exposed += 1

            object.exposed = exterior_exposed


#calculate total exposed
total_exposed = 0
for pos, object in world.items():
    if isinstance(object, Cube):
        total_exposed += object.exposed

print(total_exposed)