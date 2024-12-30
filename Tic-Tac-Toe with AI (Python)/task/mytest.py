import io
from textwrap import dedent
from unittest import TestCase
from unittest.mock import patch

import tictactoe


class Test(TestCase):
    ################
    # part 1 tests #
    ################
    @patch('builtins.input', side_effect=['_XXOO_OX_', '3 3'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_mine(self, mock_stdout, mock_input):
        try:
            tictactoe.init_cells()
            tictactoe.main()
        except StopIteration:
            pass

        output = mock_stdout.getvalue()
        expected = dedent("""\
            ---------
            |   X X |
            | O O   |
            | O X X |
            ---------
            Game not finished""")
        self.assertIn(expected, output)

    @patch('builtins.input', side_effect=['_XXOO_OX_', '1 1'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_main_test1(self, mock_stdout, mock_input):
        try:
            tictactoe.main()
        except StopIteration:
            pass

        output = mock_stdout.getvalue()
        expected = dedent("""\
            ---------
            | X X X |
            | O O   |
            | O X   |
            ---------
            X wins""")
        self.assertIn(expected, output)
