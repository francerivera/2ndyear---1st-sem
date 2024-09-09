def get_negative():
    while True:
        num1 = input("Please enter the first negative number: ")
        num2 = input("Please enter the second negative number: ")
        if num1.lstrip('-').isdigit() and num2.lstrip('-').isdigit():
            num1 = int(num1)
            num2 = int(num2)
            if num1 < 0 and num2 < 0:
                return num1, num2
            else:
                print("Invalid input. Please enter negative integers.")
        else:
            print("Invalid input. Please enter integers.")

while True:
    num1, num2 = get_negative()
    print("Select an operation:\n(1) Addition\n(2) Subtraction\n(3) Multiplication\n(4) Division\n(5) Modulus Division\n(6) Exponent\n(7) Floor Division\n(x) EXIT")
    choice = input("Enter your choice: ")

    if choice == '1':
        result = num1 + num2
    elif choice == '2':
        result = num1 - num2
    elif choice == '3':
        result = num1 * num2
    elif choice == '4':
        if num2 == 0:
            print("Cannot divide by zero.")
            continue
        result = num1 / num2
    elif choice == '5':
        result = num1 % num2
    elif choice == '6':
        result = num1 ** num2
    elif choice == '7':
        result = num1 // num2
    elif choice.lower() == 'x':
        break
    else:
        print("Invalid choice. Please try again.")
        continue

    print(f"The result is: {result}")

    continue_choice = input("Press 'y' to continue or 'x' to exit: ")
    if continue_choice == 'y':
        continue
    elif continue_choice == 'x':
        break
