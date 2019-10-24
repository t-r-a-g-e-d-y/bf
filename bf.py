data = [0] * 30000
dataptr = 0

def incr_ptr():
    global data, dataptr
    dataptr += 1
    if dataptr >= len(data):
        data.extend([0] * 30000)

def decr_ptr():
    global dataptr
    dataptr -= 1

def incr_data():
    global data
    data[dataptr] += 1

def decr_data():
    global data
    data[dataptr] -= 1

def print_byte():
    try:
        print(chr(data[dataptr]), end='')
    except ValueError:
        print(data[dataptr], end='')

def get_input():
    global data
    try:
        byte = f'{input(">>> ")}\n'
    except EOFError:
        # don't modify data on EOF
        print()
        return

    try:
        data[dataptr] = int(byte)
    except ValueError:
        data[dataptr] = ord(byte[0])

def jump_forward(index, jump_pairs):
    if data[dataptr] == 0:
        index = jump_pairs['opening'][index] + 1
    else:
        index += 1

    return index

def jump_backward(index, jump_pairs):
    if data[dataptr] != 0:
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

    index = 0
    while True:
        if index >= len(program):
            exit()

        c = program[index]

        symbol = symbols.get(c)

        if c in '[]':
            index = symbol(index, jump_pairs)
            continue
        else:
            symbol()

        index += 1

