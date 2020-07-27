#Manager

from Enum import Enum

class heuristic_type(Enum):
    MANHATTAN = 1

class HeuristicValue:

    def define_heuristic(self, type):
        if (type == Enum.MANHATTAN):
            self.heuristic = Enum.MANHATTAN
        print("enum non handled error")
        return 0

    @staticmethod
    def return_h(self, state):
        if (self.heuristic == Enum.MANHATTAN):
            return self.check_manhattan(state)

    def check_manhattan(self, curr):
        difference = 0
        for i in range(0, len(curr.puzzle)):
            for j in range(0, len(i)):
                if curr.puzzle[i][j] != self.goal[i][j]:
                    difference += 1
        return difference