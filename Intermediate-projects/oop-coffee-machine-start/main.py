from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine


def main():
    """Main program loop for the coffee machine."""
    # Create instances of all the classes
    menu = Menu()
    coffee_maker = CoffeeMaker()
    money_machine = MoneyMachine()
    
    machine_on = True

    while machine_on:
        print("\n☕ Welcome to the Coffee Maker!")
        print("=" * 40)
        
        # Get user choice - use the menu object to display options
        choice = input(f"What would you like? ({menu.get_items()}report/off): ").lower()
        
        if choice == "off":
            print("\nTurning off... Goodbye! 👋")
            machine_on = False
        elif choice == "report":
            # Use the objects' report methods
            print("\n📊 Current Status Report:")
            print("-" * 40)
            coffee_maker.report()
            money_machine.report()
        else:
            # Try to find the drink in the menu
            drink = menu.find_drink(choice)
            
            if drink:
                # Check if resources are sufficient using the coffee_maker object
                if coffee_maker.is_resource_sufficient(drink):
                    # Process payment using the money_machine object
                    if money_machine.make_payment(drink.cost):
                        # Make the coffee using the coffee_maker object
                        coffee_maker.make_coffee(drink)


if __name__ == "__main__":
    main()
