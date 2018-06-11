import operator

symbols = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}


class Element:
    def __init__(self, value: str):
        elem = Element.separate_coefficient(value)
        self.coefficient = float(elem[0])
        self.variable = Variable(elem[1])

    def __repr__(self):
        if self.variable is None:
            return f'{self.coefficient}'
        if self.coefficient == 0:
            return f'0'
        if self.coefficient == 1:
            return f'{self.variable}'
        if self.coefficient % 1 == 0.0:
            return f'{int(self.coefficient)}{self.variable}'
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
            var = Variable(a.variable.name)

            if op == '*':
                var.mul(b.variable)
            else:
                var.div(b.variable)

            coefficient = symbols.get(op)(a.coefficient, b.coefficient)
            return Element(f'{coefficient}{var.name}')

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

    def add(self, elem):
        if self.variable == elem.variable:
            self.coefficient += elem.coefficient
        else:
            raise ValueError('Cannot add or subtract elements of different terms')


class Variable:
    def __init__(self, name: str):
        self.name = ""
        self.components = None
        self._parse_variable(name)
        self.write_name()

    def __repr__(self):
        if self.name is None:
            return ''
        return self.name

    def __eq__(self, other):
        if self.components is None and other.components is None:
            return True

        try:
            return sorted(self.components) == sorted(other.components)
        except TypeError:
            return False

    def write_name(self):
        if self.components is not None:
            self.name = ""
            self.components.sort()
            freq = {}
            for e in self.components:
                if freq.get(e) is None:
                    freq[e] = 1
                else:
                    freq[e] += 1
            for e in freq:
                if freq[e] == 1:
                    self.name += e
                else:
                    self.name += f'{e}^{freq[e]}'

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

    def mul(self, other):
        self.components.extend(other.components)
        self.write_name()

    def div(self, other):
        pass


class Expression:
    def __init__(self, exp: str):
        self.given_exp = exp
        self.elements = []
        self._parse_expression(exp)

    def __repr__(self):
        out = ''
        for i in range(len(self.elements)):
            if i == 0:
                out += f'{self.elements[i]}'
            elif isinstance(self.elements[i], str):
                out += f' {self.elements[i]}'
            else:
                if isinstance(self.elements[i - 1], str):
                    out += f' {self.elements[i]}'
                else:
                    e = f'{self.elements[i]}'
                    if e[0] == '-':
                        out += f' - {e[1:]}'
                    else:
                        out += f' + {e}'
        return out

    def _parse_expression(self, exp: str):
        exp = ''.join(exp.split())  # remove spaces from exp
        exp += '-1'  # not part of the expression, just so the loop can execute twice more
        begin = 0
        for i in range(1, len(exp)):

            if exp[begin] == '*' or exp[begin] == '/':
                self.elements.append(exp[begin])
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

    def simplify(self):
        i = 0
        while i < len(self.elements):
            if isinstance(self.elements[i], str):
                try:
                    new_elem = Element.apply_operator(
                        self.elements[i - 1],
                        self.elements[i + 1],
                        self.elements[i]
                    )
                    self.elements.insert(i + 2, new_elem)
                    self.elements = self.elements[:i - 1] + self.elements[i + 2:]

                except ValueError:
                    if self.elements[i] == '+':
                        del self.elements[i]
                    elif self.elements[i] == '-':
                        if self.elements[i + 1].coefficient < 0:
                            self.elements[i + 1].coefficient *= -1
                        del self.elements[i]

            else:
                i += 1

        # By this point, all items in self.elements should be Element objects
        i = 0
        while i < len(self.elements):
            j = i + 1
            while j < len(self.elements):
                try:
                    self.elements[i].add(self.elements[j])
                    del self.elements[j]
                except ValueError:
                    j += 1
            i += 1


"""
a = Element('4a^2')
b = Element('2aa')
print(Element.apply_operator(a, b, '/'))"""
ex = Expression('4a * +2a +4')
ex.simplify()
print(ex)
