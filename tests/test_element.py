import unittest
from kanu.expression import *


class ElementTests(unittest.TestCase):
    def test_get_matching_paren(self):
        self.assertRaises(ValueError, lambda: get_matching_paren('3(1 + 2)'))
        self.assertRaises(IndexError, lambda: get_matching_paren('(1 % 2'))
        self.assertEqual(get_matching_paren('(1 + 2) / 8'), 6)
        self.assertEqual(get_matching_paren('(1 + (3) + (4 / (5))) + 90 / 10'), 20)

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