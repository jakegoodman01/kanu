import kanu


while True:
    print('Select one:')
    print('\t1 -> Solve a linear equation')
    print('\t2 -> Simplify any expression')
    print('\t3 -> Exit program')

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
    elif choice == '3':
        print('Thank you for using kanu!\nPlease contact me at jake@jakelgoodman.com with any bugs or suggestions.')
        break
    else:
        print('You must select an option from the menu!')
    print()
