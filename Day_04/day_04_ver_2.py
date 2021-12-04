#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 4: Giant Squid

import argparse

from pathlib import Path

class Cell:
    def __init__(self, n):
        self.value = int(n)
        self.called = False

    def __repr__(self):
        return f'Cell({self.value})'

    def __str__(self):
        return f'{"O" if self.called else "X"} {self.value:>2}'

    def call(self):
        self.called = True

class Board:
    def __init__(self, *numbers):
        self.numbers = list(numbers)
        self.set = set(self.numbers)
        self.layout = tuple(numbers[i:i+5] for i in range(0, 25, 5))
        self.called_layout = [[Cell(n) for n in line] for line in self.layout]
        self.won = False

    def __repr__(self):
        return f'Board({", ".join(map(str, self.numbers))})'

    def __str__(self):
        return '\n'.join(' '.join(str(cell) for cell in line)
                         for line in self.called_layout)

    def __bool__(self):
        return True

    def call_number(self, n):
        if self.won:
            return False
        if not n in self.set:
            return False
        for line in self.called_layout:
            for cell in line:
                if cell.value == n:
                    cell.call()
                    if self.check_board():
                        self.last_number = n
                        self.score_board()
                    return True
        return False

    def check_board(self):
        if self.won:
            return True
        if any(all(cell.called for cell in line) for line in self.called_layout):
            self.won = True
            return True
        if any(all(line[x].called for line in self.called_layout)
                                  for x in range(5)):
            self.won = True
            return True
        return False

    def score_board(self):
        if not self.won:
            return None
        self.board_score = sum(cell.value for line in self.called_layout
                               for cell in line if not cell.called)
        self.total_score = self.board_score * self.last_number

    @classmethod
    def from_layout(cls, string):
        numbers = [int(n) for line in string.splitlines() for n in line.split()]
        return cls(*numbers)

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 04')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(puzzle_input):
    split = puzzle_input.split('\n\n', 1)
    order = map(int, split[0].split(','))
    layouts = split[1].split('\n\n')
    boards = [Board.from_layout(layout) for layout in layouts]
    return order, boards


if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')

    order, boards = parse_input(puzzle_input)

    print(f'Got {len(boards)} boards')
    first_winner = None
    for n in order:
        for board in boards:
            if board.call_number(n):
                if board.won and not first_winner:
                    first_winner = board
                if all(board.won for board in boards):
                    last_winner = board
                    break

    print(f'Part 1: Winning board score = {first_winner.total_score}')
    print(f'Part 2: Losing board score = {last_winner.total_score}')
