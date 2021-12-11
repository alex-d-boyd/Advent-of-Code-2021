#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 9: Smoke Basin

import argparse

from collections import deque
from pathlib import Path

DELTAS = ((-1, 0), (0, 1), (1, 0), (0, -1))

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def scan_low_points(height_map):
    rows, cols = len(height_map), len(height_map[0])
    lows = []
    for r in range(rows):
        for c in range(cols):
            if all(height_map[r][c] < height_map[r2][c2]
                   for dr, dc in DELTAS
                   if 0 <= (r2 := r+dr) < rows and 0 <= (c2 := c+dc) < cols):
                lows.append(((r, c), height_map[r][c]))
    return lows

def find_basins(height_map, lows):
    def adjacents(point):
        r, c = point
        return [(r2, c2) for dr, dc in DELTAS
                if 0 <= (r2 := r+dr) < rows and 0 <= (c2 := c+dc) < cols]
    basins = []
    rows, cols = len(height_map), len(height_map[0])
    for low in lows:
        q = deque()
        q.append(low)
        basin = set()
        while q:
            point = q.popleft()
            r, c = point
            if height_map[r][c] != 9 and point not in basin:
                basin.add(point)
                q.extend(adjacents(point))
        basins.append(basin)
    return basins

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')

    height_map = [list(map(int,list(line)))
                  for line in puzzle_input.splitlines()]

    lows = scan_low_points(height_map)
    risk = sum(i + 1 for p, i in lows)
    print(f'Part 1: Total risk is {risk}')

    basins = sorted(find_basins(height_map, [p for p, i in lows])
                    , key=len, reverse=True)
    prod = len(basins[0]) * len(basins[1]) * len(basins[2])
    print(f'Part 2: Product of top three basins is {prod}')
