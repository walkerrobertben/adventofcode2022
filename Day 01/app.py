lines = None
with open("Day 01\\data.txt") as f:
    lines = [line.strip("\n") for line in f.readlines()]

elfIndex = 1
calorieSum = 0
elfCalorieSums = []

for itemCalorieContent in lines:
    if itemCalorieContent == '':
        #new elf
        elfCalorieSums.append((elfIndex, calorieSum))
        elfIndex += 1
        calorieSum = 0

    else:
        calorieSum += int(itemCalorieContent)

def getSortCriteria(t):
    return t[1]

elfCalorieSums.sort(reverse=True, key = getSortCriteria)

finalSum = 0
for i in range(0, 3):
    finalSum += elfCalorieSums[i][1]

print(finalSum)

# calorieSum = 0
# currentElfNumber = 1

# highestElfCalories = 0
# highestElfNumber = 0

# for itemCalorieContent in foodList:
#     if itemCalorieContent == '':
#         #we are now at the end of this elfs food count
#         #check if it is the highest
#         if (calorieSum > highestElfCalories):
#             highestElfCalories = calorieSum
#             highestElfNumber = currentElfNumber

#         calorieSum = 0
#         currentElfNumber += 1

#     else:
#         calorieSum += int(itemCalorieContent)

# print("The highest elf is elf", highestElfNumber, "with", highestElfCalories, "calories")