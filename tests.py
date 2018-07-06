import unittest
from expression import *


class ModuleTests(unittest.TestCase):
    def test_get_matching_paren(self):
        self.assertRaises(ValueError, lambda: get_matching_paren('3(1 + 2)'))
        self.assertRaises(IndexError, lambda: get_matching_paren('(1 % 2'))
        self.assertEqual(get_matching_paren('(1 + 2) / 8'), 6)
        self.assertEqual(get_matching_paren('(1 + (3) + (4 / (5))) + 90 / 10'), 20)


class ElementTests(unittest.TestCase):
    def test_separate_coefficient(self):
        self.assertEqual(Element.separate_coefficient('+a'), ('1', 'a'))
        self.assertEqual(Element.separate_coefficient('1'), ('1', None))
        self.assertEqual(Element.separate_coefficient('-1'), ('-1', None))
        self.assertEqual(Element.separate_coefficient('-a'), ('-1', 'a'))
        self.assertEqual(Element.separate_coefficient('-1a^e'), ('-1', 'a^e'))
        self.assertEqual(Element.separate_coefficient('+2a'), ('2', 'a'))
        self.assertEqual(Element.separate_coefficient('0'), ('0', None))
        self.assertEqual(Element.separate_coefficient('a^b'), ('1', 'a^b'))
        self.assertEqual(Element.separate_coefficient('4^2'), ('1', '4^2'))
        self.assertEqual(Element.separate_coefficient('4^a'), ('1', '4^a'))
        self.assertEqual(Element.separate_coefficient('1000a^4'), ('1000', 'a^4'))
        self.assertEqual(Element.separate_coefficient('-1^a^2'), ('1', '-1^a^2'))

    def test_eq(self):
        self.assertEqual(Element('a^2b') == Element('ba^2'), True)
        self.assertEqual(Element('a^0') == Element('1'), True)
        self.assertEqual(Element('a^2b') == Element('ab^2'), False)

    def test_repr(self):
        e1 = Element('+123')
        e2 = Element('0ab^4')
        e3 = Element('-a^0')

        self.assertEqual(repr(e1), '123')
        self.assertEqual(repr(e2), '0')
        self.assertEqual(repr(e3), '-1')


class VariableTests(unittest.TestCase):
    def test_parse_variable(self):
        v1 = Variable('a^-bc')
        v2 = Variable('a^(bc)')
        v3 = Variable('ab^(3a^(4a^e)c)')
        v4 = Variable('a^2')
        v5 = Variable('b^3^v')
        v6 = Variable('a^b^2')

        self.assertEqual(v1.components, {'a': Element('-b'), 'c': Element('1')})
        self.assertEqual(v2.components, {'a': Element('bc')})
        self.assertEqual(v3.components, {'a': Element('1'), 'b': Element('3a^(4a^e)c')})
        self.assertEqual(v4.components, {'a': Element('2')})
        self.assertEqual(v5.components, {'b': Element('3^v')})
        self.assertEqual(v6.components, {'a': Element('b^2')})

    def test_repr(self):
        v1 = Variable('a')
        v2 = Variable('a^2')
        v3 = Variable('ab^9^2')
        v4 = Variable('a^a^b^3^4^v')
        v5 = Variable('b^0')

        self.assertEqual(repr(v1), 'a')
        self.assertEqual(repr(v2), 'a^2')
        self.assertEqual(repr(v3), 'ab^81')
        self.assertEqual(repr(v4), 'a^(a^(b^(3^(4^v))))')
        self.assertEqual(repr(v5), '')


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


if __name__ == '__main__':
    unittest.main()