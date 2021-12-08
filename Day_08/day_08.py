#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 8: Seven Segment Search 

import argparse

from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='AoC 2021 Day 01')
    parser.add_argument('-t', '--test', help='use test data', action='store_true')
    args = parser.parse_args()
    return args

def diff(a, b):
    return ''.join(sorted(char for char in a if char not in b))

def identify_digits(seg_list):
    digits = dict(zip([0,1,2,3,4,5,6,7,8,9], [None]*10, strict=True))
    digits[1] = seg_list[0]
    digits[7] = seg_list[1]
    digits[4] = seg_list[2]
    digits[8] = 'abcdefg'
    assert digits[8] == seg_list[-1]
    digits[9] = [segs for segs in seg_list if len(segs) == 6 and
                               all(c in segs for c in digits[4])][0]
    top = diff(digits[7], digits[4])
    bot = diff(diff(digits[9], digits[4]), top)
    ll = diff(digits[8], digits[9])
    digits[3] = [segs for segs in seg_list if len(segs) == 5 and
                               all(c in segs for c in digits[1])][0]
    mid = diff(digits[3], digits[1] + top + bot)
    digits[0] = diff(digits[8], mid)
    digits[6] = [segs for segs in seg_list if len(segs) == 6 and
                               segs not in digits.values()][0]
    digits[5] = diff(digits[6], ll)
    digits[2] = [segs for segs in seg_list if segs not in digits.values()][0]
    digits_look_up = {v: k for k, v in digits.items()}
    return digits_look_up

if __name__ == '__main__':
    args = parse_args()
    if args.test:
        in_file = Path('test.txt')
    else:
        in_file = Path('input.txt')
    puzzle_input = in_file.read_text(encoding='utf-8').splitlines()

    inputs = []
    outputs = []
    for line in puzzle_input:
        inp, _, out = line.partition(' | ')
        inputs.append(sorted([''.join(sorted(list(word)))
                              for word in inp.split()], key=len))
        outputs.append([''.join(sorted(list(word))) for word in out.split()])
    result = sum(len(out_digit) in [7, 3, 4, 2]
                 for out in outputs for out_digit in out)
    print(f'Part 1: total outputs unique: {result}')

    total = 0
    for inp, out in zip(inputs, outputs):
        digits_look_up = identify_digits(inp)
        output = int(''.join(map(str,(digits_look_up[o] for o in out))))
        total += output
    print(f'Part 2: Sum of output values = {total}')
