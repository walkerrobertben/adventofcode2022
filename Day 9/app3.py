import os, copy, time

lines = None
with open("data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

rn = 10

rope = []
for i in range(0, rn):
    rope.append([0,0])

dirs = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0)
}

out = []

for line in lines:
    [dirString, stepsString] = line.split(" ")
    dir = dirs[dirString]
    steps = int(stepsString)

    for i in range(0, steps):

        rope[0][0] += dir[0]
        rope[0][1] += dir[1]

        for j in range(0, rn-1):

            r0 = rope[j]
            r1 = rope[j+1]

            dX = r0[0] - r1[0]
            dY = r0[1] - r1[1]
            d2 = dX * dX + dY * dY

            #check moved side to side
            if dX != 0:
                if d2 >= 2*2:
                    r1[0] += (dX >= 0 and 1 or -1)

            #check moved up or down
            if dY != 0:
                if d2 >= 2*2:
                    r1[1] += (dY >= 0 and 1 or -1)

        out.append(copy.deepcopy(rope))

print("Simulated")

# minX = 999999999999
# maxX = -999999999999
# minY = 999999999999
# maxY = -999999999999

# for rope in out:
#    for r in rope:
#        minX = min(minX, r[0])
#        maxX = max(maxX, r[0])
#        minY = min(minY, r[1])
#        maxY = max(maxY, r[1])

# w = maxX - minX
# h = maxY - minY

minX = -75
maxX = 75
minY = -25
maxY = 25

print("Bounds", minX, maxX, minY, maxY)

render = []
for i, rope in enumerate(out):

    rows = []
    for y in range(minY, maxY+1):
        rows.append([" "]*(maxX - minX + 1))

    for r in rope:
        x = r[0] - minX
        y = r[1] - minY

        if y >= 0 and y <= (maxY - minY):
            if x >= 0 and x <= (maxX - minX):
                rows[y][x] = "#"
        
    render.append("\n".join(map("".join, rows)))
    print("Rendered", i+1, "out of", len(out))

print("Rendering")

while True:
    for frame in render:
        print(frame)
        os.system("cls")