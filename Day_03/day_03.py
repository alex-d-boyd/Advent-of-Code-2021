#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 3: Binary Diagnostic

import argparse

from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def find_gamma_and_epsilon(seq):
    gamma = epsilon = ''
    for place in range(len(seq[0])):
        mcb, lcb = most_least_common_bit(seq, place)
        gamma += mcb
        epsilon += lcb
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma, epsilon

def most_least_common_bit(seq, place):
    ones = ''.join(s[place] for s in seq).count('1')
    zeros = ''.join(s[place] for s in seq).count('0')
    if ones > zeros:
        return '1', '0'
    elif zeros > ones:
        return '0', '1'
    else:
        return'=', '='

def find_life_support(seq, o2=True):
    cseq = seq[:]
    place = 0
    while len(cseq) > 1:
        mcb, lcb = most_least_common_bit(cseq, place)
        if mcb == '=':
            mcb = '1'
            lcb = '0'
        keep = mcb if o2 else lcb
        cseq = [s for s in cseq if s[place] == keep]
        place += 1
    return int(cseq[0], 2)
        

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8')
    lines = puzzle_input.splitlines()

    gamma, epsilon = find_gamma_and_epsilon(lines)
    prod = gamma * epsilon
    print(f'Part 1: gamma = {gamma}, epsilon = {epsilon}, power = {prod}')

    o2 = find_life_support(lines)
    co2 = find_life_support(lines, o2=False)
    life = o2 * co2
    print(f'Part 2: O2 gen = {o2}, CO2 scrub = {co2}, life support = {life}')
