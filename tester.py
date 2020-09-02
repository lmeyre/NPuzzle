#! /usr/bin/env python3

import time
import subprocess
import os
import sys
import argparse as arg
import re
import pandas as pd

# Colors
class c(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Npuzzle(object):

    def __init__(self, filename=None, algo_opt=None, heuristic_opt=None):
        self.time = 0
        self.cmd = "python3 main.py --hide {algo} {heuristic} {filename}".format(
            algo=algo_opt, heuristic=heuristic_opt, filename=filename if filename else "generated_puzzle.txt")
        self.algo = algo_opt
        self.h = heuristic_opt

    def parse_output(self):
        crash = re.search(
            r'End too long, total try =\s*([0-9]*)', self.out.decode())
        if crash:
            return {
                'nb_moves': None,
                'complexity_time': None,
                'complexity_size': None,
                'nb_loops': crash.group(1),
                'time': round(self.time, 3)
            }
        self.out_heuristic = re.search(
            r'Using heuristic :\s*([A-Z|_]*)', self.out.decode()).group(1)
        self.out_algo = re.search(
            r'Using algorithm :\s*([A-Z|_]*)', self.out.decode()).group(1)
        self.nb_moves = re.search(
            r'The original state was solved in\s*([0-9]*)', self.out.decode()).group(1)
        self.complexity_time = re.search(
            r'Complexity in time :\s*([0-9]*)', self.out.decode()).group(1)
        self.complexity_size = re.search(
            r'Complexity in size :\s*([0-9]*)', self.out.decode()).group(1)
        results = {
            'nb_moves': self.nb_moves,
            'complexity_time': self.complexity_time,
            'complexity_size': self.complexity_size,
            'time': round(self.time, 3)
        }
        return results

    def run(self):
        start_time = time.time()
        try:
            self.out = subprocess.check_output(
                self.cmd, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            print("Npuzzle returned an " + c.FAIL +
                  "error" + c.ENDC + ": %d" % exc.returncode)
            print(c.OKBLUE + "Npuzzle output :\n" + c.ENDC)
            print(exc.output.decode())
            sys.exit(1)
        self.time = time.time() - start_time


class Process(object):

    available_algorithms = {'a_star': ' -A a_star ', 'a_star_boost': ' -A a_star -b ', 'ida_star': '  -A ida_star ',
                            'greedy': ' -A greedy ', 'greedy_boost': ' -A greedy -b ', 'uniform_cost': ' -A uniform_cost ', 'uniform_cost_boost': ' -A uniform_cost -b '}
    # 0 = Manhattan
    # 1 = Out of place
    # 2 = Linear conflict
    # 3 = Corner Tiles
    available_heuristics = {0: ' -H 0 ', 1: ' -H 1 ', 2: ' -H 2 ', 3: ' -H 3 '}
    heuristics_named = {0: 'Manhattan', 1: 'Out of place',
                        2: 'Linear conflict', 3: 'Corner Tiles'}
    algo_named = {'a_star': 'A *', 'a_star_boost': 'A * boosted', 'ida_star': 'IDA *',
                  'greedy': 'Greedy search', 'greedy_boost': 'Greedy search boosted', 'uniform_cost': 'Uniform cost', 'uniform_cost_boost': 'Uniform cost boosted'}
    generator_cmd = 'python2 npuzzle-gen.py -s {size} > {filename}'

    def __init__(self, algo=None, heuristic=None):
        self.algorithms = {k: v for k,
                           v in self.available_algorithms.items() if k in algo}
        self.heuristics = {
            k: v for k, v in self.available_heuristics.items() if k in heuristic}

    def launch_loop(self, args):
        process_results = []
        row_names = {}
        print("Launching %s with heuristic %s : %d times" % (args.algo, args.heuristic, args.number))
        for i in range(args.number):
            print("Try %d" % i)
            filename = "puzzles/generated_puzzle_%d.txt" % i
            self.generate_puzzle(args, filename)
            for _, algo_v in self.algorithms.items():
                for _, h_v in self.heuristics.items():
                    n = Npuzzle(filename=filename, algo_opt=algo_v, heuristic_opt=h_v)
                    n.run()
                    row_names[i] = "Try %d" % i
                    process_results.append(n.parse_output())
        df = pd.DataFrame(process_results)
        df = df.rename(index=row_names)
        return df

    def launch(self, args):
        self.generate_puzzle(args, "generated_puzzle.txt")
        self.print_generated_puzzle()
        row_names = {}
        i = 0
        process_results = []
        for algo_key, algo_v in self.algorithms.items():
            for h_key, h_v in self.heuristics.items():
                print("Launching %s with heuristic %s" % (self.algo_named[algo_key], self.heuristics_named[h_key]))
                n = Npuzzle(filename="generated_puzzle.txt", algo_opt=algo_v, heuristic_opt=h_v)
                name = "[%s + %s]" % (self.algo_named[algo_key], self.heuristics_named[h_key])
                n.run()
                process_results.append(n.parse_output())
                row_names[i] = name
                i += 1
        df = pd.DataFrame(process_results)
        df = df.rename(index=row_names)
        return df

    def generate_puzzle(self, args, filename):
        if args.size and args.size >= 3:
            size = str(args.size)
        else:
            print("please enter a valid size")
            sys.exit(1)
        self.gen_filename = filename
        self.cmd = self.generator_cmd.format(size=size, filename=filename)
        # Exec the generator
        os.system(self.cmd)
        self.get_generated_puzzle()
        return self.get_generated_puzzle()

    def print_generated_puzzle(self):
        file = open(self.gen_filename)
        print(c.OKBLUE + "Tested file :\n" + c.ENDC)
        puzzle = file.read()
        print(puzzle)
        print(c.OKBLUE + "-----------\n" + c.ENDC)
        file.close()

    def get_generated_puzzle(self):
        file = open(self.gen_filename)
        puzzle = file.read()
        file.close()
        return puzzle


if __name__ == "__main__":
    parser = arg.ArgumentParser(description='This program solves n-puzzle')
    parser.add_argument("size", type=int, nargs='?',
                        help="Size of the puzzle's side. Must be >3.")
    parser.add_argument("-n", "--number", type=int, help="Number of times the tests will be done. Work only with one heuristic and one algo")
    parser.add_argument('-H', '--heuristic', nargs='+', type=int, choices=[0, 1, 2, 3], default=[0, 1, 2, 3],
                        help='The heuristic function to use : 0 = Manhattan (default), 1 = Out of place, 2 = Linear conflict, 3 = Corner Tiles')
    parser.add_argument('-A', '--algo', type=str, nargs='+', choices=['a_star', 'ida_star', 'greedy', 'uniform_cost', 'a_star_boost', 'greedy_boost', 'uniform_cost_boost'], default=['a_star', 'ida_star', 'greedy', 'uniform_cost', 'a_star_boost', 'greedy_boost', 'uniform_cost_boost'],
                        help='The algo type to use')
    parser.add_argument('-S', '--sort', type=str, choices=['nb_moves', 'complexity_time', 'complexity_size', 'time'],
                        help='Sort the table by a column name')
    args = parser.parse_args()

    p = Process(algo=args.algo, heuristic=args.heuristic)

    if args.number:
        if len(args.algo) == 1 and len(args.heuristic) == 1:
            df = p.launch_loop(args)
        else:
            print("Need 1 algo and 1 heuristic with the --number argument")
            sys.exit(1)
    else:
        df = p.launch(args)
    # Print in stdout
    print("Results:")
    if args.sort:
        if args.number:
            print("Sorting by ascending = False")
            df = df.sort_values(ascending=False, by=[args.sort])
        else:
            print("Sorting by ascending = True")
            df = df.sort_values(by=[args.sort])
    if args.number:
        print("The top 10")
        df = df.head(10)
    print(df.to_string())
