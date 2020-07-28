#Manager

from enum import Enum

class E_Heuristic(Enum):
    MANHATTAN = 1

class HeuristicValue:

    heuristic = E_Heuristic.MANHATTAN

    @staticmethod
    def assign_type(heur):
        if (heur == E_Heuristic.MANHATTAN):
            HeuristicValue.heuristic = E_Heuristic.MANHATTAN
        print("enum non handled error")

    @staticmethod
    def return_h(state):
        if (HeuristicValue.heuristic == E_Heuristic.MANHATTAN):
            return HeuristicValue.check_manhattan(state)

    @staticmethod
    def check_manhattan(curr):
        difference = 0
        for i in range(0, len(curr.puzzle)):
            for j in range(0, len(curr.puzzle)):
                if curr.puzzle[i][j] != ' ':#goal not known yet, ' ' is temporary, to replace with goal array
                    difference += 1
        return difference