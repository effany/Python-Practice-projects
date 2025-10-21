import random

rock = """
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
"""

paper = """
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
"""

scissors = """
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
"""

handshape_mapping = {"rock": rock, "paper": paper, "scissors": scissors}

rules = {
    "rock": "scissors",
    "scissors": "paper",
    "paper": "rock"
}

# Validate user input
while True:
    try:
        user_input = int(input("Enter your choice: 0 for rock, 1 for paper, 2 for scissors: "))
        if user_input not in [0, 1, 2]:
            print("No such choice! Try again!")
            continue
        break
    except ValueError:
        print("Invalid input! Please enter a number.")

# Correct the range for computer's choice
computer = random.randint(0, 2)

def decide_shape(input, by_who):
    if input == 0:
        print(f"{by_who} choose rock {rock}")
        return "rock"
    elif input == 1:
        print(f"{by_who} choose paper {paper}")
        return "paper"
    elif input == 2:
        print(f"{by_who} choose scissors {scissors}")
        return "scissors"
    
user_shape = decide_shape(user_input, "You")
computer_shape = decide_shape(computer, "Computer")

def beats():
    return rules[user_shape] == computer_shape


def play_game():

    if user_input == computer:
        print("It's a tie!") 
    elif beats():
        print("You Win!")
    else:
        print("You lost!")

play_game()