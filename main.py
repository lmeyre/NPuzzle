#! /usr/bin/env python3

import argparse as arg
import sys
import Parsing
import Puzzle
import Utils

def main():
    parser = arg.ArgumentParser(description='This program solves n-puzzle')
    parser.add_argument('file', type=str, nargs='?', help='A file that contains the puzzle to be solved')
    parser.add_argument('-H', '--heuristic', type=int, nargs='?', choices=[0, 1, 2, 3], default=0,
                    help='The heuristic function to use : 0 = Manhattan (default), 1 = Out of place, 2 = Linear conflict, 3 = Corner Tiles')
    parser.add_argument("--hide", action="store_true", default=False)
    algos = parser.add_mutually_exclusive_group()
    algos.add_argument('--ida', action="store_true")
    algos.add_argument('--uniformcost', action="store_true")
    algos.add_argument('--greedy', action="store_true")
    args = parser.parse_args()

    p = Parsing.Parsing()
    puzzle, err = p.parse(args.file)
    if err:
        print("n-puzzle error: %s" % err)
        return False
    # print("Solvable" if Utils.is_solvable(puzzle, Utils.get_goal_snail(puzzle)) else "Not solvable")
    algo = Puzzle.E_Search.A_STAR
    if (args.uniformcost):
        algo = Puzzle.E_Search.UNIFORM_COST
    elif (args.greedy):
        algo = Puzzle.E_Search.GREEDY_SEARCH
    elif (args.ida):
        algo = Puzzle.E_Search.IDA_STAR
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
