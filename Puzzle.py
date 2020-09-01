from State import State
from enum import Enum
from Heuristic import HeuristicValue, E_Heuristic
import sys
import Utils
import queue

class E_Search(Enum):
    A_STAR = 0
    IDA_STAR = 1
    UNIFORM_COST = 2
    GREEDY_SEARCH = 3

class Puzzle:

    def __init__(self, puzzle, args, algo):
        self.size = len(puzzle)
        HeuristicValue.heuristic = E_Heuristic(args.heuristic)
        self.err = self.create_goal(puzzle, args.format)
        if not self.err:
            self.starter = State(puzzle, 0, None, algo)
            print("start :")
            for row in self.starter.puzzle:
                print(row)
            self.actives = queue.PriorityQueue()
            self.used = queue.PriorityQueue()
            self.ida = []
            self.ida_used = 0
            self.complexity_size = 0
            self.debug = False
            print("We are using heuristic = ", E_Heuristic(args.heuristic))

    def update_complexity_size(self):
        if self.actives.qsize() > self.complexity_size:
            self.complexity_size = self.actives.qsize()

    def get_complexity_time(self):
        if self.ida_used:
            return self.ida_used
        else:
            return self.used.qsize() + self.actives.qsize()

    def check_valid_puzzle(self, origin_puzzle):
        return Utils.is_solvable(origin_puzzle, self.goal)

    def create_goal(self, origin_puzzle, format):
        self.goal = Utils.create_goal(origin_puzzle, format)
        if not self.check_valid_puzzle(origin_puzzle):
            return "puzzle is unsolvable"
        HeuristicValue.goal = self.goal
        return None

    def check_past_states(self, newState, current):
        if (current.parent is not None and newState.puzzle == current.parent.puzzle):
            return False
        # for i in list(self.actives.queue):
        #     if (newState.puzzle == i.puzzle and newState.priority >= i.priority):
        #         return False
        # for i in list(self.used.queue):
        #     if (newState.puzzle == i.puzzle):
        #         return False
        return True

    def search_ida(self, g, bound):
        node = self.ida[-1]
        f = g + node.h
        if f > bound:
            return f
        if node.puzzle == self.goal:
            return True
        mini = float("inf")
        for succ in node.create_paths():
            if succ not in self.ida:
                self.ida.append(succ)
                self.update_complexity_size()
                t = self.search_ida(g + 1, bound)
                if t == True:
                    return True
                if t < mini:
                    mini = t
                self.ida_used += 1
                self.ida.pop()
        return mini
 
    def ida_star(self):
        t = self.search_ida(0, self.bound)
        self.bound = t
        return self.ida[-1]
        
    def run_puzzle_ida(self):
        self.actives.put(self.starter)
        self.bound = self.starter.h
        current = None
        while True:
            self.update_complexity_size()
            current = self.ida_star()
            if (current.h == 0):
                return current

    def run_puzzle(self, algo):
        val = 0
        self.actives.put(self.starter)
        current = None
        while True:
            val += 1
            self.update_complexity_size()
            current = self.actives.get()
            if (val == 1000):
                print("current F H G = ", current.f, "  ", current.h, "   ", current.g, " et actives / used", self.actives.qsize(), "/", self.used.qsize())
                val = 0
            #print("curr = ")
            # for i in current.puzzle:
            #     print(i)
            if (current.h == 0):
                return current
            paths = current.create_paths()
            self.used.put(current, current.priority)
            for i in paths:
                if self.check_past_states(i, current):
                    self.actives.put(i, i.priority)
    
    def print_result(self, final, hide):
        for i in range(0, len(final.puzzle)):
            print(final.puzzle[i])
        complexity_time = self.get_complexity_time()
        print("Complexity in time : ", complexity_time)
        print("Complexity in size : ", self.complexity_size)
        print("The original state was solved in ", final.g, "moves")
        if not(hide):
            print("Winning sequence from start to end : \n")
            Utils.display_winning_sequence(final, True)

    def launch_puzzle(self, hide, algo):
        print("Using algorithm : ", algo)
        if (self.err):
            return self.err
        if algo != E_Search.IDA_STAR:
            final = self.run_puzzle(algo)
        else:
            final = self.run_puzzle_ida()
        self.print_result(final, hide)
        return None
