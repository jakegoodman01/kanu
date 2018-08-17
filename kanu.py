import kanu


while True:
    print('Select one:')
    print('\t1) Solve a linear equation')
    print('\t2) Simplify any expression')

    choice = input()
    if choice == '1':
        print('Enter the equation:', end=' ')
        print(kanu.solve_single_linear_equation(input()))
    elif choice == '2':
        print('Enter the expression:', end=' ')
        print(kanu.all_together_now(input()))
    print()