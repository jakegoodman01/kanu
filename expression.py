from element import *

operations = {'+': Element.add, '-': Element.sub, '*': Element.mul, '/': Element.div}


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


class ExpressionParser:
    def __init__(self, exp: str):
        self.exp = ExpressionParser._format_parens(exp)
        self.elements = ExpressionParser._parse_expression(self.exp)

    @classmethod
    def _format_parens(cls, exp: str) -> str:
        exp_list = list(exp)
        i = 0
        while i < len(exp_list):
            if exp_list[i] == '(':
                exp_list.insert(i, '*')
                i += 1
            i += 1
        return ''.join(exp_list)

    @classmethod
    def _parse_expression(cls, exp: str) -> OperatorList:
        exp = ''.join(exp.split())  # remove spaces from exp
        for i in range(len(exp)):
            if exp[i] in ('+', '-', '*', '/', '^'):
                return OperatorList(
                    OperatorList(ExpressionParser._parse_expression(exp[:i])),
                    OperatorList(ExpressionParser._parse_expression(exp[i + 1:])),
                    operation=exp[i]
                )

        # there are no operators once program flow reaches this point
        return Element(exp)


if __name__ == '__main__':
    ex = ExpressionParser('a + 2 * b + 1')
    print(ex.elements)
