#Manager

from enum import Enum

class E_Heuristic(Enum):
    MANHATTAN = 0

class HeuristicValue:

    heuristic = E_Heuristic.MANHATTAN
    goal = [[0,0,0],[0,0,0],[0,0,0]]

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
        #print("Comparing goal and this puzzle :")
        for i in range(0, len(curr.puzzle)):
            #print(curr.puzzle[i])
            for j in range(0, len(curr.puzzle)):
                if curr.puzzle[i][j] != HeuristicValue.goal[i][j]:
                    difference += 1
                    #print("A diff, puzzle = ", curr.puzzle[i][j], " and goal : ", HeuristicValue.goal[i][j])
        #print("compared difference = ", difference)
        return difference