#Manager

from enum import Enum
import Utils
#import Heuristic

class E_Heuristic(Enum):
    MANHATTAN = 0
    OUT_OF_PLACE = 1
    LINEAR_CONFLICT = 2

class HeuristicValue:

    heuristic = E_Heuristic.MANHATTAN
    # goal = [[0,0,0],[0,0,0],[0,0,0]]
    goal = []
    #instance = HeuristicValue()

    # @staticmethod
    # def assign_type(heur):
    #     # print("here heur = ", heur)
    #     # print("man = ", E_Heuristic.MANHATTAN)
    #     #tmp 
    #     heur = E_Heuristic.MANHATTAN
    #     if (heur == E_Heuristic.MANHATTAN):
    #         HeuristicValue.heuristic = E_Heuristic.MANHATTAN
    #     else:
    #         print("enum non handled error")
    
    # @staticmethod
    # def assign_goal(goal_target):
    #     goal = goal_target
    #     print("assigned goal", goal)

    @staticmethod
    def return_h(state):
        if (HeuristicValue.heuristic == E_Heuristic.MANHATTAN):
            return HeuristicValue.check_manhattan(state)
        elif (HeuristicValue.heuristic == E_Heuristic.OUT_OF_PLACE):
            return 0 # To manage
        elif (HeuristicValue.heuristic == E_Heuristic.LINEAR_CONFLICT):
            return HeuristicValue.check_linear_conflict(state)
        else:
            print("Non handled Enum type")

    @staticmethod
    def check_manhattan(curr):
        difference = 0
        for i in range(0, len(curr.puzzle)):
            for j in range(0, len(curr.puzzle)):
                if curr.puzzle[i][j] != HeuristicValue.goal[i][j]:
                    x, y = Utils.find_pos(curr.puzzle[i][j], HeuristicValue.goal)
                    #print("distance = ", Utils.return_distance(x, y, i, j), " from ", curr.puzzle[i][j], "between start = ", curr.puzzle, " and goal = ", HeuristicValue.goal)
                    difference += return_distance(x, y, i, j)
        #print(difference, " is diff")
        return difference

    @staticmethod
    def check_linear_conflict(curr):
        # on confirme : ils sont sur la meme ligne
                        #l'un est a gauche de l'autre
                        #mais le goal de l'un est a droite du goal de l'autre
        base_h = HeuristicValue.check_manhattan(curr)
        conflict_value = find_conflict(curr.puzzle, HeuristicValue.goal)
        return conflict_value

def find_conflict(puzzle, goal):
    #row
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
            if (return_goal_line(False, number, goal) == row # if number is on the goal row
            and return_goal_line(False, number, goal) == return_goal_line(False, other, goal) # and there is another number in this row which goal is in this row too
            and number != other):
                if number < other:
                    position = -1
                else:
                    position = 1
            if ((position == -1 and return_goal_line(True, number, goal) > return_goal_line(True, other, goal))#if number is to the left (compared to other) and his goal is to the right (compared to other) -> conflict
            or (position == 1 and return_goal_line(True, number, goal) < return_goal_line(True, other, goal))):# or opposite
                conflict_value += 1 #Normalement 2 mais on met qu'un vu qu'on les compte en double
            #A voir si on detecte tous les conflits, dans les deux sens, puis a la fin on divise par deux la valeur de conflit vu qu'on les a tous compte en double, ou si on fait un truc qui verifie si on le connait deja et stock
            #Je ne sais pas lequel est le plus couteux
    return conflict_value

def analyze_colum(col, puzzle, goal):
    position = 0
    conflict_value = 0
    area1 = artificial_colum(puzzle, col)
    for number in range(0, len(area1)):
        for other in range(0, len(area1)):
            if (return_goal_line(True, number, goal) == col
            and return_goal_line(True, number, goal) == return_goal_line(True, other, goal)
            and number != other):
                if number < other:
                    position = -1
                else:
                    position = 1
            if ((position == -1 and return_goal_line(False, number, goal) > return_goal_line(False, other, goal))
            or (position == 1 and return_goal_line(False, number, goal) < return_goal_line(False, other, goal))):
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

def return_goal_line(is_colum, target, goal):#Return the line or the colum the number should be in goal state
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


    #Old manhattan -> not manhattan but heuristic: pieces out of place
    # @staticmethod
    # def check_manhattan(curr):
    #     difference = 0
    #     #print("Comparing goal and this puzzle :")
    #     for i in range(0, len(curr.puzzle)):
    #         #print(curr.puzzle[i])
    #         for j in range(0, len(curr.puzzle)):
    #             if curr.puzzle[i][j] != HeuristicValue.goal[i][j]:
    #                 difference += 1
    #                 #print("A diff, puzzle = ", curr.puzzle[i][j], " and goal : ", HeuristicValue.goal[i][j])
    #     #print("compared difference = ", difference)
    #     return difference

#on veut en faire un file comme dans util mais stock ici
def return_distance(x1, y1, x2, y2):
    finalX = abs(x1 - x2)
    finalY = abs(y1 - y2)
    return (finalX + finalY)