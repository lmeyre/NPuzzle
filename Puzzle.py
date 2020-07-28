from State import State
from Heuristic import HeuristicValue, E_Heuristic
import sys
import Utils

class Puzzle:

    def __init__(self, puzzle, heuristic):
        self.size = size
        self.actives = []
        self.used = []
        HeuristicValue.assign_type(heuristic)

    def check_valid_puzzle(self):
        return True

    def create_goal(self):
        if (self.check_valid_puzzle() == False):
            print("Bad Puzzle forms")#temporary message
            sys.exit()
        #sort piece to make a good puzzle
        return 0
        
    def best_choice(self):
        best = self.actives[0]
        bestF = self.actives[0].f
        for i in self.actives:
            if i.f < bestF:
                bestF = i.f
                best = i
        return best
        
    def run_puzzle(self):
        #Do while not avalaible ?
        loop = 0
        self.actives.append(self.starter)
        while True:
            #print("one loop")
            loop += 1
            if loop > 1000:
                print("stuck")
                sys.exit()
            current = self.best_choice()
            if (current.h == 0):
                break
            paths = current.create_paths()
            self.used.append(current)
            del self.actives[0]
            for i in paths:
                self.actives.append(i)
        print("finished ?")

    def launch_puzzle(self):
        self.create_goal()
        self.run_puzzle()