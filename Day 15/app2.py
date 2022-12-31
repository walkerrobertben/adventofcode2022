lines = None
with open("Day 15\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

import random

class _V2:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

v2s = {}

def V2(x, y):
    k = str(x) + "," + str(y)
    if not k in v2s:
        v2s[k] = _V2(x, y)
    return v2s[k]

def distance(p1, p2):
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)

SENSOR = "S"
BEACON = "B"

class Sensor:
    def __init__(self, s, b):
        self.s = s
        self.b = b
        self.d = distance(s, b)

def V2FromString(s):
    [x, y] = s.split(", ")
    x = x.strip("x=")
    y = y.strip("y=")
    return V2(int(x), int(y))

sensors = []
for line in lines:
    [sensor, beacon] = line.split(": ")
    sensor = sensor.strip("Sensor at ")
    beacon = beacon.strip("closest beacon is at ")
    sensors.append(Sensor(V2FromString(sensor), V2FromString(beacon)))



#each sensor defines a diamond shape
#that diamond is made of 4, 45 degree lines


def isint(x):
    if isinstance(x, int):
        return True
    elif isinstance(x, float):
        return x.is_integer()
    return False

class Line:
    def __init__(self, point, gradient):
        self.p = point

        #self.gradient = gradient

        if gradient == 1:
            self.d = V2(1, 1)

        if gradient == -1:
            self.d = V2(1, -1)

    def intersection(self, other):
        ix = -((-other.d.y * other.p.x * self.d.x + other.d.x * other.p.y * self.d.x + other.d.x * self.d.y * self.p.x - other.d.x * self.d.x * self.p.y) / (other.d.y * self.d.x - other.d.x * self.d.y))
        iy = -((other.d.y * other.p.x * self.d.y - other.d.x * other.p.y * self.d.y - other.d.y * self.d.y * self.p.x + other.d.y * self.d.x * self.p.y) / (-other.d.y * self.d.x + other.d.x * self.d.y))
        if isint(ix): ix = int(ix)
        if isint(iy): iy = int(iy)
        return V2(ix, iy)

lines = []
for sensor in sensors:
    dx = int(sensor.d/2)
    dy = (sensor.d - dx) + 1
    test = V2(sensor.s.x + dx, sensor.s.y + dy)
    lines.append(Line(V2(sensor.s.x + dx, sensor.s.y + dy), -1))
    lines.append(Line(V2(sensor.s.x + dx, sensor.s.y - dy), 1))
    lines.append(Line(V2(sensor.s.x - dx, sensor.s.y + dy), 1))
    lines.append(Line(V2(sensor.s.x - dx, sensor.s.y - dy), -1))

checked = {}

for line in lines:
    for other in lines:

        if line == other or line.d == other.d:
            continue

        i = line.intersection(other)

        if isint(i.x) and isint(i.y):
            if 0 <= i.x <= 4000000 and 0 <= i.y <= 4000000:
                if not i in checked:
                    
                    works = True
                    for sensor in sensors:

                        d = distance(sensor.s, i)
                        if d <= sensor.d:
                            works = False
                            break

                    if works:
                        print(i.x, i.y, i.x * 4000000 + i.y)

                    checked[i] = True