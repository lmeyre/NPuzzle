from State import State
from Heuristic import HeuristicValue, E_Heuristic
import sys
import Utils

#Faire remonter les exits
class Puzzle:

    def __init__(self, puzzle, heuristic):
        self.size = len(puzzle)
        HeuristicValue.heuristic = E_Heuristic.MANHATTAN
        self.create_goal(puzzle)
        self.starter = State(puzzle, 0, None)
        self.actives = []
        self.used = []
        self.debug = False

    def check_valid_puzzle(self, origin_puzzle):
        return Utils.is_solvable(origin_puzzle, self.goal)

    def create_goal(self, origin_puzzle):
        self.goal = Utils.create_goal(origin_puzzle)
        if (self.check_valid_puzzle(origin_puzzle) == False):
            print("Bad Puzzle forms")
            sys.exit()
        HeuristicValue.goal = self.goal
        
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
        for i in self.actives:
            if (newState == i.puzzle):
                return False
        for i in self.used:
            if (newState == i.puzzle):
                return False
        return True

#############################################################
#   TEST IDA*
#############################################################

    def search(self, path, g, bound):
        # node := path.last
        # f := g + h(node)
        # if f > bound then return f
        # if is_goal(node) then return FOUND
        # min := ∞
        # for succ in successors(node) do
        #     if succ not in path then
        #       path.push(succ)
        #       t := search(path, g + cost(node, succ), bound)
        #       if t = FOUND then return FOUND
        #       if t < min then min := t
        #       path.pop()
        #     end if
        # end for
        # return min
        node = path[-1]
        f = g + node.h
        if f > bound:
            return f
        # print("comparaison", node.puzzle, self.goal)
        if node.puzzle == self.goal:
            return True
        mini = float("inf")
        for succ in node.create_paths():
            if succ not in path:
                path.append(succ)
                t = self.search(path, succ.g, bound)
                if t == True:
                    return True
                if t < mini:
                    mini = t
                path.pop()
        return mini

    def ida_star(self):
        # bound := h(root)
        # path := [root]
        # loop
        #     t := search(path, 0, bound)
        #     if t = FOUND then return (path, bound)
        #     if t = ∞ then return NOT_FOUND
        #     bound := t
        # end loop
        bound = self.starter.h
        path = [self.starter]
        loop = 0
        while True:
            loop += 1
            t = self.search(path, 0, bound)
            if t == True:
                print("finished in %d loop" % loop)
                print(path, bound)
                return path, bound
            if t == float("inf"):
                print("not found")
                return False
            bound = t

#############################################################

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
            # if loop > 10:
            #     print("End too long, total try = ", loop)
            #     sys.exit()
            current = self.best_choice()
            if (current.h == 0):
                break
            paths = current.create_paths()
            self.used.append(current)
            print("1 len = ", len(self.actives))
            self.actives.remove(current)
            print("2 len = ", len(self.actives))
            for i in paths:
                if (self.check_past_states(i.puzzle) == False):
                    # paths.remove(i)
                    print("Deleting one!")
                else:
                    self.actives.append(i)
            if (self.debug == True):
                print("totals paths = ", len(self.actives), " Added ", len(paths), "new ones, they are: ")
                for i in paths:
                    print("///////////")
                    for j in range(0, len(i.puzzle)):
                        print(i.puzzle[j])
                    print("its f and h value = ", i.f, i.h)
            print("3 len = ", len(self.actives))

        print("Finished in a total of ", loop, "loops in algo")
        for i in range(0, len(current.puzzle)):
            print(current.puzzle[i])

    def launch_puzzle(self):
        self.run_puzzle()
