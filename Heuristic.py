from enum import Enum
import Utils

class E_Heuristic(Enum):
    MANHATTAN = 0
    OUT_OF_PLACE = 1
    LINEAR_CONFLICT = 2
    CORNER_TILE = 3

class HeuristicValue:

    heuristic = E_Heuristic.MANHATTAN
    goal = []

    @staticmethod
    def return_h(state):
        if (HeuristicValue.heuristic == E_Heuristic.MANHATTAN):
            return HeuristicValue.h_manhattan(state)
        elif (HeuristicValue.heuristic == E_Heuristic.OUT_OF_PLACE):
            return HeuristicValue.check_out_of_place(state)
        elif (HeuristicValue.heuristic == E_Heuristic.LINEAR_CONFLICT):
            return HeuristicValue.check_linear_conflict(state)
        elif (HeuristicValue.heuristic == E_Heuristic.CORNER_TILE):
            return HeuristicValue.h_corner_tile(state)

    @staticmethod
    def h_manhattan(curr):
        difference = 0
        for i in range(0, len(curr.puzzle)):
            for j in range(0, len(curr.puzzle)):
                if curr.puzzle[i][j] != HeuristicValue.goal[i][j]:
                    x, y = Utils.find_pos(curr.puzzle[i][j], HeuristicValue.goal)
                    difference += return_distance(x, y, i, j)
        return difference

    @staticmethod
    def h_corner_tile(curr):
        base_h = HeuristicValue.h_manhattan(curr)
        size = len(curr.puzzle)
        for i in range(0, size):
            for j in range(0, size):
                if (curr.puzzle[i][j] == HeuristicValue.goal[i][j]):
                    continue
                if i == 0 and j == 0:
                    if curr.puzzle[i][j + 1] == HeuristicValue.goal[i][j + 1]:
                        base_h += 2
                    if curr.puzzle[i + 1][j] == HeuristicValue.goal[i + 1][j]:
                        base_h += 2
                elif i == 0  and j == size - 1:
                    if curr.puzzle[i][j - 1] == HeuristicValue.goal[i][j - 1]:
                        base_h += 2
                    if curr.puzzle[i + 1][j] == HeuristicValue.goal[i + 1][j]:
                        base_h += 2
                elif i == size - 1 and j == 0:
                    if curr.puzzle[i][j + 1] == HeuristicValue.goal[i][j + 1]:
                        base_h += 2
                    if curr.puzzle[i - 1][j] == HeuristicValue.goal[i - 1][j]:
                        base_h += 2
                elif i == size - 1 and j == size - 1:
                    if curr.puzzle[i][j - 1] == HeuristicValue.goal[i][j - 1]:
                        base_h += 2
                    if curr.puzzle[i - 1][j] == HeuristicValue.goal[i - 1][j]:
                        base_h += 2
        return base_h

    @staticmethod
    def check_linear_conflict(curr):
        base_h = HeuristicValue.h_manhattan(curr)
        conflict_value = find_conflict(curr.puzzle, HeuristicValue.goal)
        return conflict_value + base_h
    
    @staticmethod
    def check_out_of_place(curr):
        difference = 0
        for i in range(0, len(curr.puzzle)):
            for j in range(0, len(curr.puzzle)):
                if curr.puzzle[i][j] != HeuristicValue.goal[i][j]:
                    difference += 1
        return difference

def find_conflict(puzzle, goal):
    conflict_value = 0
    for row in range(0, len(puzzle)):
        conflict_value += analyze_row(row, puzzle, goal)
        conflict_value += analyze_colum(row, puzzle, goal)
    return conflict_value

def analyze_row(row, puzzle, goal):
    position = 0
    conflict_value = 0
    area1 = puzzle[row]
    for number in range(0, len(area1)):
        for other in range(0, len(area1)):
            if (return_goal_line(False, area1[number], goal) == row
            and return_goal_line(False, area1[number], goal) == return_goal_line(False, area1[other], goal)
            and number != other):
                if number < other:
                    position = -1
                else:
                    position = 1
                if ((position == -1 and return_goal_line(True, area1[number], goal) > return_goal_line(True, area1[other], goal))
                or (position == 1 and return_goal_line(True, area1[number], goal) < return_goal_line(True, area1[other], goal))):
                    conflict_value += 1
    return conflict_value

def analyze_colum(col, puzzle, goal):
    position = 0
    conflict_value = 0
    area1 = artificial_colum(puzzle, col)
    for number in range(0, len(area1)):
        for other in range(0, len(area1)):
            if (return_goal_line(True, area1[number], goal) == col
            and return_goal_line(True, area1[number], goal) == return_goal_line(True, area1[other], goal)
            and number != other):
                if number < other:
                    position = -1
                else:
                    position = 1
                if ((position == -1 and return_goal_line(False, area1[number], goal) > return_goal_line(False, area1[other], goal))
                or (position == 1 and return_goal_line(False, area1[number], goal) < return_goal_line(False, area1[other], goal))):
                    conflict_value += 1
    return conflict_value
            
def artificial_colum(puzzle, col):
    artificial = []
    for row in puzzle:
        for colum in range(0, len(row)):
            if (colum != col):
                continue
            else:
                artificial.append(row[colum])
    return artificial

def return_goal_line(is_colum, target, goal):
    if (is_colum == False):
        for row in range(0, len(goal)):
            for number in goal[row]:
                if number == target:
                    return row
    else:
        for row in goal:
            for colum in range(0, len(row)):
                if row[colum] == target:
                    return colum

def return_distance(x1, y1, x2, y2):
    finalX = abs(x1 - x2)
    finalY = abs(y1 - y2)
    return (finalX + finalY)