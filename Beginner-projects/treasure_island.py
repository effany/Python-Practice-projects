def game_over(message):
    """Prints a game over message and exits the game."""
    print(message)
    exit()

def treasure_island():
    print("Welcome to Treasure Island. Your mission is to find the treasure.")

    first_step = input("Left or Right? ").lower()
    if first_step == "right":
        game_over("Fall into a hole. Game over.")
    elif first_step != "left":
        game_over("Invalid choice. Game over.")

    print("To next step.")
    second_step = input("Swim or Wait? ").lower()
    if second_step == "swim":
        game_over("Attacked by trout. Game over.")
    elif second_step != "wait":
        game_over("Invalid choice. Game over.")

    third_question = input("Which door? Red, Blue, or Yellow? ").lower()
    if third_question == "red":
        game_over("Burned by fire. Game over.")
    elif third_question == "blue":
        game_over("Eaten by beast. Game over.")
    elif third_question == "yellow":
        print("You Win!!")
    else:
        game_over("Invalid choice. Game over.")

# Start the game
treasure_island()