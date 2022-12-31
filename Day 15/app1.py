lines = None
with open("Day 15\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

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

#for each sensor
#find closest point on row=y (manhattan)
#if out of range, this point can have a beacon, break
#if in range, if this point is a beacon, break
#if in range, and this point is free, no beacon, check left and right


sensorExists = {}
beaconExists = {}
for sensor in sensors:
    sensorExists[sensor.s] = True
    beaconExists[sensor.b] = True


cannot = {}

for i, sensor in enumerate(sensors):

    print("checking sensor", i)

    firstCheck = V2(sensor.s.x, 2000000)
    toCheck = [firstCheck]

    checked = {}

    while len(toCheck) > 0:
        point = toCheck.pop(0)
        checked[point] = True
        
        dist = distance(sensor.s, point)

        if dist > sensor.d:
            continue
        elif (point in sensorExists) or (point in beaconExists):
            continue
        else:
            cannot[point] = True

            left = V2(point.x-1, point.y)
            right = V2(point.x+1, point.y)

            if not left in checked:
                toCheck.append(left)
            if not right in checked:
                toCheck.append(right)

print(len(cannot.keys()))