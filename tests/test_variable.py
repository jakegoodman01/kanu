import unittest
from kanu.expression import *


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
