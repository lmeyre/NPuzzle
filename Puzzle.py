from State import State
from Heuristic import HeuristicValue, E_Heuristic
import sys
import Utils

#Faire remonter les exits
class Puzzle:

    def __init__(self, puzzle, heuristic):
        self.size = len(puzzle)
        HeuristicValue.heuristic = E_Heuristic(heuristic)
        self.err = self.create_goal(puzzle)
        self.starter = State(puzzle, 0, None)
        self.actives = []
        self.used = []
        self.debug = True
        print("We are using heuristic = ", E_Heuristic(heuristic))

    def check_valid_puzzle(self, origin_puzzle):
        return Utils.is_solvable(origin_puzzle, self.goal)

    def create_goal(self, origin_puzzle):
        self.goal = Utils.create_goal(origin_puzzle)
        if (self.check_valid_puzzle(origin_puzzle) == False):
            return "Puzzle is not solvable"
        HeuristicValue.goal = self.goal
        return None
        
    def best_choice(self):
        if (len(self.actives) == 0):
            print("actives are EMPTY !!")
        best = self.actives[0]
        bestF = self.actives[0].f
        for i in self.actives:
            if i.f < bestF:
                bestF = i.f
                best = i
        if (self.debug):
            print("Path selected, we selected this with a value of F,H,G", bestF, best.h, best.g)
            print(best.puzzle)
        return best

    def check_past_states(self, newState):
        #remettre quand ca marchera  
        for i in self.actives:
            if (newState == i.puzzle):
                return False
        for i in self.used:
            if (newState == i.puzzle):
                return False
        return True

        
    def run_puzzle(self):
        loop = 0
        self.actives.append(self.starter)
        if self.debug:
            print("Origin = ")
            for i in range(0, len(self.starter.puzzle)):
                print(self.starter.puzzle[i])
        while True:
            #print("One round")
            loop += 1
            if loop > 10000:
                print("End too long, total try = ", loop)
                sys.exit()
            current = self.best_choice()
            if (current.h == 0):
                break
            paths = current.create_paths()
            self.used.append(current)
            self.actives.remove(current)
            for i in paths:
                if (self.check_past_states(i.puzzle) != False):
                    self.actives.append(i)
            # if (self.debug == True):
            #     print("totals paths = ", len(self.actives), " Added new ones, they are: ")
            #     for i in paths: #Careful it count not selected path too
            #             print("///////////")
            #             for j in range(0, len(i.puzzle)):
            #                 print(i.puzzle[j])
            #             print("its f and h value = ", i.f, i.h)

        print("Finished in a total of ", loop, "loops in algo")
        for i in range(0, len(current.puzzle)):
            print(current.puzzle[i])

    def launch_puzzle(self):
        if (self.err):
            return self.err
        self.run_puzzle()
