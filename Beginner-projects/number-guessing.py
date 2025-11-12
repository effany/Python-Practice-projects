import random 

def random_number():
    return random.randint(1, 100)

def determine_attempts():
    while True:
        question = input("Choose a difficulty. Type 'easy' or 'hard': ").lower()
        if question == 'easy':
            return 10
        elif question == 'hard':
            return 5
        else:
            print("Invalid input, please try again.")

def check_guess(input_num, target_num):
    if input_num == target_num:
        print("🎉 Congratulations! You got it!")
        return True
    elif input_num > target_num:
        print("Too high.")
        return False
    else:
        print("Too low.")
        return False
    
def play_game():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    target = random_number()
    attempts = determine_attempts()
    guessed_numbers = set()  # Use set for faster lookup
    
    for attempt in range(attempts):
        remaining = attempts - attempt
        print(f"\nYou have {remaining} attempt(s) remaining.")
        
        try:
            user_guess = int(input("Make a guess: "))
            
            if user_guess < 1 or user_guess > 100:
                print("Please guess a number between 1 and 100.")
                continue
                
            if user_guess in guessed_numbers:
                print("You've already guessed that number!")
                continue
            
            guessed_numbers.add(user_guess)
            
            if check_guess(user_guess, target):
                print(f"You won in {attempt + 1} attempt(s)!")
                return
                
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
    
    print(f"\n😞 Game Over! The number was {target}.")

def main():
    play_game()

if __name__ == "__main__":
    main()