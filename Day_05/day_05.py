#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 

import argparse

from collections import Counter
from math import gcd
from pathlib import Path

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def shift(self, delta):
        x = self.x + delta[0]
        y = self.y + delta[1]
        return Point(x, y)

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'Line({self.start!r}, {self.end!r})'

    def __str__(self):
        return f'{self.start} -> {self.end})'

    def is_vertical(self):
        return self.start.x == self.end.x

    def is_horizontal(self):
        return self.start.y == self.end.y

    def slope(self):
        delta_x = self.end.x - self.start.x
        delta_y = self.end.y - self.start.y
        cd = gcd(delta_x, delta_y)
        dx = delta_x // cd
        dy = delta_y // cd
        return (dx, dy)

    def points_covered(self):
        slope = self.slope()
        x = self.start.x
        y = self.start.y
        current = Point(x, y)
        points = [current]
        while current != self.end:
            current = current.shift(slope)
            points.append(current)
        return points

    @classmethod
    def from_str(cls, line_string):
        start_coords, end_coords = line_string.split(' -> ')
        start_coords = map(int,start_coords.split(','))
        end_coords = map(int,end_coords.split(','))
        start = Point(*start_coords)
        end = Point(*end_coords)
        return cls(start, end)

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
    puzzle_input = in_file.read_text(encoding='utf-8').splitlines()

    lines = [Line.from_str(l) for l in puzzle_input]
    
    h_v_point_counter = Counter()
    all_point_counter = Counter()
    for line in lines:
        points = line.points_covered()
        all_point_counter.update(points)
        if line.is_vertical() or line.is_horizontal():
            h_v_point_counter.update(points)

    h_v_crosses = [p for p in h_v_point_counter if h_v_point_counter[p] >= 2]
    all_crosses = [p for p in all_point_counter if all_point_counter[p] >= 2]
    
    print(f'Part 1: Points with at least two vents: {len(h_v_crosses)}')
    print(f'Part 2: Points with at least two vents: {len(all_crosses)}')
