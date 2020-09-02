from Heuristic import HeuristicValue, E_Heuristic
import Puzzle
import queue

class State:

    def __init__(self, puzzle, g, parent, algo):
        self.algo = algo
        self.g = g
        self.puzzle = puzzle
        self.parent = parent
        self.size = len(puzzle)
        self.h = HeuristicValue.return_h(self)
        self.f = self.g + self.h
        self.priority = self.get_queue_val(algo)

    def __lt__(self, other):
        selfPriority = (self.priority)
        otherPriority = (other.priority)
        return selfPriority < otherPriority

    def give_space_pos(self):
        for i in range(0, len(self.puzzle)):
            for j in range(0, len(self.puzzle)):
                if self.puzzle[i][j] == 0:
                    return i, j
        return -1, -1

    def make_next_state(self, numberPosX, numberPosY, spacePosX, spacePosY):
        newPuzzle = self.clone()
        temp = self.puzzle[numberPosX][numberPosY]
        newPuzzle[spacePosX][spacePosY] = temp
        newPuzzle[numberPosX][numberPosY] = 0
        newState = State(newPuzzle, self.g + 1, self, self.algo)
        return newState

    def clone(self):
        copy = []
        for i in self.puzzle:
            line = []
            for j in i:
                line.append(j)
            copy.append(line)
        return copy
    
    def create_paths(self):
        x, y = self.give_space_pos()
        paths = queue.PriorityQueue()
        if (x - 1 >= 0):
            new = self.make_next_state(x - 1, y, x, y)
            paths.put(new, new.priority)
        if (x + 1 < self.size):
            new = self.make_next_state(x + 1, y, x, y)
            paths.put(new, new.priority)
        if (y - 1 >= 0):
            new = self.make_next_state(x, y - 1, x, y)
            paths.put(new, new.priority)
        if (y + 1 < self.size):
            new = self.make_next_state(x, y + 1, x, y)
            paths.put(new, new.priority)
        return paths.queue

    def get_queue_val(self, algo):
        if algo == Puzzle.E_Search.A_STAR or algo == Puzzle.E_Search.IDA_STAR:
            return self.a_star()
        elif algo == Puzzle.E_Search.UNIFORM_COST:
            return self.uniform_cost_search()
        elif algo == Puzzle.E_Search.GREEDY_SEARCH:
            return self.greedy_search()

    def a_star(self):
        return self.f
    
    def greedy_search(self):
        return self.h
    
    def uniform_cost_search(self):
        return self.g
