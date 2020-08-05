from State import State
from enum import Enum
from Heuristic import HeuristicValue, E_Heuristic
import sys
import Utils

class E_Search(Enum):
    A_STAR = 0
    IDA_STAR = 1
    UNIFORM_COST = 2
    GREEDY_SEARCH = 3

#Faire remonter les exits
class Puzzle:

    def __init__(self, puzzle, heuristic):
        self.size = len(puzzle)
        HeuristicValue.heuristic = E_Heuristic(heuristic)
        self.err = self.create_goal(puzzle)
        if not self.err:
            self.starter = State(puzzle, 0, None)
            print("start :")
            for row in self.starter.puzzle:
                print(row)
            self.actives = []
            self.used = []
            self.debug = False
            print("We are using heuristic = ", E_Heuristic(heuristic))

    def check_valid_puzzle(self, origin_puzzle):
        return Utils.is_solvable(origin_puzzle, self.goal)

    def create_goal(self, origin_puzzle):
        self.goal = Utils.create_goal(origin_puzzle)
        if not self.check_valid_puzzle(origin_puzzle):
            return "puzzle is unsolvable"
        HeuristicValue.goal = self.goal
        return None
        
    def a_star(self):
        best = self.actives[0]
        bestF = self.actives[0].f
        for i in self.actives:
            if i.f < bestF:
                bestF = i.f
                best = i
        if (self.debug):
            print("Path selected, we selected this with a value of F,H,G", bestF, best.h, best.g)
            #print(best.puzzle)
        return best
    
    def greedy_search(self):
        best = self.actives[0]
        bestH = self.actives[0].h
        for i in self.actives:
            if i.h < bestH:
                bestH = i.h
                best = i
        if (self.debug):
            print("Path selected, we selected this with a value of H", bestH)
            #print(best.puzzle)
        return best
    
    def uniform_cost_search(self):
        best = self.actives[0]
        bestG = self.actives[0].g
        for i in self.actives:
            if i.g < bestG:
                bestG = i.g
                best = i
        if (self.debug):
            print("Path selected, we selected this with a value of G", bestG)
            #print(best.puzzl
        return best

    def check_past_states(self, newState):
        for i in self.actives:
            if (newState == i.puzzle):
                return False
        for i in self.used:
            if (newState == i.puzzle):
                return False
        return True

        
    def run_puzzle(self, hide, algo):
        loop = 0
        self.actives.append(self.starter)
        if self.debug:
            print("Origin = ")
            for i in range(0, len(self.starter.puzzle)):
                print(self.starter.puzzle[i])
        current = None
        while True:
            loop += 1
            if loop > 10000:
                print("End too long, total try = ", loop)
                print("our state was ")
                for row in current.puzzle:
                    print(row)
                print(" its h value was ", current.h)
                sys.exit()
            #///////////////////////////
            if algo == E_Search.A_STAR:#for now we have if -> later call 3 different for A*, greedy etc  | on le fait a la fin car sinon on va devoir rajouter le debug dans les 3 fonction a chaque fois
                current = self.a_star()
            elif algo == E_Search.UNIFORM_COST:
                current = self.uniform_cost_search()
            elif algo == E_Search.GREEDY_SEARCH:
                current = self.greedy_search()
            # elif algo == E_Search.IDA_STAR:
            #     current = self.ida_star():
            if (current.h == 0):
                break
            paths = current.create_paths()
            self.used.append(current)
            self.actives.remove(current)
            for i in paths:
                if self.check_past_states(i.puzzle):
                    self.actives.append(i)

        print("Finished in a total of ", loop, "loops in algo")
        for i in range(0, len(current.puzzle)):
            print(current.puzzle[i])
        print("Complexity in time : ", (len(self.used) + len(self.actives)))
        #Missing complexity in size here
        print("The original state was solved in ", current.g, "moves")
        if not(hide):
            print("Winning sequence from start to end : \n")
            Utils.display_winning_sequence(current, True)

    def launch_puzzle(self, hide, algo):
        print("Using algorythm : ", algo)
        if (self.err):
            return self.err
        self.run_puzzle(hide, algo)
        return None
