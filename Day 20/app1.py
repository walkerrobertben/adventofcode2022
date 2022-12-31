lines = None
with open("Day 20\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

class Value:
    def __init__(self, value):
        self.value = int(value)
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self)

zero = None
values = []
for line in lines:
    v = Value(line)
    if v.value == 0:
        zero = v
    values.append(v)

n = len(values)

for value in values.copy():
    if value.value != 0:
        i0 = values.index(value)
        i1 = (i0 + value.value) % (n - 1)
        values.pop(i0)
        values.insert(i1, value)

def get(i):
    return values[(values.index(zero) + i) % n].value

print(get(1000) + get(2000) + get(3000))
