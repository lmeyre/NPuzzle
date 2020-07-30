import sys

# def translate_position(self, number, size):
#     x = number / size
#     y = number % size
#     return x, y

def collect_numbers(array):
    numbers = []
    exception = False
    for i in range(0, len(array)):
        for j in range(0, len(array)):
            try:
                int(array[i][j])
                numbers.append(int(array[i][j]))
            except ValueError:
                    if (array[i][j] == '_' and exception == False):
                        exception = True
                    else:
                        print("One of the cells isnt a number")
                        sys.exit()
    return numbers

def verify_numbers_link(numbers, size):
    a = 1
    total = size * size - 1
    while (a <= total):
        for i in numbers:
            print(i)
            if i == a:
                a += 1;
                break
        print("problem numbers dont link")
        sys.exit()

def create_goal(puzzle):
    size = len(puzzle)
    goal = []
    for i in puzzle:
        line = []
        for j in puzzle:
            line.append(0)
        goal.append(line)
    way = 1 
    target = 1
    posX, posY = 0, 0
    minX, minY, maxX, maxY = 0, 1, (size -1), (size -1)
    while target < (size * size):
        goal[posY][posX] = target
        # print("////")
        # for i in range(0, len(goal)):
        #     print(goal[i])
        target += 1
        if way == 1:
            posX += 1
            if (posX == (maxX)):
                way = 2
                maxX -= 1
        elif way == 2:
            posY += 1
            if (posY == (maxY)):
                way = 3
                maxY -= 1
        elif way == 3:
            posX -= 1
            if (posX == minX):
                way = 4
                minX += 1
        elif way == 4:
            posY -= 1
            if (posY == minY):
                way = 1
                minY += 1
    print("Goal is ")
    
    for i in range(0, len(goal)):
        print(goal[i])
    print("///////")
    return goal

    # OLD LINEAR GOAL... BONUS ?

    # size = len(puzzle)
    # goal = [[size * y + x for x in range(1, size+1)] for y in range(size)]
    # goal[size-1][size-1] = 0
    # print("Goal is ", goal)
    # return goal
    
def find_pos(number, puzzle):
    for i in range(0, len(puzzle)):
        for j in range(0, len(puzzle)):
            if (puzzle[i][j] == number):
                return i, j
    print("Error, was looking for ", number, " in puzzle = ", puzzle)
    return 0, 0

def return_distance(x1, y1, x2, y2):
    finalX = abs(x1 - x2)
    finalY = abs(y1 - y2)
    return (finalX + finalY)


