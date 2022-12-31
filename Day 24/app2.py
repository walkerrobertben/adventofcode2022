lines = None
with open("Day 24\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]


#define 2d array containing the path
#dilate path region (into adjacent cells)
#walls & wind masks off cells
#repeat dilation until target hit


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

world_width = len(lines[0])
world_height = len(lines)

direction_map = {
    ">": Vector2(1, 0),
    "v": Vector2(0, 1),
    "<": Vector2(-1, 0),
    "^": Vector2(0, -1),
}

dilate = (
    Vector2(0, 0),
    Vector2(1, 0),
    Vector2(0, 1),
    Vector2(-1, 0),
    Vector2(0, -1)
)

def find_target(start, target, wind):
    steps = 0

    path = set()
    path.add(start)

    searching_for_target = True

    while searching_for_target:
        steps += 1

        # debug = View2D(" ")
        # for x in range(0, world_width):
        #     for y in range(0, world_height):
        #         if x == 0 or y == 0 or x == world_width - 1 or y == world_height-1:
        #             debug.set(x, y, "+")
        # for pos in path:
        #     debug.set(pos.x, pos.y, "#")
        # for direction, positions in wind.items():
        #     for pos in positions:
        #         debug.set(pos.x, pos.y, direction)
        # print(debug.get())
        # print(" ")

        #move winds
        new_wind = {}
        for direction, positions in wind.items():
            new_positions = set()
            delta = direction_map[direction]

            for position in positions:
                new_position = position + delta
                if new_position.x <= 0: new_position.x = world_width - 2
                if new_position.x >= world_width - 1: new_position.x = 1
                if new_position.y <= 0: new_position.y = world_height - 2
                if new_position.y >= world_height - 1: new_position.y = 1

                new_positions.add(new_position)

            new_wind[direction] = new_positions

        #expand path
        new_path = set()
        for position in path:
            for delta in dilate:

                is_valid = False
                new_position = position + delta
            
                if new_position == start:
                    is_valid = True

                elif new_position == target:
                    is_valid = True
                    searching_for_target = False

                elif new_position.x > 0 and new_position.x < world_width - 1 and new_position.y > 0 and new_position.y < world_height - 1:
                    is_valid = True

                    for direction, positions in new_wind.items():
                        if new_position in positions:
                            is_valid = False
                            break
                            
                if is_valid:
                    new_path.add(new_position)

        path = new_path
        wind = new_wind

    return (steps, wind)

start = None
target = None
wind = {}

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        p = Vector2(x, y)
        if y == 0 and c == ".":
            start = p
        elif y == world_height-1 and c == ".":
            target = p
        elif c != "#" and c != ".":
            if not c in wind: wind[c] = set()
            wind[c].add(p)

a, new_wind = find_target(start, target, wind)
b, new_wind = find_target(target, start, new_wind)
c, new_wind = find_target(start, target, new_wind)
print(a, b, c)
print(a + b + c)