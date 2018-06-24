from element import *

operations = {'+': Element.add, '-': Element.sub, '*': Element.mul, '/': Element.div}
operator_precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '^': 4}


class OperatorList:
    def __init__(self, *elements, operation='+'):
        """ Elements is composed of Elements and OperatorLists
            op is an operation character: +, -, *, /
        """
        self.members = []
        for e in elements:
            if isinstance(e, Element):
                self.members.append(e)
            elif isinstance(e, OperatorList):
                if len(e.members) > 1 and operation in ('*', '/'):
                    self.members.append(e)
                else:
                    self.members.extend(e.members)
            else:
                raise ValueError('Invalid argument for an OperatorList')

        self.operation = operation

        self.simplify()

    def __repr__(self):
        return f'{self.operation}{self.members}'

    def simplify(self):
        i = 0
        while i < len(self.members) - 1:
            j = i + 1
            restart = False
            while j < len(self.members):
                try:
                    e = operations[self.operation](
                        self.members[i],
                        self.members[j]
                    )
                    self.members.pop(j)
                    self.members.pop(i)
                    self.members.insert(i, e)
                    restart = True
                except ValueError:
                    j += 1
                except AttributeError:
                    j += 1
            if restart:
                i = 0
            else:
                i += 1


def format_parens(exp: str) -> str:
    exp_list = list(exp)
    i = 0
    while i < len(exp_list):
        if i > 0 and exp_list[i] == '(' and (exp_list[i - 1].isdigit() or exp_list[i - 1] == ')'):
            exp_list.insert(i, '*')
            i += 1
        i += 1
    return ''.join(exp_list)


def parse_expression(exp: str) -> list:
    # the '-' character is not part of the expression, it's function is so that the while loop executes once more
    exp = ''.join(exp.split()) + '-'
    elements = []
    i = 0
    begin = -1
    while i < len(exp):
        if exp[i].isdigit():
            if begin == -1:
                begin = i
        elif begin == -1:
            elements.append(exp[i])
        else:
            elements.append(exp[begin:i])
            elements.append(exp[i])
            begin = -1
        i += 1
    return elements[:-1]


def to_rpn(elements: list) -> list:
    """Conversion to reverse polish notation, implementing the Shunting-yard algorithm"""
    i = 0
    output_queue = []
    op_stack = []
    while i < len(elements):
        token = elements[i]
        if token.isdigit() or token.isalpha():
            output_queue.append(token)
        elif token in ('+', '-', '*', '/', '^'):
            while len(op_stack) > 0 and \
                    op_stack[-1] != '(' \
                    and operator_precedence[op_stack[-1]] >= operator_precedence[token]:
                output_queue.append(op_stack.pop())
            op_stack.append(token)
        elif token == '(':
            op_stack.append(token)
        elif token == ')':
            while op_stack[-1] != '(':
                output_queue.append(op_stack.pop())
            op_stack.pop()
        i += 1

    while len(op_stack) > 0:
        output_queue.append(op_stack.pop())
    return output_queue


if __name__ == '__main__':
    ex = 'a + 2 * (b + 12)'
    ex = format_parens(ex)
    ex = parse_expression(ex)
    ex = to_rpn(ex)
    print(ex)
