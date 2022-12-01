#! /usr/bin/env python3

# Advent of Code
# https://adventofcode.com/2021
# Day 16: Packet Decoder

import argparse

from itertools import count
from pathlib import Path

class Packet:
    MIN_LENGTH = 11
    
    def __init__(self, bit_stream):
        self.bit_stream = bit_stream
        self.hex_string = hex(int(bit_stream, 2))[2:]
        if len(self.hex_string) % 2:
            self.hex_string += '0'
        self.ver_bits = self.bit_stream[:3]
        self.type_bits = self.bit_stream[3:6]
        self.version = int(self.ver_bits, 2)
        self.type = int(self.type_bits, 2)

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.bit_stream}')"

    def __str__(self):
        return self.hex_string

    def __len__(self):
        return len(self.bit_stream)

    def is_valid(self):
        raise NotImplementedError('must be overridden')

    def version_sum(self):
        if isinstance(self, LiteralPacket):
            return self.version
        else:
            return self.version + sum(p.version_sum() for p in self.sub_packets)

    @classmethod
    def parse_hex(cls, hex_string):
        bit_stream = bin(int(hex_string, 16))[2:]
        while len(bit_stream) % 4:
            bit_stream = '0' + bit_stream
        return cls.parse(bit_stream)

    @classmethod
    def parse(cls, bit_stream):
        if len(bit_stream) < cls.MIN_LENGTH:
            raise ValueError('cannot parse stream; too short')
        type = int(bit_stream[3:6], 2)
        if type == 4: # Type 4 is a literal
            return LiteralPacket(bit_stream)
        else: # Must be an operator packet
            return OperatorPacket(bit_stream)

class LiteralPacket(Packet):
    MIN_LENGTH = 11

    def __init__(self, bit_stream):
        if len(bit_stream) < self.MIN_LENGTH:
            raise ValueError('too short')
        super().__init__(bit_stream)
        self.payload = self.bit_stream[6:]
        self._parse_value()
        if not self.is_valid():
            raise ValueError('bad packet')

    def _parse_value(self):
        chunks = [self.payload[i:i+5]
                  for i in range(0, len(self.payload), 5)]
        bin_val = ''
        used_chunks = ''
        for chunk in chunks:
            if chunk[0] == '1' and len(chunk) == 5:
                used_chunks += chunk
                bin_val += chunk[1:]
            elif chunk[0] == '0' and len(chunk) == 5:
                used_chunks += chunk
                bin_val += chunk[1:]
                break
            else:
                raise ValueError(
                    f'invalid chunk {chunk} in {self.payload}')
        self.value = int(bin_val, 2)
        self.chunklen = len([c for c in chunks if len(c)==5])
        self.tail = self.payload.removeprefix(used_chunks)
        self.payload = used_chunks

    def is_valid(self):
        if len(self.ver_bits) != 3:
            return False
        if self.type != 4 or len(self.type_bits) != 3:
            return False
        if self.tail and any(c != '0' for c in self.tail):
            return False
        if self.chunklen < 1:
            return False
        return True
        

class OperatorPacket(Packet):
    MIN_LENGTH = 29
    
    def __init__(self, bit_stream):
        if len(bit_stream) < self.MIN_LENGTH:
            raise ValueError('too short')
        super().__init__(bit_stream)
        self.length_id = int(self.bit_stream[6])
        self.sub_packets = []
        if self.length_id == 0: # 15 bits giving total bitlength of contents
            self.sub_packet_length = int(self.bit_stream[7:22], 2)
            self.sub_packet_count = None
            self.payload = self.bit_stream[22:22+self.sub_packet_length]
            self.tail = self.bit_stream[22+self.sub_packet_length:]
            if len(self.payload) != self.sub_packet_length:
                raise ValueError('bad packet')
        else: # 11 bits giving sub-packet count
            self.sub_packet_length = None
            self.sub_packet_count = int(self.bit_stream[7:18], 2)
            self.payload = self.bit_stream[18:]
            self.tail = None
            if len(self.payload) < Packet.MIN_LENGTH * self.sub_packet_count:
                raise ValueError('bad packet')
        self._find_sub_packets()
        
    def _find_sub_packets(self):
        stream_to_parse = self.payload
        while stream_to_parse and not (
            (self.sub_packet_count == len(self.sub_packets)) or
            (sum(len(p) for p in self.sub_packets) == self.sub_packet_length))
            next_packet_type = int(stream_to_parse[3:6], 2)
            if next_packet_type == 4:
                for i in count(LiteralPacket.MINLENGTH, 5):
                    try:
                        p = LiteralPacket(stream_to_parse[:i])
                    except:
                        continue
                self.sub_packets.append(p)
                stream_to_parse = stream_to_parse.removeprefix(p.bit_stream)
            else:
                next_packet_
        

    def is_valid(self):
        if len(self.ver_bits) != 3:
            return False
        if self.type == 4 or len(self.type_bits) != 3:
            return False
        if self.tail and any(c != '0' for c in self.tail):
            return False
        return True
    

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

    packet = Packet.parse_hex(puzzle_input)
    print(f'Part 1: The version sum is {packet.version_sum()}')
