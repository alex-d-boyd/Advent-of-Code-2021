#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 13: Transparent Origami

import argparse

from pathlib import Path

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

    
    points = set()
    folds = []
    for line in puzzle_input:
        if line.startswith('fold'):
            fold = line.replace('fold along ','')
            ax, _, val = fold.partition('=')
            fold = (ax, int(val))
            folds.append(fold)
        elif line == '':
            continue
        else:
            point = tuple(map(int, line.split(',')))
            points.add(point)

    for i, fold in enumerate(folds):
        remove = set()
        new  = set()
        match fold:
            case ['x', x_ax]:
                for point in points:
                    x, y = point
                    if x > x_ax:
                        new_point = (x - (2 * (x - x_ax)), y)
                        new.add(new_point)
                        remove.add(point)
            case ['y', y_ax]:
                for point in points:
                    x, y = point
                    if y > y_ax:
                        new_point = (x, y - (2 * (y - y_ax)))
                        new.add(new_point)
                        remove.add(point)
        points.update(new)
        points.difference_update(remove)
        if i == 0:
            print(f'Part 1: There are {len(points)} points after one fold')

    max_x = max(point[0] for point in points) + 1
    max_y = max(point[1] for point in points) + 1

    print('Part 2: The code is:')
    for y in range(max_y):
        for x in range(max_x):
            if (x, y) in points:
                print('#', end='')
            else:
                print('.', end='')
        print()
