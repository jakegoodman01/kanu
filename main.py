import operator

symbols = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}


class Element:
    def __init__(self, value: str):
        elem = Element.separate_coefficient(value)
        self.coefficient = int(elem[0])
        self.variable = Variable(elem[1])

    def __repr__(self):
        if self.variable is None:
            return f'{self.coefficient}'
        if self.coefficient == 0:
            return f'0'
        if self.coefficient == 1:
            return f'{self.variable}'
        return f'{self.coefficient}{self.variable}'

    @classmethod
    def apply_operator(cls, a, b, op: str):
        if op not in symbols.keys():
            raise ValueError('Invalid operator symbol')

        if op == '+' or op == '-':
            if a.variable == b.variable:
                coefficient = symbols.get(op)(a.coefficient, b.coefficient)
                return Element(f'{coefficient}{a.variable}')
            else:
                raise ValueError('Cannot add or subtract elements of different terms')
        else:
            # TODO: Implement applying * and / operators onto Elements
            pass

    def add(self, elem):
        if self.variable == elem.variable:
            self.coefficient += elem.coefficient
        else:
            raise ValueError('Cannot add or subtract elements of different terms')

    @classmethod
    def separate_coefficient(cls, e) -> tuple:
        for i in range(len(e)):
            if e[i].isalpha():
                if i == 0:
                    return '1', e
                if i == 1 and not e[0].isdigit():
                    return f'{e[0]}1', e[i:]
                return e[:i], e[i:]

        # If the for loop completes, there was no variable in e
        return e, None


class Variable:
    def __init__(self, name: str):
        self.name = name
        self.components = None
        self._parse_variable(name)

    def __repr__(self):
        if self.name is None:
            return ''
        return self.name

    def _parse_variable(self, name: str):
        if name is not None:
            name += 'z'  # not part of the variable name, just so the loop can execute once more
            self.components = []  # Contains the number of variables in the name. For example: a^2b -> [a, a, b]
            curr_var = name[0]
            check_exponent = False
            power = None
            if len(name) == 1:
                self.components.append(curr_var)
            else:
                for i in range(1, len(name)):
                    if check_exponent:
                        power = int(name[i])
                        check_exponent = False
                    elif name[i] == '^':
                        check_exponent = True
                    else:
                        #  this code is run when a new letter has been read
                        if power is None:
                            self.components.append(curr_var)
                        else:
                            self.components.extend([curr_var for j in range(power)])
                            power = None
                        curr_var = name[i]


class Expression:
    def __init__(self, exp: str):
        """Elements in the expression are space separated."""
        self._parse_expression(exp)

    def _parse_expression(self, exp: str):
        self.elements = []

        exp = ''.join(exp.split())  # remove spaces from exp
        exp += '-1'  # not part of the expression, just so the loop can execute twice more
        begin = 0
        for i in range(1, len(exp)):

            if exp[begin] == '*' or exp[begin] == '/':
                self.elements.append(symbols.get(exp[begin]))
                begin = i
            else:
                if exp[i] in symbols:
                    if i - begin == 1:
                        if exp[begin].isdigit():
                            self.elements.append(Element(exp[begin]))
                        else:
                            self.elements.append(exp[begin])
                    else:
                        self.elements.append(Element(exp[begin:i]))
                    begin = i


# ex = Expression('-2 + 10a^2 * 6a + 2 / 9')
# print(ex.elements)
# for e in ex.elements:
#     print(f'{e} -> {type(e)}')
first = Element('ab^2')
print(first.variable.components)
