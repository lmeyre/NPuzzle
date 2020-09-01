#! /usr/bin/env python3

import argparse as arg
import sys
import Parsing
import Puzzle
import Utils

def main():
    parser = arg.ArgumentParser(description='This program solves N-Puzzle')
    parser.add_argument('file', type=str, nargs='?', help='file that contains the puzzle to be solved')
    parser.add_argument('-H', '--heuristic', type=int, nargs='?', choices=[0, 1, 2, 3], default=2,
                    help='the heuristic function to use : 0 = manhattan (default), 1 = out of place, 2 = linear conflict, 3 = corner tiles')
    parser.add_argument('-F', '--format', type=str, nargs='?', choices=['snail', 'classic'], default='snail',
                    help='the format of the puzzle goal : snail (default) or classic')
    parser.add_argument("--hide", action="store_true", default=False, help="hide the print of the full solution path")
    parser.add_argument('-b', "--boost", action="store_true", default=False, help="Optimisation, reduce the time")
    parser.add_argument('-A', '--algo', type=str, choices=['a_star', 'ida_star', 'greedy', 'uniform_cost'], default='a_star',
                        help='The algo')
    # algos = parser.add_mutually_exclusive_group()
    # algos.add_argument('--ida', action="store_true", help="use the IDA * algorithm")
    # algos.add_argument('--uniformcost', action="store_true", help="use the Uniform Cost algorithm")
    # algos.add_argument('--greedy', action="store_true", help="use the Greedy Search algorithm")
    args = parser.parse_args()

    p = Parsing.Parsing()
    puzzle, err = p.parse(args.file)
    if err:
        print("n-puzzle error: %s" % err)
        return False
    elif (args.algo == 'a_star'):
        algo = Puzzle.E_Search.A_STAR
    elif (args.algo == 'uniform_cost'):
        algo = Puzzle.E_Search.UNIFORM_COST
    elif (args.algo == 'greedy'):
        algo = Puzzle.E_Search.GREEDY_SEARCH
    elif (args.algo == 'ida_star'):
        algo = Puzzle.E_Search.IDA_STAR
    Solver = Puzzle.Puzzle(puzzle, args, algo)
    err = Solver.launch_puzzle(args.hide, algo, args.boost)
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
