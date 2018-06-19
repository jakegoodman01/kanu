from element import *

operations = {'+': Element.add, '-': Element.sub, '*': Element.mul, '/': Element.div}


class OperatorList:
    def __init__(self, operation, *elements):
        """ Elements is composed of Elements and OperatorLists
            op is an operation character: +, -, *, /
        """
        self.members = list(elements)
        self.operation = operation

        self.simplify()

    def __repr__(self):
        return f'{self.operation}{self.members}'

    def simplify(self):
        i = 0
        restart = False
        while i < len(self.members) - 1:
            j = i + 1
            operation_done = False
            while j < len(self.members):
                try:
                    e = operations[self.operation](
                        self.members[i],
                        self.members[j]
                    )
                    operation_done = True
                    self.members.pop(j)
                    self.members.pop(i)
                    self.members.insert(i, e)
                    restart = True
                except ValueError:
                    j += 1
            if not operation_done:
                break
            if restart:
                i = 0
            else:
                i += 1


e1 = Element('5a')
e2 = Element('6a')
e3 = Element('1')
print(OperatorList('+', e1, e2, e3))