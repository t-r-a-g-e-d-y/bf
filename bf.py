class BFMachine:
    def __init__(self):
        self.data = [0 for _ in range(30000)]
        self.dataptr = 0

def incr_ptr(bf):
    ''' > command '''
    bf.dataptr += 1
    if bf.dataptr >= len(bf.data):
        bf.data.extend([0 for _ in range(30000)])

def decr_ptr(bf):
    ''' < command '''
    bf.dataptr -= 1

def incr_data(bf):
    ''' + command '''
    bf.data[bf.dataptr] += 1

def decr_data(bf):
    ''' - command '''
    bf.data[bf.dataptr] -= 1

def print_byte(bf):
    ''' . command '''
    try:
        print(chr(bf.data[bf.dataptr]), end='')
    except ValueError:
        print(bf.data[bf.dataptr], end='')

def get_input(bf):
    ''' , command '''
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
    ''' [ command '''
    if bf.data[bf.dataptr] == 0:
        index = jump_pairs['opening'][index] + 1
    else:
        index += 1

    return index

def jump_backward(bf, index, jump_pairs):
    ''' ] command '''
    if bf.data[bf.dataptr] != 0:
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
    ']': jump_backward
}

def read_program(fn):
    with open(fn, 'r') as f:
        program = f.read()

    return [c for c in program if c in commands.keys()]

def build_jump_pairs(program):
    ''' Precompute [ and ] jump locations '''
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

def bf_run(bfm, program, jump_pairs):
    index = 0

    while index < len(program):
        c = program[index]

        command = commands.get(c)

        if c in '[]':
            index = command(bfm, index, jump_pairs)
            continue
        else:
            command(bfm)

        index += 1

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

    bfm = BFMachine()

    bf_run(bfm, program, jump_pairs)

