import unittest
from kanu.equation import *


class EquationTests(unittest.TestCase):
    def test_solve_single_linear_equation(self):
        self.assertEqual(solve_single_linear_equation('x=x'), 'There are infinite solutions')
        self.assertEqual(solve_single_linear_equation(' x   =       x'), 'There are infinite solutions')
        self.assertRaises(NonLinearEquationError, lambda: solve_single_linear_equation('x^2 = 4'))
        self.assertRaises(NonLinearEquationError, lambda: solve_single_linear_equation('1/x = x'))
        self.assertEqual(solve_single_linear_equation('9x - 15 = 3'), 'x = 2')
        self.assertEqual(solve_single_linear_equation('5=-3x + 14'), 'x = 3')
        self.assertEqual(solve_single_linear_equation('4x + 2.8 = 6.4'), 'x = 0.9')
        self.assertEqual(solve_single_linear_equation('x / 7 - 4 = 5'), 'x = 63')
        self.assertEqual(solve_single_linear_equation('3(x+5) = 12'), 'x = -1')
        self.assertEqual(solve_single_linear_equation('13 - 4x = 3x - 8'), 'x = 3')
        self.assertEqual(solve_single_linear_equation('3(5q - 4) = 2(4q  + 6)'), 'q = 3.43')