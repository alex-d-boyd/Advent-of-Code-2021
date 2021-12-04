#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 

import argparse
import pprint

from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 04')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def parse_input(puzzle_input):
    lines = puzzle_input.splitlines()
    order = map(int, lines.pop(0).split(','))
    lines = lines[1:]
    lines.append('')
    boards = {}
    board = []
    for line in lines:
        if line == '':
            board_set = frozenset(n[0] for line in board for n in line)
            boards[board_set] = [board, False]
            board = []
        else:
            board.append([[int(n), False] for n in line.split()])
    return order, boards

def call_number(n, boards):
    winners = []
    for board_set, board in boards.items():
        this_board_wins = False
        if not n in board_set:
            continue
        if board[1]:
            continue
        for line in board[0]:
            for num in line:
                if num[0] == n:
                    num[1] = True
                    if check_board(board[0]):
                        board[1] = True
                        winners.append(board_set)
                        this_board_wins = True
                        break
                if this_board_wins:
                    break
    return winners
                

def check_board(board):
    if any(all(n[1] for n in line) for line in board):
        return True
    if any(all(line[x][1] for line in board) for x in range(5)):
        return True
    return False

def score_board(board, last_num):
    board_score = sum(n[0] for line in board for n in line if not n[1])
    return last_num * board_score

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
        if winners := call_number(n, boards):
            if not first_winner:
                first_winner = winners[0]
                top_n = n
            if all(board[1] for board in boards.values()):
                last_winner = winners[0]
                last_n = n
                break

    top_board_score = score_board(boards[first_winner][0], top_n)
    last_board_score = score_board(boards[last_winner][0], last_n)
            
    print(f'Part 1: Winning board score = {top_board_score}')
    print(f'Part 2: Losing board score = {last_board_score}')
