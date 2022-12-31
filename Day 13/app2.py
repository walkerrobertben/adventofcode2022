lines = None
with open("Day 13\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

import itertools
import functools

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


NEXT = 0
RIGHT = -1
WRONG = 1

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

packets = []

packets.append("[[2]]")
packets.append("[[6]]")

for line in lines:
    if line != "":
        packets.append(line)

for packet in packets:
    print(packet)

packets.sort(key = functools.cmp_to_key(compare))

for packet in packets:
    print(packet)

p1 = -1
p2 = -1

for i, packet in enumerate(packets):
    if packet == "[[2]]":
        p1 = i+1
    elif packet == "[[6]]":
        p2 = i+1

print(p1, p2, p1*p2)