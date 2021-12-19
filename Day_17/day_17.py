#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 17: Trick Shot 

import argparse

from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args



if __name__ == '__main__':
    args = parse_args()
    # Cannot be bothered writing a parser for this
    if args.test:
        # target area: x=20..30, y=-10..-5
        x_target = range(20, 31)
        y_target = range(-10, -4)
    else:
        # target area: x=79..137, y=-176..-117
        x_target = range(79, 138)
        y_target = range(-176, -116)

    # If initial y vel is >= the min of the target area (abs), it will
    # overshoot, no matter what the x velocity is
    max_y_vel = abs(min(y_target)) - 1
    max_y_pos = max_y_vel * (max_y_vel + 1) // 2
    print(f'Part 1: The maximum height acheivable is {max_y_pos}')

    # If the initial y velocity is greater in magnitude than the bottom edge
    # of the target area, it can never end up inside
    min_y_vel = min(y_target)

    # If the initial x velocity is greater in magnitude than the right edge
    # of the target area, it can never end up inside
    max_x_vel = max(x_target)

    # Minimum initial x velocity must enter the target area after x velocity
    # is reduced to 0 by drag:
    # i.e. min_x_vel * (min_x_vel +1) // 2 >= min(x_target)
    for i in range(min(x_target)):
        if i * (i + 1) // 2 >= min(x_target):
            min_x_vel = i
            break

    initial_vels = set()
    for init_y_vel in range(min_y_vel, max_y_vel + 1):
        for init_x_vel in range(min_x_vel, max_x_vel + 1):
            y_vel, y_pos = init_y_vel, 0
            x_vel, x_pos = init_x_vel, 0

            while True:
                x_pos += x_vel
                y_pos += y_vel
                x_vel = max(x_vel - 1, 0)
                y_vel -= 1

                if x_pos in x_target and y_pos in y_target:
                    initial_vels.add((init_x_vel, init_y_vel))
                    break
                elif x_pos > max(x_target) or y_pos < min(y_target):
                    break
                else:
                    continue

    print(f'Part 2: There are {len(initial_vels)} possible initial velocities')
