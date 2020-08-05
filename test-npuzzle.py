#! /usr/bin/env python3

import time
import subprocess
import os
import sys
import argparse as arg

class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def exec_npuzzle(options, h):
    start_time = time.time()
    cmd = "python3 main.py " + options
    try:
        out = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        print("Npuzzle returned an " + c.FAIL + "error" + c.ENDC + ": %d" % exc.returncode)
        print(c.OKBLUE + "Npuzzle output :\n" + c.ENDC)
        print(exc.output.decode())
        return None
    calc_time = time.time() - start_time
    print(("Npuzzle executed with the "+ c.OKBLUE + "heuristic" + c.ENDC + ": %d, " + c.OKBLUE + "time" + c.ENDC + ": %f" + c.ENDC) % (h, round(calc_time, 4)))
    print(c.OKBLUE + "Npuzzle output :\n" + c.ENDC)
    output = out.decode()
    print(output)
    print(c.OKBLUE + "-----------\n" + c.ENDC)
    # for line in out.splitlines():
    #     words = line.split()
    #     if words[0].decode() == "Finished":
    #         print("Number of " + c.OKBLUE + "loops returned" + c.ENDC + " : ", words[5].decode())
    return calc_time, output

def generate_puzzle(args):
    generator = "python npuzzle-gen.py "
    if args.unsolvable:
        generator += "-u "
    elif args.solvable:
        generator += "-s "
    if args.size and args.size >= 3:
        generator += str(args.size)
    else:
        print("please enter a valid size")
        sys.exit(1)
    generator += " > generated_puzzle.txt"
    os.system(generator)

    file = open("generated_puzzle.txt")
    print(c.OKBLUE + "Tested file :\n" + c.ENDC)
    puzzle = file.read()
    print(puzzle)
    print(c.OKBLUE + "-----------\n" + c.ENDC)
    file.close()
    return puzzle

if __name__ == "__main__":
    parser = arg.ArgumentParser(description='This program solves n-puzzle')
    parser.add_argument("size", type=int, nargs='?', help="Size of the puzzle's side. Must be >3.")
    parser.add_argument("-n", "--number", type=int, help="Number of times the tests will be done")
    parser.add_argument('-u', "--unsolvable", action="store_true", default=False)
    parser.add_argument('-s', "--solvable", action="store_true", default=False)
    parser.add_argument('-H', '--heuristic', type=int, choices=[0, 1, 2, 3],
                        help='The heuristic function to use : 0 = Manhattan (default), 1 = Out of place, 2 = Linear conflict, 3 = Corner Tiles')
    args = parser.parse_args()

    options = " generated_puzzle.txt "
    if args.heuristic:
        option = "-H " + str(args.heuristic) + options
        if args.number:
            puzzle_times = {}
            for i in range(args.number):
                puzzle = generate_puzzle(args)
                t, out = exec_npuzzle(options, args.heuristic)
                puzzle_times[round(t, 4)] = [puzzle, out]
            sorted_puzzle_times = {k: v for k, v in sorted(puzzle_times.items(), reverse=True)}
            print(c.WARNING + "RANK 3 SLOWER PUZZLES:" + c.ENDC)
            i = 0
            for key, value in sorted_puzzle_times.items():
                    print(c.WARNING + "Time :" + c.ENDC, key)
                    print(c.WARNING + "Puzzle :" + c.ENDC)
                    print(value[0], end='')
                    print(c.WARNING + "Output :" + c.ENDC, end='')
                    print(value[1])
                    print(c.WARNING + "-----------" + c.ENDC)
                    i += 1
                    if i >= 3:
                        break
        else:
            generate_puzzle(args)
            exec_npuzzle(options, args.heuristic)
    else:
        times = {}
        for i in range(4):
            generate_puzzle(args)
            option = "-H " + str(i) + options
            t = exec_npuzzle(option, i)
            if t:
                times[i] = t
        if len(times):
            print(c.OKBLUE + "Ranking in time of execution:" + c.ENDC)
            for i in sorted(times.items(), key=lambda item: item[1]):
                print("[%d]: %fsec" % (i[0], i[1]))
        
