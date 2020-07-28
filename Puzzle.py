from State import State
from Heuristic import HeuristicValue, E_Heuristic
import sys
import Utils

class Puzzle:

    def __init__(self, size):
        self.size = size
        self.actives = []
        self.used = []
        
    def read_input(self):
        puzzle = []
        for i in range(0, self.size):
            while True:
                line = input().split(" ")
                if (len(line) == self.size):
                    break 
                print("Please enter a right number of elements, you entered " , len(line))
            puzzle.append(line)
        return puzzle
    
    def get_data(self):
        print("Please enter the original puzzle form, line by line")
        lineArray = self.read_input()
        self.starter = State(lineArray, 0, None) 

    def check_valid_puzzle(self):
        numbers = Utils.collect_numbers(self.starter.puzzle)
        #Utils.verify_numbers(numbers, self.size)
        return True

    def create_goal(self):
        if (self.check_valid_puzzle() == False):
            print("Bad Puzzle forms")#temporary message
            sys.exit()
        #sort piece to make a good puzzle
        return 0
        
    def best_choice(self):
        #print("actives cells = ", len(self.actives))
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
        HeuristicValue.assign_type(E_Heuristic.MANHATTAN)
        self.get_data()
        self.create_goal()
        self.run_puzzle()

x = Puzzle(3)
x.launch_puzzle()
"1 3 2"
"4 5 6"
"8 7 _"