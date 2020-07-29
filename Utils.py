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

def get_goal(size):
    goal = [[size * y + x for x in range(1, size+1)] for y in range(size)]
    goal[size-1][size-1] = 0
    return goal

def get_goal_snail(start):
    # Init goat 2d tab
    goal = [[x for x in range(1, size+1)] for y in range(size)]
    # Get list of numbers
    numbers = [x for x in range(1, size * size)]
    numbers.append(0)

    size = len(start)

    start_col_i = 0
    start_row_i = 0
    end_col_i = size
    end_row_i = size

    # while start_row_i < end_row_i and start_col_i < end_col_i:
    while end_row_i and end_col_i:
        # Fill the top empty row, left to right 🡢
        for i in range(start_col_i, end_col_i):
            goal[start_row_i][i] = numbers[0]
            numbers = numbers[1:]
        start_row_i += 1
        # Fill the bottom empty column, top to bottom 🡣
        for i in range(start_row_i, end_row_i):
            goal[i][end_col_i - 1] = numbers[0]
            numbers = numbers[1:]
        end_col_i -= 1
        # Fill the bottom empty row, right to left 🡠
        if start_row_i < end_row_i: 
            for i in range(end_col_i - 1, (start_col_i - 1), -1):
                goal[end_row_i - 1][i] = numbers[0]
                numbers = numbers[1:]
            end_row_i -= 1
        # Fill the right empty row, bottome to top 🡩
        if start_col_i < end_col_i: 
            for i in range(end_row_i - 1, start_row_i - 1, -1): 
                goal[i][start_col_i] = numbers[0]
                numbers = numbers[1:]
            start_col_i += 1
    return goal

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
    # print("goal inversions", goal_inversions)
    # print("inversions", inversions)
    # Odd case
    if len(start) % 2:

        if goal_inversions % 2:
            if inversions % 2:
                return True
            return False
        if not inversions % 2:
            return True
        return False
    # Even case
    zero_row_position = get_zero_row_position(start)
    if zero_row_position % 2:
        if not inversions % 2:
            return True
        return False
    if inversions % 2:
        return True
    return False
