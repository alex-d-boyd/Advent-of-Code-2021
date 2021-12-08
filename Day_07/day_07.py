#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 7: The Treachery of Whales 

import argparse

from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def fuel(a, b):
    return (d := abs(a - b)) * (d + 1) // 2


if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8').splitlines()

    positions = list(map(int, puzzle_input[0].split(',')))

    min_fuel_part_1 = float('inf')
    min_fuel_part_2 = float('inf')
    for alignment in range(min(positions), max(positions)+1):
        fuel_part_1 = sum(abs(alignment - position) for position in positions)
        if fuel_part_1 < min_fuel_part_1:
            min_fuel_part_1 = fuel_part_1
            min_pos_part_1 = alignment
        fuel_part_2 = sum(fuel(alignment, position) for position in positions)
        if fuel_part_2 < min_fuel_part_2:
            min_fuel_part_2 = fuel_part_2
            min_pos_part_2 = alignment

    print(f'Part 1: Minimum fuel required is {min_fuel_part_1} at position {min_pos_part_1}')
    print(f'Part 1: Minimum fuel required is {min_fuel_part_2} at position {min_pos_part_2}')
