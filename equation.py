from expression import *


def find_variables(exp: OperatorList) -> set:
    variables = set()
    for elem in exp.members:
        variables = variables.union(elem.variable.components.keys())
    return variables


def solve(equation: str) -> str:
    equal_sign = equation.index('=')
    ls = all_together_now(equation[:equal_sign])
    rs = all_together_now(equation[equal_sign + 1:])

    ls_vars = find_variables(ls)
    rs_vars = find_variables(rs)

    if len(ls_vars.union(rs_vars)) > 1:
        raise ValueError('Cannot solve single equation with multiple variables')
    elif len(ls_vars.union(rs_vars)) == 0:
        return 'There are no variables to solve for!'

    # Here, it is confirmed that there is only one variable in the equation

    """return f'ls = {ls}\nrs = {rs}\n\n' \
           f'ls variables: {find_variables(ls)}\n' \
           f'rs variables: {find_variables(rs)}\n\n'"""
    return ''


while True:
    print(solve(input()))