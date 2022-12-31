lines = None
with open("Day 13\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

import itertools

def parseSet(set):
    parsed = []
    set = set[1:len(set)-1]

    item = ""
    depth = 0
    for c in set:
        if depth == 0 and c == ",":
            if not item.startswith("["):
                item = int(item)
            parsed.append(item)
            item = ""
        else:
            item += c
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1

    if item != "":
        if not item.startswith("["):
            item = int(item)
        parsed.append(item)

    return parsed


NEXT = "NEXT"
RIGHT = "RIGHT"
WRONG = "WRONG"

def compare(left, right):

    print("comparing", left, right)

    if left is None:
        return RIGHT
    if right is None:
        return WRONG

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return RIGHT
        elif left > right:
            return WRONG
        else:
            return NEXT

    elif isinstance(left, str) and isinstance(right, str):
        left = parseSet(left)
        right = parseSet(right)
        for l2, r2 in itertools.zip_longest(left, right):
            result = compare(l2, r2)
            if result != NEXT:
                return result
        return NEXT

    else:
        l2 = "[" + str(left) + "]" if isinstance(left, int) else left
        r2 = "[" + str(right) + "]" if isinstance(right, int) else right
        return compare(l2, r2)

i = 0
t = 0
def readPair():
    global i
    global t

    i += 1

    p1 = lines.pop(0) #line 1
    p2 = lines.pop(0) #line 2
    result = compare(p1, p2)
    print(result)
    if result == RIGHT:
        t += i

while True:
    readPair()
    if len(lines) > 0:
        lines.pop(0) #read blank
    else:
        break

print(t)