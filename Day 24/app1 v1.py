lines = None
with open("Day 24\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

import time

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

direction_map = {
    ">": Vector2(1, 0),
    "v": Vector2(0, 1),
    "<": Vector2(-1, 0),
    "^": Vector2(0, -1),
}

check_moves = (
    Vector2(1, 0),
    Vector2(0, 1),
    Vector2(-1, 0),
    Vector2(0, -1),
)

world_width = len(lines[0])
world_height = len(lines)

class Blizzard:
    def __init__(self, x, y, d):
        self.position = Vector2(x, y)
        self.direction = direction_map[d]

class Branch:
    def __init__(self):
        self.steps = 0
        self.position = Vector2(1, 0)
        self.blizzards = []

    def simulate_step(self):
        self.steps += 1

        #build set of valid move positions as we do this
        #if blizzard lands on one of these positions, remove it
        valid_next_positions = set()
        valid_next_positions.add(self.position)
        for delta in check_moves:
            valid_next_positions.add(self.position + delta)

        for blizzard in self.blizzards:
            blizzard.position += blizzard.direction

            #wrap blizzards
            if blizzard.position.x == 0:
                blizzard.position.x = world_width - 2
            elif blizzard.position.x == world_width - 1:
                blizzard.position.x = 1
            if blizzard.position.y == 0:
                blizzard.position.y = world_height - 2
            elif blizzard.position.y == world_height - 1:
                blizzard.position.y = 1
            
            #check if blizzard hit one of the deltas
            if blizzard.position in valid_next_positions:
                valid_next_positions.remove(blizzard.position)

        return valid_next_positions

    def copy(self):
        new_branch = Branch()
        new_branch.steps = self.steps
        new_branch.position = Vector2(self.position.x, self.position.y)
        for blizzard in self.blizzards:
            new_blizzard = Blizzard(0,0,">")
            new_blizzard.position = Vector2(blizzard.position.x, blizzard.position.y)
            new_blizzard.direction = blizzard.direction
            new_branch.blizzards.append(new_blizzard)
        return new_branch

    def hash(self):
        h = str(self.position)
        for blizzard in self.blizzards:
            h += ":" + str(blizzard.position)
        return h


root = Branch()
target = None
best_steps = None
branches = [root]

previously_explored = set()

def append_with_pruning(new_branch):

    #hash branch and compare to previously explored
    if new_branch.hash() in previously_explored:
        return

    #dont add if this branch uses more steps than existing solution
    if best_steps is not None and new_branch.steps >= best_steps:
       return

    branches.append(new_branch)

for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if y == 0 and c == ".":
            root.position = Vector2(x, y)
        elif y == len(lines)-1 and c == ".":
            target = Vector2(x, y)
        elif c != "#" and c != ".":
            root.blizzards.append(Blizzard(x, y, c))

a = time.time()

while len(branches) > 0:
    branch = branches.pop(0)

    if branch.position == target:
        print("Found a solution that uses", branch.steps, "steps")
        best_steps = branch.steps if best_steps is None else min(best_steps, branch.steps)

    else:

        #simulate blizzards 1 step
        valid_next_positions = branch.simulate_step()

        #if current branch isn't breaking rule, add it back on (waiting)
        if branch.position in valid_next_positions:
            append_with_pruning(branch)

        #branch for possible moves (n, e, s, w)
        for new_position in valid_next_positions:
            if new_position == target or (new_position.x >= 1 and new_position.x <= world_width - 2 and new_position.y >= 1 and new_position.y <= world_height - 2):
                new_branch = branch.copy()
                new_branch.position = new_position
                append_with_pruning(new_branch)

    previously_explored.add(branch.hash())

    #pruning will come from figuring out if branch dead-ends
    #some branches will get you 'killed' ie - no way to escape blizzard
    #if all blizzards vanished, and branch couldnt beat current best, prune

b = time.time()

print("Explored", len(previously_explored), "branches in", (b - a), "seconds")
print("Best branch used", best_steps, "steps")