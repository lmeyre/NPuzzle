import State
from Heuristic import HeuristicValue, heuristic_type

class OurPuzzle:

    def __init__(self, size):
        self.size = size
        self.actives = []
        self.used = []
        
    def read_input(self):
        puzzle = []
        #On pourrait prendre chiffre par chiffre, mais ligne semble plus clair
        for i in range(0, self.size):
            while True:
                line = input().split(" ")
                if (len(line) == self.size):
                    break 
                print("Please enter a right number of elements")
            puzzle.append()
        return puzzle
        #Protection, nombre double, lettres, etc. A integrer.
        #En a ton besoin ? Ca peut marcher avec des lettres etc
    
    def get_data(self):
        print("Please enter the original puzzle form, line by line")
        self.start = State(self.read_input(), 0, 0, None) #start is a node with f value etc
        print("Please enter the goal puzzle form, line by line")
        self.goal = self.read_input() #Goal is just an array with no f value
        
        
    def run_puzzle(self):
        #Do while not avalaible ?
        self.actives.append(self.start)
        while True:
            current = self.actives[0]
            if (current.h == 0):
                break
            paths = current.create_paths()


    def launch_puzzle(self):
        self.heur = HeuristicValue(heuristic_type.MANHATTAN)
        self.get_data()
        self.run_puzzle()