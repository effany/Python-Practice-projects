print("Welcome to the tip calculator!")

# Get inputs with basic validation
total_bill = float(input("What was the total bill? $"))
tip_percentage = int(input("How much tip would you like to give? 10, 12 or 15? "))
group_size = int(input("How many people to split the bill? "))

def calculate_tips(bill, tip_percent, people):
    # Calculate total with tip in one step
    total_with_tip = bill * (1 + tip_percent / 100)
    per_person = total_with_tip / people
    print(f"Each person should pay: ${per_person:.2f}")
    return per_person

calculate_tips(total_bill, tip_percentage, group_size)


