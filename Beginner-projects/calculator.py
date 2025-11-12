def calculator(number1, number2, operation):
    """Perform basic arithmetic operations."""
    operations = {
        "+": number1 + number2,
        "-": number1 - number2,
        "*": number1 * number2,
        "/": number1 / number2 if number2 != 0 else None
    }
    
    if operation in operations:
        if operation == "/" and number2 == 0:
            return "Error: Division by zero!"
        return operations[operation]
    else:
        return "Error: Unknown operator"


def get_number(prompt):
    """Get a valid number from user input."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def get_operation():
    """Get a valid operation from user input."""
    valid_operations = ["+", "-", "*", "/"]
    print("Available operations: + - * /")
    
    while True:
        operation = input("Pick an operation: ").strip()
        if operation in valid_operations:
            return operation
        print("Please choose a valid operation: +, -, *, or /")


def get_user_choice(current_result):
    """Get user's choice for continuing calculations."""
    while True:
        choice = input(
            f"Type 'y' to continue with {current_result}, "
            f"'n' for new calculation, or 'q' to quit: "
        ).lower().strip()
        
        if choice in ['y', 'n', 'q']:
            return choice
        print("Invalid input. Please type 'y', 'n', or 'q'.")


def main():
    """Main calculator program."""
    print("Welcome to the Calculator!")
    
    while True:
        # Get initial calculation
        number1 = get_number("What's the first number? ")
        operation = get_operation()
        number2 = get_number("What's the next number? ")
        
        result = calculator(number1, number2, operation)
        
        if isinstance(result, str):  # Error occurred
            print(result)
            continue
            
        print(f"Result: {result}")
        
        # Continue with current result or start new calculation
        while True:
            choice = get_user_choice(result)
            
            if choice == 'y':
                operation = get_operation()
                number2 = get_number("What's the next number? ")
                result = calculator(result, number2, operation)
                
                if isinstance(result, str):  # Error occurred
                    print(result)
                    break
                    
                print(f"Result: {result}")
                
            elif choice == 'n':
                break
                
            elif choice == 'q':
                print("Thanks for using the calculator! Goodbye!")
                return


if __name__ == "__main__":
    main()
