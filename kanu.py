import kanu


while True:
    print('Select one:')
    print('\t1) Solve a linear equation')
    print('\t2) Simplify any expression')

    choice = input()
    if choice == '1':
        print('Enter the equation:', end=' ')

        try:
            print(kanu.solve_single_linear_equation(input()))
        except kanu.NonLinearEquationError:
            print('You entered a non-linear equation. The current version of Kanu can only solve linear equations!')
    elif choice == '2':
        print('Enter the expression:', end=' ')
        print(kanu.all_together_now(input()))
    print()