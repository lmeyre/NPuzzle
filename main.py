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
                    help='The heuristic function to use : 0 = Manhattan (default), 1 = Autre chose3, 2 = NTM')
    args = parser.parse_args()

    p = Parsing.Parsing()
    puzzle, err = p.parse(args.file)
    if err:
        print("n-puzzle error: %s" % err)
        return False
    # print("Solvable" if Utils.is_solvable(puzzle, Utils.get_goal_snail(puzzle)) else "Not solvable")
    Solver = Puzzle.Puzzle(puzzle, args.heuristic)
    if (Solver.launch_puzzle()):
        print("mes couilles")
        sys.exit()
    return True
        
if __name__ == '__main__':
    try:
         if main() == False:
             sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(0)
