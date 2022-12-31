import random

test = []

things = list(range(1, 30))
dividers = list(range(1, 30))

random.shuffle(things)
random.shuffle(dividers)


v1 = 1
v2 = 1

n1 = 0
n2 = 0

for i, thing in enumerate(things):
    divider = dividers[i]

    v1 = (v1 + thing)
    v2 = (v2 + thing) % divider

    print(v1, thing, divider)

    if v1 % divider == 0:
        n1 += 1
    if v2 == 0:
        n2 += 1

print(n1, n2)


# print(things)


# for x in range(1, 20):

#     value = 1

#     for i in range(1, 100):

#         value = (value * i) % x

#         if value % x == 0:
#             n += 1

# print("there are", n)