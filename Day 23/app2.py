lines = None
with open("Day 23\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

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

class Elf:
    def __init__(self, x, y, c):
        self.name = c
        self.position = Vector2(x, y)
        self.proposing = 0

propose_cycle = [
    (Vector2(-1, -1), Vector2(0, -1), Vector2(1, -1)),
    (Vector2(1, 1), Vector2(0, 1), Vector2(-1, 1)),
    (Vector2(-1, 1), Vector2(-1, 0), Vector2(-1, -1)),
    (Vector2(1, -1), Vector2(1, 0), Vector2(1, 1)),
]

check_around = (
    Vector2(-1, -1), Vector2(0, -1), Vector2(1, -1),
    Vector2(-1,  0),                 Vector2(1,  0),
    Vector2(-1,  1), Vector2(0,  1), Vector2(1,  1),
)

elves = []

n = 0
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c == "#":
            elves.append(Elf(x, y, chr(65+n)))
            n += 1


def iteration():

    #each elf proposes a position to move to
    #duplicate propositions are culled
    #remaining propositions are fulfilled
    #each elfs proposition counter increments

    #cache elf positions
    elf_positions = set()
    for elf in elves:
        elf_positions.add(elf.position)

    propositions = {}
    for elf in elves:

        #check all around. if no adjacent elves, skip this
        should_try_move = False
        for check in check_around:
            check_world_pos = elf.position + check
            if check_world_pos in elf_positions:
                should_try_move = True
                break
            
        if should_try_move:
            proposed_delta = None

            for i in range(0, len(propose_cycle)):
                checks = propose_cycle[i]
                passed_checks = True

                for check in checks:
                    check_world_pos = elf.position + check
                    if check_world_pos in elf_positions:
                        passed_checks = False
                        break

                if passed_checks:
                    proposed_delta = checks[1]
                    break

            if proposed_delta:
                proposed_position = elf.position + proposed_delta

                if proposed_position in propositions:
                    propositions[proposed_position] = True
                else:
                    propositions[proposed_position] = elf


    move_count = 0
    for proposed_position, elf in propositions.items():
        if isinstance(elf, Elf):
            move_count += 1
            elf.position = proposed_position

    #move cycle
    propose_cycle.append(propose_cycle.pop(0))

    return move_count == 0

def calculate_coverage():
    AA = None
    BB = None

    for elf in elves:
        if AA == None:
            AA = Vector2(elf.position.x, elf.position.y)
        else:
            AA.x = min(AA.x, elf.position.x)
            AA.y = min(AA.y, elf.position.y)
        if BB == None:
            BB = Vector2(elf.position.x, elf.position.y)
        else:
            BB.x = max(BB.x, elf.position.x)
            BB.y = max(BB.y, elf.position.y)

    w = BB.x - AA.x + 1
    h = BB.y - AA.y + 1

    return (w * h) - len(elves)

def render():
    view = View2D(".")
    for i, elf in enumerate(elves):
        view.set(elf.position.x, elf.position.y, elf.name)
    print(view.get())


n = 0
while True:
    done = iteration()
    n += 1

    print(n)

    if done:
        break

print("done")