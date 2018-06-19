import unittest
from element import *


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
        self.assertEqual(Element.separate_coefficient('-1a'), ('-1', 'a'))
        self.assertEqual(Element.separate_coefficient('+2a'), ('2', 'a'))
        self.assertEqual(Element.separate_coefficient('0'), ('0', None))

    def test_repr(self):
        e1 = Element('+123')
        e2 = Element('0ab^4')
        e3 = Element('a^0')

        self.assertEqual(repr(e1), '123')
        self.assertEqual(repr(e2), '0')
        self.assertEqual(repr(e3), '1')


class VariableTests(unittest.TestCase):
    def test_parse_variable(self):
        v1 = Variable('a^-bc')
        v2 = Variable('a^(bc)')
        v3 = Variable('ab^(3ac)')

        self.assertEqual(v1.components, {'a': Element('-b'), 'c': Element('1')})
        self.assertEqual(v2.components, {'a': Element('bc')})
        self.assertEqual(v3.components, {'a': Element('1'), 'b': Element('3ac')})


if __name__ == '__main__':
    unittest.main()