#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 14: Extended Polymerization

import argparse

from collections import Counter
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def naive_polymerise(template, steps):
    for _ in range(steps):
        new = template[0]
        for i in range(2, len(template)+1):
            chunk = template[i-2:i]
            new += mapping[chunk] + chunk[1]
        template = new

    counter = Counter(template)
    return counter

def polymerise(template, steps):
    elements = Counter(template)
    chunks = Counter(template[i-2:i] for i in range(2, len(template)+1))
    for _ in range(steps):
        new_chunks = Counter()
        removed_chunks = Counter()
        for chunk in chunks:
            add = mapping[chunk]
            elements[add] += chunks[chunk]
            removed_chunks[chunk] += chunks[chunk]
            new1 = chunk[0] + add
            new2 = add + chunk[1]
            new_chunks[new1] += chunks[chunk]
            new_chunks[new2] += chunks[chunk]
        chunks.subtract(removed_chunks)
        chunks.update(new_chunks)
        assert elements.total() - chunks.total() == 1
    return elements

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8').splitlines()

    template = puzzle_input.pop(0)
    mapping = {}
    for line in puzzle_input[1:]:
        comb, add = line.split(' -> ')
        mapping[comb] = add
    
    
    counter = polymerise(template, 10)
    counts = counter.most_common()
    print(f'Part 1: Most common - least common is {counts[0][1]-counts[-1][1]}')

    counter = polymerise(template, 40)
    counts = counter.most_common()
    print(f'Part 2: Most common - least common is {counts[0][1]-counts[-1][1]}')
