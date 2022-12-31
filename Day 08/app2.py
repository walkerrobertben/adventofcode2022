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

best = 0

width = len(lines[0])
height = len(lines)

for y, row in enumerate(forest):
    for x, tree in enumerate(row):

        scenic = 1
        for dir in dirs:

            n = 0
            view = 0
            while True:

                n += 1
                nX = x + dir[0] * n
                nY = y + dir[1] * n

                if nX >= 0 and nX < width and nY >= 0 and nY < height:
                    nTree = forest[nY][nX]
                    view += 1
                    if nTree >= tree:
                        break
                    
                else:
                    break

            scenic *= view

        if scenic > best:
            best = scenic

print(best)