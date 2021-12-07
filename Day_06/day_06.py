#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 6: Lanternfish 

import argparse

from collections import Counter
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def brute_force(start, days):
    school = start[:]
    for _ in range(days):
        for i in range(len(school)):
            if school[i] == 0:
                school[i] = 6
                school.append(8)
            else:
                school[i] -= 1
    return len(school)

def count_fish(start, days, debug=False):
    counter = Counter(start)
    add_in_two = 0
    add_in_one = 0
    for i in range(days):
        temp = add_in_one
        add_in_one = add_in_two
        add_in_two = counter[i % 7]
        counter[i % 7] += temp
    return counter.total() + add_in_one + add_in_two

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    puzzle_input = list(map(int,puzzle_input.splitlines()[0].split(',')))

    num = count_fish(puzzle_input, 80)
    print(f'Part 1: Number of lanternfish after 80 days: {num}')

    num = count_fish(puzzle_input, 256)
    print(f'Part 1: Number of lanternfish after 256 days: {num}')


