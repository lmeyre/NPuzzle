import sys

def translate_position(self, number, size):
    x = number / size
    y = number % size
    return x, y

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
    # goal = []
    # target = 1
    # for i in range(0, len(puzzle)):
    #     line = []
    #     for j in range(0, len(puzzle)):
    #         line.append(target)
    #         target += 1
    #         if (target == len(puzzle) * len(puzzle)):
    #             target = 0
    #     goal.append(line)
    # print("Goal is ", goal)
    #Ou truc de bg

    size = len(puzzle)
    goal = [[size * y + x for x in range(1, size+1)] for y in range(size)]
    goal[size-1][size-1] = 0
    return goal
    



