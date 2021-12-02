#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 1: Sonar Sweep

import argparse

from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def count_increases(seq):
    """Count the number of elements in a sequece greater than the previous"""
    increases = 0
    for i in range(1, len(seq)):
        if seq[i] > seq[i-1]:
            increases += 1
    return increases

def windowise(seq):
    windows = []
    for i in range(3, len(seq)+1):
        windows.append(sum(seq[i-3:i]))
    return windows

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')

    seq = list(map(int, puzzle_input.splitlines()))
    
    p1_incs = count_increases(seq)
    print(f'Part 1: Number of increasing elements is: {p1_incs}')

    p2_incs = count_increases(windowise(seq))
    print(f'Part 2: Number of increasing elements is: {p2_incs}')

    
