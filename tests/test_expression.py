import unittest
from kanu.expression import *


class ExpressionTests(unittest.TestCase):
    def test_operator_list(self):
        o1 = OperatorList(Element('1'), Element('5a'), Element('6a'), operation='+')
        o2 = OperatorList(Element('10'), Element('a^2'), Element('8'), Element('7a^2'), operation='-')
        o3 = OperatorList(Element('4'), Element('4'), Element('ab'), operation='*')
        o4 = OperatorList(Element('10a'), Element('b'), Element('2a'), operation='/')

        self.assertEqual(o1.members, [Element('1'), Element('11a')])
        self.assertEqual(o2.members, [Element('2'), Element('-8a^2')])
        self.assertEqual(o3.members, [Element('16ab')])
        self.assertEqual(o4.members, [Element('5b^-1')])

    def test_format_parens(self):
        self.assertEqual(format_parens('3(a + b)'), '3*(a + b)')
        self.assertEqual(format_parens('a^2(bc)(4 + a)'), 'a^2*(bc)*(4 + a)')

    def test_parse_expression(self):
        self.assertEqual(parse_expression(' 3   *(1  + b)'), ['3', '*', '(', '1', '+', 'b', ')'])
        self.assertEqual(parse_expression('123 + 4 5 * a / b'), ['123', '+', '45', '*', 'a', '/', 'b'])
        self.assertEqual(parse_expression('-12a+-1'), ['-12', '*', 'a', '+', '-1'])

    def test_to_rpn(self):
        self.assertEqual(to_rpn(['(', '12', '-', 'a', ')', '/', '3']), [Element('12'), Element('a'), '-',
                                                                        Element('3'), '/'])
        self.assertEqual(to_rpn(['5', '+', '2', '^', '3']), [Element('5'), Element('2'), Element('3'), '^', '+'])

    def test_all_together_now(self):
        self.assertEqual(all_together_now("a - b * (2 + 1)").print(), 'a - 3b')
        self.assertEqual(all_together_now('ab * b^(3 - 1)').print(), 'ab^3')
        self.assertEqual(all_together_now('-8c^5 * 5c^6 * 2c^3').print(), '-80c^14')
        self.assertEqual(all_together_now('z * 10z * z * z').print(), '10z^4')
        self.assertEqual(all_together_now('-3a^3 * (-4a^5) * (-9a^3)').print(), '-108a^11')
        self.assertEqual(all_together_now('3  +  7(3t  +  10)').print(), '73 + 21t')
        self.assertEqual(all_together_now('-6(-3n - 1)  +  8(-6  +  9n)').print(), '90n - 42')

        """ self.assertEqual(all_together_now('(-2v^3) / (-10xv^2)'), 'v / (5x)')
            this actually returns : 0.2vx^(-1)
            Both are correct, but the first one is cleaner and more readable
        """
        # TODO: Simplify division into most reducible fraction. See comment above
