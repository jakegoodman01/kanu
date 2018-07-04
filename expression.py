from element import *

operations = {'+': Element.add, '-': Element.sub, '*': Element.mul, '/': Element.div, '^': Element.pow}
operator_precedence = {'+': 2, '-': 2, '*': 3, '/': 3, '^': 4}

# TODO: Implement the distributive property


class OperatorList:
    def __init__(self, *elements, operation='+'):
        """ Elements is composed of Elements and OperatorLists
            op is an operation character: +, *, /
            There are no subtraction lists because they will just be addition lists with negative numbers
        """
        self.members = []
        is_first_element = True
        for e in elements:
            if isinstance(e, Element):
                if not is_first_element and operation == '-':
                    self.members.append(Element.mul(e, Element('-1')))
                else:
                    self.members.append(e)
            elif isinstance(e, OperatorList):
                if operation in ('*', '/'):
                    self.members.append(e)
                elif not is_first_element and operation in ('+', '-') and e.operation in ('+', '-'):
                    for i in range(1, len(e.members)):
                        e.members[i] = Element.mul(e.members[i], Element('-1'))
                    self.members.extend(e.members)
                else:
                    self.members.extend(e.members)
            else:
                raise ValueError('Invalid argument for an OperatorList')
            is_first_element = False

        if operation == '-':
            self.operation = '+'
        else:
            self.operation = operation

        self.simplify()

    def __repr__(self):
        return f'{self.operation}{self.members}'

    def __eq__(self, other):
        return self.operation == other.operation and self.members == other.members

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

        while True:
            try:
                self.members.remove(Element('0'))
            except AttributeError:
                break
            except ValueError:
                break

        if self.operation == '*' and len(self.members) == 2:
            """if the preceding condition is true, this OperatorList must be simplified using the distributive
                property
            """
            new_members = []

            # first and second are OperatorLists and are cast to OperatorLists if they are not already
            first = self.members[0] if isinstance(self.members[0], OperatorList) else OperatorList(self.members[0])
            second = self.members[1] if isinstance(self.members[1], OperatorList) else OperatorList(self.members[1])

            for i in first.members:
                for j in second.members:
                    new_members.append(Element.mul(i, j))
            self.members = new_members
            self.operation = '+'


def format_parens(exp: str) -> str:
    exp_list = list(exp)
    i = 0
    while i < len(exp_list):
        if i > 0 and exp_list[i] == '(' and \
                (exp_list[i - 1].isdigit() or exp_list[i - 1] == ')' or exp_list[i - 1].isalpha()):
            exp_list.insert(i, '*')
            i += 1
        elif i < len(exp_list) - 1 and exp_list[i] == ')' and \
                (exp_list[i + 1].isdigit() or exp_list[i + 1].isalpha()):
            exp_list.insert(i + 1, '*')
            i += 1

        i += 1
    return ''.join(exp_list)


def parse_expression(exp: str) -> list:
    # the '-' character is not part of the expression, it's function is so that the while loop executes once more
    exp = ''.join(exp.split()) + '-'
    elements = []
    begin = 0
    if exp[0] == '(':
        elements.append('(')
        begin += 1

    i = 1
    while i < len(exp):
        if exp[i] in operations or exp[i] in ('(', ')') or exp[i].isalpha():
            if exp[i] in ('+', '-') and (exp[i - 1] in operations or exp[i - 1] == '('):
                # if the above is true, then the sign is a negative sign, rather than a minus sign
                pass
            else:
                if begin != i:
                    elements.append(exp[begin:i])
                if exp[i].isalpha() and (exp[i - 1].isdigit() or exp[i - 1].isalpha()):
                    elements.append('*')
                elements.append(exp[i])
                begin = i + 1
        i += 1
    return elements[:-1]


def to_rpn(elements: list) -> list:
    """Conversion to reverse polish notation, implementing the Shunting-yard algorithm"""
    i = 0
    output_queue = []
    op_stack = []
    while i < len(elements):
        token = elements[i]
        try:
            # If token is not a valid element string, it will raise an exception
            output_queue.append(Element(token))
        except ValueError:
            if token in ('+', '-', '*', '/', '^'):
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


def to_op_list(elements: list) -> OperatorList:
    """elements should be a properly written reverse polish notation expression to be made into OperatorLists"""
    new_elements = []
    for e in elements:
        if isinstance(e, Element):
            new_elements.append(e)
        elif e in operations:
            operand_2 = new_elements.pop()
            operand_1 = new_elements.pop()
            result = OperatorList(operand_1, operand_2, operation=e)
            if len(result.members) == 1:
                result = Element(repr(result.members[0]))
            new_elements.append(result)
    if len(new_elements) > 1:
        raise ValueError("was not able to process expression")

    if type(new_elements[0]) == OperatorList:
        return new_elements[0]
    return OperatorList(*new_elements, operation='+')


def all_together_now(expression: str) -> OperatorList:
    """Calls all needed methods to have a readable expression"""
    ex = format_parens(expression)
    ex = parse_expression(ex)
    ex = to_rpn(ex)
    return to_op_list(ex)


if __name__ == '__main__':
    while True:
        print(all_together_now(input()))
