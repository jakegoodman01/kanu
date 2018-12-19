from kanu.expression import *


def find_variables(exp: OperatorList) -> set:
    variables = set()
    for elem in exp.members:
        variables = variables.union(elem.variable.components.keys())
    return variables


def solve_single_linear_equation(equation: str) -> str:
    equal_sign = equation.index('=')

    try:
        ls = all_together_now(equation[:equal_sign])
        rs = all_together_now(equation[equal_sign + 1:])
    except (MismatchedParenthesisError, InvalidElementError, InvalidExpressionError):
        return 'This equation is syntactically invalid!'

    ls_vars = find_variables(ls)
    rs_vars = find_variables(rs)

    if len(ls_vars.union(rs_vars)) > 1:
        raise ValueError('Cannot solve single equation with multiple variables')
    elif len(ls_vars.union(rs_vars)) == 0:
        return 'There are no variables to solve for!'

    # Here, it is confirmed that there is only one variable in the equation
    # The variable is isolated on the left side:

    while len(find_variables(rs)) > 0:
        for element in rs.members:
            if element.variable.components != {}:
                # subtracting the element with a variable from both sides
                rs = OperatorList(*rs.members, Element.mul(element, Element('-1')))
                ls = OperatorList(*ls.members, Element.mul(element, Element('-1')))
                break

    while len(find_variables(ls)) < len(ls.members):
        # if the above condition is true, there are element in ls which do not have variables
        for element in ls.members:
            if element.variable.components == {}:
                # subtracting the element with a variable from both sides
                rs = OperatorList(*rs.members, Element.mul(element, Element('-1')))
                ls = OperatorList(*ls.members, Element.mul(element, Element('-1')))
                break

    if len(ls.members) == 1 and len(rs.members) == 1:
        divisor = Element(f'{ls.members[0].coefficient}')
        ls = OperatorList(ls.members[0], divisor, operation='/')
        rs = OperatorList(rs.members[0], divisor, operation='/')

    return f'{ls.print()} = {rs.print()}'
