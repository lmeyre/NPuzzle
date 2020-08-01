#Manager

from enum import Enum
import Utils

class E_Heuristic(Enum):
    MANHATTAN = 0

class HeuristicValue:

    heuristic = E_Heuristic.MANHATTAN
    # goal = [[0,0,0],[0,0,0],[0,0,0]]
    goal = []

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
                    difference += Utils.return_distance(x, y, i, j)
        #print(difference, " is diff")
        return difference

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
