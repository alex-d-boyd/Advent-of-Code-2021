#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 12: Passage Pathing

import argparse

from collections import defaultdict
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def create_map(lines):
    cave_map = defaultdict(set)
    for line in lines:
        start, end = line.split('-')
        cave_map[start].add(end)
        cave_map[end].add(start)
    return cave_map

def depth_first_all(paths, graph, current, visited=None, part=1):
    if visited is None:
        visited = []
    visited.append(current)
    if current == 'end':
        if visited not in paths:
            paths.append(visited)
        return
    for vertex in graph[current]:
        if (vertex not in visited or
            ok_to_revisit(vertex, part, visited)):
            depth_first_all(paths, graph, vertex, visited.copy(), part)

def ok_to_revisit(vertex, part, visited):
    if part == 1:
        if vertex.isupper():
            return True
        else:
            return False
    elif part == 2:
        if vertex.isupper():
            return True
        elif vertex in ['start', 'end']:
            return False
        else:
            revisited_small_before = any(visited.count(v) >= 2
                                         for v in visited
                                         if v.islower())
            return not revisited_small_before

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8').splitlines()

    cave_map = create_map(puzzle_input)

    paths = []
    depth_first_all(paths, cave_map, 'start')

    print(f'Part 1: There are {len(paths)} paths available.')

    paths = []
    depth_first_all(paths, cave_map, 'start', part=2)

    print(f'Part 2: There are {len(paths)} paths available.')
