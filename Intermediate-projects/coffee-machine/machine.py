from resources import info

COINS = {
    "quarters": 0.25,
    "dimes": 0.10,
    "nickels": 0.05,
    "pennies": 0.01
}

def get_default_resources():
    """Get the default starting resources from config."""
    return info[1]["resources"]

def get_current_resources(used_resource):
    """Calculate remaining resources based on what's been used."""
    default = get_default_resources()
    return {
        "water": default["water"] - used_resource["water"],
        "milk": default["milk"] - used_resource["milk"],
        "coffee": default["coffee"] - used_resource["coffee"]
    }

def print_report(used_resource, total_profit):
    """Display current resource levels and money earned."""
    data = get_current_resources(used_resource)
    print(f"Water: {data['water']}ml")
    print(f"Milk: {data['milk']}ml")
    print(f"Coffee: {data['coffee']}g")
    print(f"Money: ${total_profit:.2f}\n")

def get_ingredients(coffee_type):
    return info[0]["MENU"][coffee_type]["ingredients"]

def get_price(coffee_type):
    return info[0]["MENU"][coffee_type]["cost"]

def are_resources_sufficient(coffee_type, used_resource):
    """Check if there are enough resources to make the requested coffee."""
    current_resources = get_current_resources(used_resource)
    needed_ingredients = get_ingredients(coffee_type)
    
    for ingredient in needed_ingredients:
        if needed_ingredients[ingredient] > current_resources[ingredient]:
            print(f"Sorry, there is not enough {ingredient}.")
            return False
    return True

def calculate_total_money(inserted_coins):
    """Calculate the total value of inserted coins."""
    return sum(COINS[coin_type] * pieces for coin_type, pieces in inserted_coins.items())

def is_payment_sufficient(total_inserted, coffee_type):
    """Check if the payment is enough for the coffee."""
    price = get_price(coffee_type)
    if total_inserted >= price:
        return True
    else:
        print(f"Sorry, that's not enough money. ${total_inserted:.2f} refunded.")
        return False

def select_coffee():
    """Prompt user to select a coffee type."""
    while True:
        try:
            choice = int(input("Press 1 for espresso, 2 for latte, 3 for cappuccino: "))
            if choice == 1:
                return "espresso"
            elif choice == 2:
                return "latte"
            elif choice == 3:
                return "cappuccino"
            else:
                print("Invalid choice. Please select 1, 2, or 3.")
        except ValueError:
            print("Please enter a valid number.")

def collect_coins():
    """Prompt user to insert coins and return the dictionary."""
    print("Please insert coins.")
    inserted_coins = {}
    try:
        for coin_type in COINS.keys():
            pieces = int(input(f"How many {coin_type}? "))
            inserted_coins[coin_type] = pieces
        return inserted_coins
    except ValueError:
        print("Invalid input. Transaction cancelled.")
        return None

def make_coffee(coffee_type, inserted_coins, used_resource):
    """
    Attempt to make coffee. Returns (success, profit) tuple.
    success: True if coffee was made, False otherwise
    profit: Money earned from this transaction (0 if failed)
    """
    # Check resources first
    if not are_resources_sufficient(coffee_type, used_resource):
        return False, 0
    
    # Calculate payment
    total_inserted = calculate_total_money(inserted_coins)
    price = get_price(coffee_type)
    
    # Check if payment is sufficient
    if not is_payment_sufficient(total_inserted, coffee_type):
        return False, 0
    
    # Calculate change and dispense coffee
    change = total_inserted - price
    if change > 0:
        print(f"Here is ${change:.2f} in change.")
    print(f"Here is your {coffee_type} ☕ Enjoy!\n")
    
    # Update used resources
    needed_ingredients = get_ingredients(coffee_type)
    for ingredient in needed_ingredients:
        used_resource[ingredient] += needed_ingredients[ingredient]
    
    return True, price
    
def top_up_resources(used_resource):
    for item in used_resource:
        used_resource[item] = 0
    
    return used_resource


def main():
    """Main program loop for the coffee machine."""
    used_resource = {
        "water": 0,
        "milk": 0,
        "coffee": 0
    }
    total_profit = 0.0

    while True:
        print("\n☕ Welcome to the Coffee Maker!")
        print("=" * 40)
        try:
            action = int(input(
                "Enter 0 to make coffee\n"
                "Enter 1 to view report\n"
                "Enter 2 to refill resources\n"
                "Enter 3 to turn off machine\n"
                "Your choice: "
            ))
        except ValueError:
            print("Please enter a valid number (0-3).")
            continue
        
        if action == 3:
            print("\nTurning off... Goodbye! 👋")
            break
        elif action == 1:
            print("\n📊 Current Resources Report:")
            print("-" * 40)
            print_report(used_resource, total_profit)
        elif action == 2:
            used_resource = top_up_resources(used_resource)
            current = get_current_resources(used_resource)
            print("\n✅ Resources refilled!")
            print(f"Water: {current['water']}ml | Milk: {current['milk']}ml | Coffee: {current['coffee']}g\n")
        elif action == 0:
            coffee_type = select_coffee()
            inserted_coins = collect_coins()
            
            if inserted_coins is None:  # Handle cancelled transaction
                continue
            
            print(f"\nYou selected: {coffee_type.capitalize()}")
            success, profit = make_coffee(coffee_type, inserted_coins, used_resource)
            
            if success:
                total_profit += profit
        else:
            print("Invalid choice. Please select 0, 1, 2, or 3.")


if __name__ == "__main__":
    main()
