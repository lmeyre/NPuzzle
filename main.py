#! /usr/bin/env python3

import argparse as arg
import sys
import Parsing
import Puzzle
import Utils

def main():
    parser = arg.ArgumentParser(description='This program solves n-puzzle')
    parser.add_argument('file', type=str, nargs='?', help='A file that contains the puzzle to be solved')
    parser.add_argument('-H', '--heuristic', type=int, nargs='?', choices=[0, 1, 2], default=0,
                    help='The heuristic function to use : 0 = Manhattan (default), 1 = Out of place, 2 = Linear conflict')
    parser.add_argument("--hide", action="store_true", default=False)
    parser.add_argument('-A*', '--a_star', action="store_true", default=False)
    parser.add_argument('-IDA*', '--ida_star', action="store_true", default=False)
    parser.add_argument('-UC', '--uniform_cost', action="store_true", default=False)
    parser.add_argument('-GS', '--greedy_search', action="store_true", default=False)
    args = parser.parse_args()

    p = Parsing.Parsing()
    puzzle, err = p.parse(args.file)
    if err:
        print("n-puzzle error: %s" % err)
        return False
    # print("Solvable" if Utils.is_solvable(puzzle, Utils.get_goal_snail(puzzle)) else "Not solvable")
    algo = Puzzle.E_Search.A_STAR
    if (args.uniform_cost):
        algo = Puzzle.E_Search.UNIFORM_COST
    elif (args.greedy_search):
        algo = Puzzle.E_Search.GREEDY_SEARCH
    elif (args.ida_star):
        algo = Puzzle.E_Search.IDA_STAR
    elif (args.a_star):
        algo = Puzzle.E_Search.A_STAR
    Solver = Puzzle.Puzzle(puzzle, args.heuristic)
    err = Solver.launch_puzzle(args.hide, algo)
    if err:
        print("n-puzzle error: %s" % err)
        return False
    return True
        
if __name__ == '__main__':
    try:
         if main() == False:
            sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)

#To keep , possible not working puzzle to test again after upgrade
#  [4, 6, 15, 9]
#  [0, 7, 8, 11]
#  [1, 10, 3, 13] 
#  [2, 14, 12, 5]    