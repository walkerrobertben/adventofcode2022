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
        return self.x == other.x and self.y == other.y and self.z == other.z
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
    global world

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

for line in lines:
    pos = Vector3(*map(int, line.split(",")))
    add_cube(pos)

total_exposed = 0
for pos, cube in world.items():
    total_exposed += cube.exposed

print(total_exposed)