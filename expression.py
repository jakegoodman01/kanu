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


class Element:
    def __init__(self, rep: str):
        elem = Element.separate_coefficient(rep)
        self.coefficient = float(elem[0])
        self.variable = Variable(elem[1])

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
        for i in range(len(e)):
            if e[i].isalpha():
                if i == 0:
                    return '1', e
                elif i == 1 and not e[0].isdigit():
                    return f'{e[:1]}1', e[1:]
                return e[:i], e[i:]
        # If the for loop completes, there was no variable in e
        return e, None

    def add(self, elem):
        if self.variable == elem.variable:
            self.coefficient += elem.coefficient
        else:
            raise ValueError('Cannot add or subtract elements of different terms')


class Variable:
    def __init__(self, rep: str):
        self.name = ""
        self.components = {} # dictionary, mapping a letter variable to it's frequency, represented as an Element
        self._parse_variable(rep)
        self.write_name()

    def __repr__(self):
        if self.name == "":
            return ''
        return self.name

    def __eq__(self, other):
        return self.components == other.components

    def write_name(self):
        self._remove_redundant_variables()
        if self.components != {}:
            self.name = ''
            keys = sorted(list(self.components.keys()))
            for key in keys:
                if self.components[key] == Element('0'):
                    pass
                elif self.components[key] == Element('1'):
                    self.name += f'{key}'
                else:
                    self.name += f'{key}^{self.components[key]}'

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
                        # end is the index of the first letter character after name[i]
                        end = None
                        for j in range(i + 1, len(name)):
                            if name[j].isalpha():
                                end = j
                                break
                            elif j == len(name) - 1:
                                end = j + 1
                                break

                        if end == i + 1:
                            power = Element(name[i:end + 1])
                        else:
                            power = Element(name[i:end])
                        check_exponent = False
                        i = end
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
        for c in self.components:
            if self.components[c] == Element('0'):
                del self.components[c]

