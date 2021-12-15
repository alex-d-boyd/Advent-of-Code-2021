#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 15: Chiton

import argparse
import heapq

from pathlib import Path

DELTAS = (
    (-1,  0), # N
    ( 0,  1), # E
    ( 1,  0), # S
    ( 0, -1), # W
    )

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def neighbours(node, rows, cols):
    r, c = node
    return [(r2, c2) for dr, dc in DELTAS
            if 0 <= (r2 := r + dr) < rows and 0 <= (c2 := c + dc) < cols]

def shortest_path_dijkstra(grid, source=(0, 0), target=None):
    rows, cols = len(grid), len(grid[0])
    if target is None:
        target = (rows-1, cols-1)

    to_visit = [(0, 0, 0)]
    risks = {}
    risks[source] = 0

    while to_visit and target not in risks:
        risk, r, c = heapq.heappop(to_visit)
        current_node = (r, c)

        for neighbour in neighbours(current_node, rows, cols):
            if neighbour not in risks:
                neighbour_risk = risk + grid[neighbour[0]][neighbour[1]]
                risks[neighbour] = neighbour_risk
                # We can do this here because the cost to enter a node
                # is the same no matter where we enter from.
                # So since we know (from Dijkstra) that the current node
                # risk is the minimum possible risk to that node,
                # the risk to the neighbour node must also be the
                # minimum risk for that node.
                heapq.heappush(to_visit, (neighbour_risk,
                                          neighbour[0], neighbour[1]))

    return risks[target]

def shortest_path(grid):
    """This doesn't work for all inputs.

    It is possible to have a minimum-risk path that requires moving up or left.
    E.G.
    19999
    11999
    91999
    11999
    19999
    11111
    """
    rows, cols = len(grid), len(grid[0])
    total_grid = [[0] * cols for _ in range(rows)]
    for c in range(1, cols):
        total_grid[0][c] = total_grid[0][c-1] + grid[0][c]
    for r in range(1, rows):
        total_grid[r][0] = total_grid[r-1][0] + grid[r][0]
        for c in range(1, cols):
            total_grid[r][c] = grid[r][c] + min(total_grid[r-1][c],
                                                total_grid[r][c-1])
    return total_grid[rows-1][cols-1]

def build_big_map(grid, dimension=5):
    big_grid = []
    for line in grid:
        new_line = line.copy()
        for i in range(dimension-1):
            new_line.extend([(x+i) % 9 + 1 for x in line])
        big_grid.append(new_line)
    add_lines = []
    for i in range(dimension-1):
        for line in big_grid:
            new_line = [(x+i) % 9 + 1 for x in line]
            add_lines.append(new_line)
    big_grid.extend(add_lines)
    return big_grid

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8').splitlines()

    risk_map = [list(map(int,list(line))) for line in puzzle_input]
    min_risk = shortest_path_dijkstra(risk_map)
    print(f'Part 1: Minimum-risk path has a total risk of {min_risk}')

    risk_map = build_big_map(risk_map)
    min_risk = shortest_path_dijkstra(risk_map)
    print(f'Part 2: Minimum-risk path has a total risk of {min_risk}')
