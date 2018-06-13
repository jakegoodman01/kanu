import unittest
from expression import Element, Expression, Variable


class ElementTests(unittest.TestCase):
    def test_positive(self):
        e1 = Element('010a')
        e2 = Element('+100b')
        e3 = Element('1c')
        e4 = Element('x')

        self.assertGreater(e1.coefficient, 0)
        self.assertGreater(e2.coefficient, 0)
        self.assertGreater(e3.coefficient, 0)
        self.assertGreater(e4.coefficient, 0)

    def test_negative(self):
        e1 = Element('-010a')
        e2 = Element('-100b')
        e3 = Element('-1c')
        e4 = Element('-x')

        self.assertLess(e1.coefficient, 0)
        self.assertLess(e2.coefficient, 0)
        self.assertLess(e3.coefficient, 0)
        self.assertLess(e4.coefficient, 0)

    def test_zero(self):
        e1 = Element('0')
        e2 = Element('0a')
        e3 = Element('00a')
        e4 = Element('-0a')
        e5 = Element('-0')

        self.assertEqual(e1.coefficient, 0)
        self.assertEqual(e2.coefficient, 0)
        self.assertEqual(e3.coefficient, 0)
        self.assertEqual(e4.coefficient, 0)
        self.assertEqual(e5.coefficient, 0)

    def test_repr(self):
        e1 = Element('4a^0b^0')
        e2 = Element('0')
        e3 = Element('0ab')
        e4 = Element('1a')
        e5 = Element('-1a')
        e6 = Element('a')
        e7 = Element('-a')
        e8 = Element('4ab')
        e9 = Element('1.85c')

        self.assertEqual(e1.__repr__(), '4')
        self.assertEqual(e2.__repr__(), '0')
        self.assertEqual(e3.__repr__(), '0')
        self.assertEqual(e4.__repr__(), 'a')
        self.assertEqual(e5.__repr__(), '-a')
        self.assertEqual(e6.__repr__(), 'a')
        self.assertEqual(e7.__repr__(), '-a')
        self.assertEqual(e8.__repr__(), '4ab')
        self.assertEqual(e9.__repr__(), '1.85c')

    def test_apply_operator(self):
        e2 = Element('0')
        e3 = Element('-2ab')
        e4 = Element('1a')
        e5 = Element('-1a')
        e6 = Element('a')
        e7 = Element('-a')
        e8 = Element('4ab')
        e9 = Element('10ab')

        self.assertRaises(ValueError, lambda: Element.apply_operator(e4, e4, 'i'))
        self.assertRaises(ValueError, lambda: Element.apply_operator(e4, e8, '+'))
        self.assertEqual(Element.apply_operator(e3, e8, '+'), Element('2ab'))
        self.assertEqual(Element.apply_operator(e8, e9, '-'), Element('-6ab'))
        self.assertEqual(Element.apply_operator(e2, e9, '*'), Element('0'))
        self.assertEqual(Element.apply_operator(e5, e7, '*'), Element('a^2'))
        self.assertEqual(Element.apply_operator(e8, e3, '*'), Element('-8a^2b^2'))
        self.assertEqual(Element.apply_operator(e3, e6, '/'), Element('-2b'))
        self.assertEqual(Element.apply_operator(e4, e3, '/'), Element('-0.5b^-1'))

    def test_separate_coefficient(self):
        self.assertEqual(Element.separate_coefficient('0'), ('0', None))
        self.assertEqual(Element.separate_coefficient('1'), ('1', None))
        self.assertEqual(Element.separate_coefficient('1a'), ('1', 'a'))
        self.assertEqual(Element.separate_coefficient('a'), ('1', 'a'))
        self.assertEqual(Element.separate_coefficient('-a'), ('-1', 'a'))
        self.assertEqual(Element.separate_coefficient('-1a'), ('-1', 'a'))
        self.assertEqual(Element.separate_coefficient('-100a'), ('-100', 'a'))

    def test_add(self):
        e1 = Element('5a')
        e2 = Element('a')
        e3 = Element('b')

        e1.add(e2)
        self.assertEqual(e1, Element('6a'))
        self.assertRaises(ValueError, lambda: e1.add(e3))


if __name__ == '__main__':
    unittest.main()
