import os
import stat
import sys

from collections import deque

class BFMachine:
    def __init__(self, input_source=sys.stdin, cell_size=8, debug_cell_count=20):
        self.data = [0 for _ in range(30000)]
        self.data_length = len(self.data)
        self.dataptr = 0
        self.input_buffer = deque()
        self.cell_max = 2 ** cell_size - 1

        # The below is so that input from a pipe or a file does not result in
        # the get_input prompt showing up while printing output or asking
        # the user for input after the input pipe/file has been read
        self.input_is_file_or_pipe = False
        input_mode = os.fstat(0).st_mode

        if input_source != sys.stdin or stat.S_ISFIFO(input_mode):
            self.input_is_file_or_pipe = True
            for c in input_source.read():
                self.input_buffer.append(ord(c))

        # Number of cells to print when # command is called in a program
        self.debug_cell_count = debug_cell_count

    @property
    def current_cell(self):
        return self.data[self.dataptr]

    @current_cell.setter
    def current_cell(self, value):
        self.data[self.dataptr] = value

def incr_ptr(bf):
    ''' > command '''
    bf.dataptr += 1
    if bf.dataptr >= bf.data_length:
        bf.data.extend([0 for _ in range(30000)])
        bf.data_length = len(bf.data)

def decr_ptr(bf):
    ''' < command '''
    bf.dataptr -= 1
    if bf.dataptr < 0:
        exit(f'Data pointer out of range ({bf.dataptr})')

def incr_data(bf):
    ''' + command '''
    if bf.current_cell >= bf.cell_max:
        bf.current_cell = 0
    else:
        bf.current_cell += 1

def decr_data(bf):
    ''' - command '''
    if bf.current_cell <= 0:
        bf.current_cell = bf.cell_max
    else:
        bf.current_cell -= 1

def print_byte(bf):
    ''' . command '''
    try:
        print(chr(bf.current_cell), end='')
    except ValueError:
        print(bf.current_cell, end='')

def debug(bf):
    ''' # command '''
    print(bf.data[:bf.debug_cell_count])
    print(f'Pointer value: {bf.dataptr}')

def get_input(bf):
    ''' , command '''
    if bf.input_buffer:
        bf.current_cell = bf.input_buffer.popleft()
    elif bf.input_is_file_or_pipe:
        # Empty input queue but program still has instructions to process
        # Handles a BF program asking for input on EOF
        return
    else:
        try:
            data = f'{input(">>> ")}\n'
        except EOFError:
            # don't modify data on EOF
            print()
            return

        bf.current_cell = ord(data[0])

        for c in data[1:]:
            bf.input_buffer.append(ord(c))

def jump_forward(bf, index, jump_pairs):
    ''' [ command '''
    if bf.current_cell == 0:
        index = jump_pairs['opening'][index] + 1
    else:
        index += 1

    return index

def jump_backward(bf, index, jump_pairs):
    ''' ] command '''
    if bf.current_cell != 0:
        index = jump_pairs['closing'][index] + 1
    else:
        index += 1

    return index

commands = {
    '>': incr_ptr,
    '<': decr_ptr,
    '+': incr_data,
    '-': decr_data,
    '.': print_byte,
    ',': get_input,
    '[': jump_forward,
    ']': jump_backward,
    '#': debug
}

def read_program(fn):
    with open(fn, 'r') as f:
        program = f.read()

    return [[c, commands.get(c)] for c in program if c in commands.keys()]

def build_jump_pairs(program):
    ''' Precompute [ and ] jump locations '''
    stack = []
    opening_pairs = {}

    for idx, c in enumerate(program):
        if c[0] == '[':
            stack.append(idx)
        elif c[0] == ']':
            try:
                opening_pairs[stack.pop()] = idx
            except IndexError:
                raise IndexError(f'Mismatched ] bracket')

    if stack:
        raise IndexError(f'Mismatched [ bracket')

    closing_pairs = {k: v for k, v in zip(opening_pairs.values(), opening_pairs.keys())}
    return {'opening': opening_pairs, 'closing': closing_pairs}

def bf_run(bfm, program, jump_pairs):
    index = 0
    program_length = len(program)

    while index < program_length:
        command, op = program[index]

        if command in '[]':
            index = op(bfm, index, jump_pairs)
        else:
            op(bfm)
            index += 1

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Program read from Brainfuck file')
    parser.add_argument('input', nargs='?', default=sys.stdin, type=argparse.FileType('r'), help='Read input from file')
    parser.add_argument('-c', '--cell-size', type=int, nargs='?', default=8, choices=[8, 16, 32], help='Cell size in bits')
    parser.add_argument('-d', '--debug', type=int, nargs='?', metavar="N", default=20, help='Number of cells to print when debug command is encountered')
    args = parser.parse_args()

    try:
        program = read_program(args.file)
    except FileNotFoundError:
        print(f'File not found: {args.file}')
        exit()

    try:
        jump_pairs = build_jump_pairs(program)
    except IndexError as err:
        print(err)
        exit()

    bfm = BFMachine(input_source=args.input, cell_size=args.cell_size, debug_cell_count=args.debug)

    try:
        bf_run(bfm, program, jump_pairs)
    except KeyboardInterrupt:
        print()
        exit()

