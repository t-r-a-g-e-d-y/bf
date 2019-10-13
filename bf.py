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
    if data[dataptr] in range(0,256):
        print(chr(data[dataptr]), end='')
    else:
        print(data[dataptr], end='')

def get_input():
    global data
    byte = input('>>> ')
    if not byte:
        return
    else:
        try:
            data[dataptr] = int(byte)
        except ValueError:
            data[dataptr] = ord(byte[0])

def jump_forward(program, index):
    count = 0
    if data[dataptr] == 0:
        index += 1
        while True:
            if program[index] == '[':
                count += 1
            elif program[index] == ']' and count > 0:
                count -= 1
            elif program[index] == ']':
                break
            index += 1

    return index + 1

def jump_backward(program, index):
    count = 0
    if data[dataptr] != 0:
        index -= 1
        while True:
            if program[index] == ']':
                count += 1
            elif program[index] == '[' and count > 0:
                count -= 1
            elif program[index] == '[':
                break
            index -= 1

    return index + 1

symbols = {
    '>': incr_ptr,
    '<': decr_ptr,
    '+': incr_data,
    '-': decr_data,
    '.': print_byte,
    ',': get_input,
    '[': jump_forward,
    ']': jump_backward,
}

def read_program(fn):
    pass

def build_jump_pairs(program):
    pass

if __name__ == '__main__':
    import sys

    with open(sys.argv[1], 'r') as f:
        program = f.read()

    index = 0
    while True:
        if index >= len(program):
            exit()

        c = program[index]

        if c in '\r\n':
            index += 1
            continue

        symbol = symbols.get(c)

        if not symbol:
            pass
        elif c in '[]':
            index = symbol(program, index)
            continue
        else:
            symbol()

        index += 1

