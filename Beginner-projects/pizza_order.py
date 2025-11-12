print("Welcome to Python Pizza Deliveries!")

size = input("Pizza size (S/M/L): ").upper()
pepperoni = input("Add pepperoni? (Y/N): ").upper()
extra_cheese = input("Add extra cheese? (Y/N): ").upper()

def calculate_price(size, pepperoni, extra_cheese):
    # Base prices by size
    base_prices = {"S": 15, "M": 20, "L": 25}
    
    # Pepperoni prices by size
    pepperoni_prices = {"S": 2, "M": 3, "L": 3}
    
    total = base_prices.get(size, 25)  # Default to Large if invalid size
    total += pepperoni_prices[size] if pepperoni == "Y" else 0
    total += 1 if extra_cheese == "Y" else 0
    
    print(f"Total: ${total}")
    return total

calculate_price(size, pepperoni, extra_cheese)
   



