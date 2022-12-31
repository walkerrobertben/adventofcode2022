lines = None
with open("Day 08\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

forest = []

dirs = (
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1)
)

for line in lines:
    row = []
    for tree in line:
        row.append(int(tree))
    forest.append(row)

total = 0

width = len(lines[0])
height = len(lines)

for y, row in enumerate(forest):
    for x, tree in enumerate(row):

        hidden = True

        for dir in dirs:

            n = 0
            foundTaller = False
            while True:
                n += 1
                nX = x + dir[0] * n
                nY = y + dir[1] * n

                if nX >= 0 and nX < width and nY >= 0 and nY < height:
                    nTree = forest[nY][nX]
                    if nTree >= tree:
                        foundTaller = True
                        break
                else:
                    break
            
            if not foundTaller:
                hidden = False

        if not hidden:
            total += 1

print(total)