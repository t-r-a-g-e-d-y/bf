import sys
import unittest

from io import StringIO

import bf

class BFTest(unittest.TestCase):
    def setUp(self):
        self.bfm = bf.BFMachine()
        self.test_program_file = 'programs/helloworld_commented.bf'
        self.program = bf.read_program(self.test_program_file)
        self.jump_pairs = bf.build_jump_pairs(self.program)

    def test_incr_ptr(self):
        bf.incr_ptr(self.bfm)
        self.assertEqual(self.bfm.dataptr, 1)

    def test_decr_ptr(self):
        self.bfm.dataptr = 1
        bf.decr_ptr(self.bfm)
        self.assertEqual(self.bfm.dataptr, 0)

    def test_decr_ptr_exit(self):
        with self.assertRaises(SystemExit):
            bf.decr_ptr(self.bfm)

    def test_incr_data(self):
        bf.incr_data(self.bfm)
        self.assertEqual(self.bfm.data[0], 1)

    def test_decr_data(self):
        bf.decr_data(self.bfm)
        self.assertEqual(self.bfm.data[0], 255)

    def test_read_program(self):
        with open(self.test_program_file, 'r') as f:
            bfp = [[c, bf.commands.get(c)] for c in f.read().strip() if c in bf.commands.keys()]
        self.assertEqual(bf.read_program(self.test_program_file), bfp)

    def test_build_jump_pairs(self):
        program = ['[', ']']
        pairs = {'opening': {0: 1}, 'closing': {1: 0}}
        self.assertEqual(bf.build_jump_pairs(program), pairs)

    @unittest.skip('Test code not implemented')
    def test_jump_forward(self):
        pass

    @unittest.skip('Test code not implemented')
    def test_jump_backward(self):
        pass

    def test_bf_run(self):
        expected_output = "Hello World!\n"
        captured_output = StringIO()
        sys.stdout = captured_output

        bf.bf_run(self.bfm, self.program, self.jump_pairs)
        self.assertEqual(captured_output.getvalue(), expected_output)

        captured_output.close()
        sys.stdout = sys.__stdout__

class BFTestPrograms(unittest.TestCase):
    def setUp(self):
        self.captured_output = StringIO()
        sys.stdout = self.captured_output
        self.bfm = bf.BFMachine()

    def tearDown(self):
        self.captured_output.close()
        sys.stdout = sys.__stdout__

    @unittest.skip('Long running test')
    def test_array_length(self):
        program = bf.read_program('tests/array_length.bf')
        jump_pairs = bf.build_jump_pairs(program)

        expected_output = '#\n'

        bf.bf_run(self.bfm, program, jump_pairs)
        self.assertEqual(self.captured_output.getvalue(), expected_output)

    def test_mismatched_rb(self):
        program = bf.read_program('tests/mismatched_rb.bf')
        with self.assertRaises(IndexError):
            bf.build_jump_pairs(program)

    def test_mismatched_lb(self):
        program = bf.read_program('tests/mismatched_lb.bf')
        with self.assertRaises(IndexError):
            bf.build_jump_pairs(program)

    def test_obscure(self):
        program = bf.read_program('tests/obscure.bf')
        jump_pairs = bf.build_jump_pairs(program)

        expected_output = 'H\n'

        bf.bf_run(self.bfm, program, jump_pairs)
        self.assertEqual(self.captured_output.getvalue(), expected_output)

    def test_rot13(self):
        program = bf.read_program('programs/rot13.bf')
        jump_pairs = bf.build_jump_pairs(program)

        program_input = '~mlk zyx\n'
        expected_output = '~zyx mlk\n'

        with StringIO(initial_value=program_input) as f:
            self.bfm = bf.BFMachine(input_source=f)

        bf.bf_run(self.bfm, program, jump_pairs)
        self.assertEqual(self.captured_output.getvalue(), expected_output)

    def test_quine(self):
        quine = 'programs/quine.bf'
        with open(quine) as f:
            expected_output = f.read().strip()

        program = bf.read_program(quine)
        jump_pairs = bf.build_jump_pairs(program)

        bf.bf_run(self.bfm, program, jump_pairs)
        self.assertEqual(self.captured_output.getvalue(), expected_output)

    def test_newline_eof_input(self):
        program = bf.read_program('tests/newline_eof.bf')
        jump_pairs = bf.build_jump_pairs(program)

        program_input = '\n'
        expected_output = 'LK\nLK\n'

        with StringIO(initial_value=program_input) as f:
            self.bfm = bf.BFMachine(f)

        bf.bf_run(self.bfm, program, jump_pairs)
        self.assertEqual(self.captured_output.getvalue(), expected_output)

if __name__ == '__main__':
    unittest.main()

