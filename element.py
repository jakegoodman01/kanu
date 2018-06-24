def get_matching_paren(exp: str) -> int:
    """ Returns the index of the right parenthesis which matches the first left parenthesis.
        exp[0] should be a left parenthesis
    """
    if exp[0] != '(':
        raise ValueError('Given string must begin with \'(\' character')
    left = 1
    right = 0
    i = 1
    while left > right:
        if exp[i] == '(':
            left += 1
        elif exp[i] == ')':
            right += 1
        i += 1
    return i - 1


class NotValidVariable(Exception):
    """ This exception is raised when the variable of an expression is a valid number, and the coefficient is 1.
        For example, Element e has coefficient of 1, and variable of 27. They should be flipped because 27 is a valid
        number."""
    def __init__(self, coefficient: float):
        self.coefficient = coefficient


class Element:
    def __init__(self, rep: str):
        elem = Element.separate_coefficient(rep)
        self.coefficient = float(elem[0])
        if self.coefficient != 0.0:
            try:
                self.variable = Variable(elem[1])
            except NotValidVariable as nvv:
                self.coefficient = nvv.coefficient
                self.variable = Variable(None)
        else:
            self.variable = Variable(None)

    def __repr__(self):
        if self.variable is None:
            return f'{self.coefficient}'
        if self.coefficient == 0:
            return '0'
        if self.coefficient == 1.0:
            if self.variable.components == {}:
                return '1'
            return f'{self.variable}'
        if self.coefficient % 1 == 0.0:
            return f'{int(self.coefficient)}{self.variable}'
        return f'{self.coefficient}{self.variable}'

    def __eq__(self, other):
        return self.variable == other.variable and self.coefficient == other.coefficient

    @classmethod
    def separate_coefficient(cls, e: str) -> tuple:
        if e[0] == '+':
            e = e[1:]

        if '^' in e and (e[:e.index('^')].isdigit() or e[1:e.index('^')].isdigit() and e[0] == '-'):
            """ This check is for when e represents a real number raised to a power, not a variable.
                i.e. -2^4
            """
            return '1', e

        for i in range(len(e)):
            if e[i].isalpha():
                if i == 0:
                    return '1', e
                elif i == 1 and not e[0].isdigit():
                    return f'{e[:1]}1', e[1:]
                return e[:i], e[i:]
        # If the for loop completes, there was no variable in e
        return e, None

    @classmethod
    def add(cls, e1, e2):
        if e1.variable == e2.variable:
            return Element(f'{e1.coefficient + e2.coefficient}{e1.variable}')
        else:
            raise ValueError('Cannot add or subtract elements of different terms')

    @classmethod
    def sub(cls, e1, e2):
        if e1.variable == e2.variable:
            return Element(f'{e1.coefficient - e2.coefficient}{e1.variable}')
        else:
            raise ValueError('Cannot add or subtract elements of different terms')

    @classmethod
    def mul(cls, e1, e2):
        coefficient = e1.coefficient * e2.coefficient
        var = Variable.mul(e1.variable, e2.variable)
        return Element(f'{coefficient}{var}')

    @classmethod
    def div(cls, e1, e2):
        coefficient = e1.coefficient / e2.coefficient
        var = Variable.div(e1.variable, e2.variable)
        return Element(f'{coefficient}{var}')

    @classmethod
    def pow(cls, e1, e2):
        if not repr(e2).isdigit():
            return Element(f'{e1}^({e2})')
        elem = Element('1')
        for i in range(int(repr(e2)) ):
            elem = Element.mul(elem, e1)
        return elem


class Variable:
    def __init__(self, rep: str):
        self.name = ''
        self.components = {}  # dictionary, mapping a letter variable to it's frequency, represented as an Element
        self._parse_variable(rep)
        self.write_name()

    def __repr__(self):
        if self.name == '':
            return ''
        return self.name

    def __eq__(self, other):
        return self.components == other.components

    @classmethod
    def mul(cls, v1, v2):
        for e in v2.components:
            if v1.components.get(e) is None:
                v1.components[e] = v2.components[e]
            else:
                v1.components[e] = Element.add(v1.components[e], v2.components[e])
        v1.write_name()
        return v1

    @classmethod
    def div(cls, v1, v2):
        for e in v2.components:
            if v1.components.get(e) is None:
                v1.components[e] = Element.mul(v2.components[e], Element('-1'))
            else:
                v1.components[e] = Element.sub(v1.components[e], v2.components[e])
        v1.write_name()
        return v1

    def write_name(self):
        self._remove_redundant_variables()
        self.name = ''
        if self.components != {}:
            keys = sorted(list(self.components.keys()))
            for key in keys:
                if self.components[key] == Element('1'):
                    self.name += f'{key}'
                elif not repr(self.components[key]).isdigit() and len(repr(self.components[key])) > 1:
                    self.name += f'{key}^({self.components[key]})'
                else:
                    self.name += f'{key}^{self.components[key]}'

            first_key = list(self.components.keys())[0]
            if len(self.components) == 1 and first_key.isdigit() and self.components[first_key] == Element('1'):
                raise NotValidVariable(float(list(self.components.keys())[0]))

    def _parse_variable(self, name: str):
        if name is not None:
            name += 'z'  # not part of the variable name, just so the loop can execute once more
            curr_var = name[0]
            check_exponent = False
            power = Element('1')
            i = 1
            while i < len(name):
                if check_exponent:
                    if name[i] == '(':
                        right_paren = get_matching_paren(name[i:])
                        power = Element(f'{name[i + 1:i + right_paren]}')
                        i += right_paren
                        check_exponent = False
                    else:
                        # end is the index of the first letter character after name[i], that is not an exponent
                        end = None
                        for j in range(i + 1, len(name)):
                            if name[j].isalpha() and name[j - 1] != '^':
                                end = j
                                break

                        if end == i + 1 and name[i] == '-':
                            power = Element(name[i:end + 1])
                            i += 1
                        else:
                            power = Element(name[i:end])
                            i = end - 1
                        check_exponent = False
                elif name[i] == '^':
                    check_exponent = True
                else:
                    #  this code is run when a new letter has been read
                    if self.components.get(curr_var) is None:
                        self.components[curr_var] = power
                    else:
                        self.components[curr_var] += power
                    curr_var = name[i]
                    power = Element('1')
                i += 1

    def _remove_redundant_variables(self):
        """ Removes all keys with value of zero because it equals one, and that is redundant.
            Also calculates exponents of two integers.
        """
        keys_to_remove = []
        keys_to_add = []
        for c in self.components:
            if self.components[c] == Element('0'):
                keys_to_remove.append(c)
            if repr(self.components[c]).isdigit() and c.isdigit():
                keys_to_remove.append(c)
                keys_to_add.append(repr(Element.pow(Element(c), self.components[c])))
        for k in keys_to_remove:
            del self.components[k]
        for k in keys_to_add:
            self.components[k] = Element('1')


if __name__ == '__main__':
    e = Element('13')
    print(e.coefficient)
    print(e.variable)
