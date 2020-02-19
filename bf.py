class BFMachine:
    def __init__(self):
        self.data = [0 for _ in range(30000)]
        self.dataptr = 0

def incr_ptr(bf):
    bf.dataptr += 1
    if bf.dataptr >= len(bf.data):
        bf.data.extend([0 for _ in range(30000)])

def decr_ptr(bf):
    bf.dataptr -= 1

def incr_data(bf):
    bf.data[bf.dataptr] += 1

def decr_data(bf):
    bf.data[bf.dataptr] -= 1

def print_byte(bf):
    try:
        print(chr(bf.data[bf.dataptr]), end='')
    except ValueError:
        print(bf.data[bf.dataptr], end='')

def get_input(bf):
    try:
        byte = f'{input(">>> ")}\n'
    except EOFError:
        # don't modify data on EOF
        print()
        return

    try:
        bf.data[bf.dataptr] = int(byte)
    except ValueError:
        bf.data[bf.dataptr] = ord(byte[0])

def jump_forward(bf, index, jump_pairs):
    if bf.data[bf.dataptr] == 0:
        index = jump_pairs['opening'][index] + 1
    else:
        index += 1

    return index

def jump_backward(bf, index, jump_pairs):
    if bf.data[bf.dataptr] != 0:
        index = jump_pairs['closing'][index] + 1
    else:
        index += 1

    return index

symbols = {
    '>': incr_ptr,
    '<': decr_ptr,
    '+': incr_data,
    '-': decr_data,
    '.': print_byte,
    ',': get_input,
    '[': jump_forward,
    ']': jump_backward
}

def read_program(fn):
    with open(fn, 'r') as f:
        program = f.read()

    return [c for c in program if c in symbols.keys()]

def build_jump_pairs(program):
    stack = []
    opening_pairs = {}

    for idx, c in enumerate(program):
        if c == '[':
            stack.append(idx)
        elif c == ']':
            try:
                opening_pairs[stack.pop()] = idx
            except IndexError:
                raise IndexError(f'Mismatched ] bracket')

    if stack:
        raise IndexError(f'Mismatched [ bracket')

    closing_pairs = {k: v for k, v in zip(opening_pairs.values(), opening_pairs.keys())}
    return {'opening': opening_pairs, 'closing': closing_pairs}

if __name__ == '__main__':
    import sys

    try:
        program = read_program(sys.argv[1])
    except FileNotFoundError:
        print(f'File not found: {sys.argv[1]}')
        exit()

    try:
        jump_pairs = build_jump_pairs(program)
    except IndexError as err:
        print(err)
        exit()

    bf = BFMachine()

    index = 0
    while True:
        if index >= len(program):
            exit()

        c = program[index]

        symbol = symbols.get(c)

        if c in '[]':
            index = symbol(bf, index, jump_pairs)
            continue
        else:
            symbol(bf)

        index += 1

