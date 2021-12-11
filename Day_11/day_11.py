#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 11: Dumbo Octopus 

import argparse

from pathlib import Path

DELTAS = (
    (-1,  0), # N
    (-1,  1), # NE
    ( 0,  1), # E
    ( 1,  1), # SE
    ( 1,  0), # S
    ( 1, -1), # SW
    ( 0, -1), # W
    (-1, -1), # NW
    )
    

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def adjacents(r, c, rows, cols):
    return [(r2, c2) for dr, dc in DELTAS
            if 0 <= (r2 := r+dr) < rows and 0 <= (c2 := c+dc) < cols]

def process_step(matrix):
    flashed = set()
    flashers = set()
    rows, cols = len(matrix), len(matrix[0])
    for r in range(rows):
        for c in range(cols):
            matrix[r][c] += 1
            if matrix[r][c] > 9:
                flashers.add((r, c))
    while flashers:
        flash = flashers.pop()
        flashed.add(flash)
        adjs = adjacents(*flash, rows, cols)
        for r, c in adjs:
            if (r, c) in flashed:
                continue
            matrix[r][c] += 1
            if matrix[r][c] > 9:
                flashers.add((r, c))
    for r, c in flashed:
        matrix[r][c] = 0
    return len(flashed)

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')

    octopus_matrix = [list(map(int,list(line)))
                      for line in puzzle_input.splitlines()]
    octopus_count = len(octopus_matrix) * len(octopus_matrix[0])

    total_flashes = 0
    for i in range(100):
        total_flashes += process_step(octopus_matrix)

    while True:
        i += 1
        if process_step(octopus_matrix) == octopus_count:
            break

    print(f'Part 1: There were a total of {total_flashes} flashes')
    print(f'Part 2: The first step where all flash was {i+1}')
