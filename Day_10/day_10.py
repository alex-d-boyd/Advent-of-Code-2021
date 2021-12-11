#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 10: Syntax Scoring 

import argparse

from collections import deque
from enum import Enum, auto
from pathlib import Path

SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
    }

class Status(Enum):
    CORRUPT = auto()
    INCOMPLETE = auto()

def score_autocomplete(line):
    scores = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
        }
    score = 0
    for token in line:
        score *= 5
        score += scores[token]
    return score

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_line(line):
    openers = '([{<'
    closers = ')]}>'
    flips = dict(zip(closers, openers))
    flips.update(dict(zip(openers, closers)))
    stack = deque()
    for token in line:
        if token in openers:
            stack.append(token)
        elif token in closers:
            if stack[-1] == flips[token]:
                _ = stack.pop()
            else:
                return Status.CORRUPT, SCORES[token]
    completer = ''
    while stack:
        completer += flips[stack.pop()]
    return Status.INCOMPLETE, score_autocomplete(completer)
    

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8').splitlines()

    corrupt_score = 0
    incomplete_scores = []
    for line in puzzle_input:
        status, line_score = parse_line(line)
        if status == Status.CORRUPT:
            corrupt_score += line_score
        else:
            incomplete_scores.append(line_score)
    incomplete_scores.sort()
    incomplete_score = incomplete_scores[len(incomplete_scores) // 2]
    
    print(f'Part 1: The total syntax error score is {corrupt_score}')
    print(f'Part 2: The middle autocomplete score is {incomplete_score}')
