from Heuristic import HeuristicValue, E_Heuristic

class State:

    def __init__(self, puzzle, g, parent):
        self.g = g
        self.puzzle = puzzle
        self.parent = parent
        self.size = len(puzzle)
        self.h = HeuristicValue.return_h(self)
        self.f = self.g + self.h

    def give_space_pos(self):
        for i in range(0, len(self.puzzle)):
            for j in range(0, len(self.puzzle)):
                if self.puzzle[i][j] == '_':
                    return i, j
        print("no blank space in algo protect")
        return -1, -1

    def make_next_state(self, numberPosX, numberPosY, spacePosX, spacePosY):
        newPuzzle = self.clone()
        temp = self.puzzle[numberPosX][numberPosY]
        newPuzzle[numberPosX][numberPosY] = temp
        newPuzzle[spacePosX][spacePosY] = '_'
        newState = State(newPuzzle, self.g + 1, self)
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
        paths = []
        if (x - 1 >= 0):
            paths.append(self.make_next_state(x - 1, y, x, y))
        if (x + 1 < self.size):
            paths.append(self.make_next_state(x + 1, y, x, y))
        if (y - 1 >= 0):
            paths.append(self.make_next_state(x, y - 1, x, y))
        if (y + 1 < self.size):
            paths.append(self.make_next_state(x, y + 1, x, y))
        if (len(paths) == 0):
            print("0 paths ? x = " , x, " y = ", y)
        return paths
