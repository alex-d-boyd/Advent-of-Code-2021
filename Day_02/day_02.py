#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 2: Dive!

import argparse

from pathlib import Path

class Position:    
    def __init__(self, horz=0, depth=0, aim=0):
        self.horz = int(horz)
        self.depth = int(depth)
        self.aim = int(aim)

    def __repr__(self):
        return f'Position(horz={self.horz}, depth={self.depth}, aim={self.aim})'

    def __str__(self):
        return f'Horizontal Pos: {self.horz}\nDepth: {self.depth}'

    def move_forward(self, x, part):
        self.horz += int(x)
        if part == 2:
            self.depth += self.aim * int(x)

    def move_up(self, u, part):
        if part == 1:
            self.depth -= int(u)
        elif part == 2:
            self.aim -= int(u)
        else:
            raise ValueError(f'unknown part {part}')

    def move_down(self, d, part):
        if part == 1:
            self.depth += int(d)
        elif part == 2:
            self.aim += int(d)
        else:
            raise ValueError(f'unknown part {part}')

    def process_course(self, course, part):
        for line in course.splitlines():
            match line.split():
                case ['forward', x]:
                    self.move_forward(x, part)
                case ['up', x]:
                    self.move_up(x, part)
                case ['down', x]:
                    self.move_down(x, part)
                case _:
                    raise ValueError(f'cannot process command "{line}"')

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')

    part1_pos = Position()
    part1_pos.process_course(puzzle_input, part=1)

    
    part2_pos = Position()
    part2_pos.process_course(puzzle_input, part=2)

    print(part1_pos)
    print(f'Product: {part1_pos.horz * part1_pos.depth}')

    print()

    print(part2_pos)
    print(f'Product: {part2_pos.horz * part2_pos.depth}')
