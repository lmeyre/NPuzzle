import sys

def get_goal(size):
    goal = [[size * y + x for x in range(1, size+1)] for y in range(size)]
    goal[size-1][size-1] = 0
    return goal

def create_goal(puzzle, goal_type):
    if goal_type == 'snail':
        return goal_snail(puzzle)
    elif goal_type == 'classic':
        return goal_classic(puzzle)

def goal_snail(puzzle): 
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
    return goal

def goal_classic(puzzle):
    size = len(puzzle)
    goal = [[size * y + x for x in range(1, size+1)] for y in range(size)]
    goal[size-1][size-1] = 0
    return goal
    
def find_pos(number, puzzle):
    for i in range(0, len(puzzle)):
        for j in range(0, len(puzzle)):
            if (puzzle[i][j] == number):
                return i, j
    print("Error, was looking for ", number, " in puzzle = ", puzzle)
    return 0, 0

def get_inversions(numbers): 
  
    inversions = 0
    size = len(numbers)
    for i in range(size): 
        for j in range(i + 1, size): 
            if (numbers[i] > numbers[j]):
                inversions += 1
    return inversions

def get_zero_row_position(start):
    row = 1
    for i in reversed(start):
        if 0 in i:
            return row
        row += 1
    return -1

def is_solvable(start, goal):
    start_one_row = sum(start, [])
    start_one_row = [x for x in start_one_row if x]
    goal_one_row = sum(goal, [])
    goal_one_row = [x for x in goal_one_row if x]
    inversions = get_inversions(start_one_row)
    goal_inversions = get_inversions(goal_one_row)
    if len(start) % 2:
        if goal_inversions % 2:
            if inversions % 2:
                return True
            return False
        if not inversions % 2:
            return True
        return False
    zero_row_position = get_zero_row_position(start)
    if zero_row_position % 2:
        if not inversions % 2:
            return True
        return False
    if inversions % 2:
        return True
    return False

def display_winning_sequence(final, initial):
    if (final.parent != None):
        display_winning_sequence(final.parent, False)
    for row in final.puzzle:
        print(row)
    if not (initial):
        print("      ")
        print("    |")
        print("    V")
        print("      ")