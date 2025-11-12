import random

CARDS = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

def calculate_score(cards):
    """Calculate the score, handling Ace (11) conversion to 1 if needed."""
    score = sum(cards)
    num_aces = cards.count(11)
    
    # Convert Aces from 11 to 1 if score is over 21
    while score > 21 and num_aces > 0:
        score -= 10  # Converting 11 to 1 reduces score by 10
        num_aces -= 1
    
    return score

def draw_card():
    """Draw a random card from the deck."""
    return random.choice(CARDS)

def display_hands(player_name, player_cards, computer_cards, hide_computer=False):
    """Display current hands and scores."""
    player_score = calculate_score(player_cards)
    print(f"\n{player_name}'s cards: {player_cards}, score: {player_score}")
    
    if hide_computer:
        print(f"Computer's first card: [{computer_cards[0]}]")
    else:
        computer_score = calculate_score(computer_cards)
        print(f"Computer's cards: {computer_cards}, score: {computer_score}")

def determine_winner(player_cards, computer_cards):
    """Determine the winner and return result message."""
    player_score = calculate_score(player_cards)
    computer_score = calculate_score(computer_cards)
    
    if player_score > 21:
        return "You went over. You lose!"
    elif computer_score > 21:
        return "Computer went over. You win!"
    elif player_score > computer_score:
        return "You win!"
    elif player_score < computer_score:
        return "Computer wins!"
    else:
        return "It's a draw!"

def play_blackjack():
    """Main game logic for a single round of blackjack."""
    player_name = input("Tell me your name: ")
    
    # Initial deal
    player_cards = [draw_card(), draw_card()]
    computer_cards = [draw_card()]
    
    display_hands(player_name, player_cards, computer_cards, hide_computer=True)
    
    # Player's turn
    while calculate_score(player_cards) < 21:
        choice = input("Type 'y' to get another card, type 'n' to pass: ").lower()
        
        if choice == 'y':
            player_cards.append(draw_card())
            display_hands(player_name, player_cards, computer_cards, hide_computer=True)
        elif choice == 'n':
            break
        else:
            print("Invalid input! Please type 'y' or 'n'.")
    
    # Computer's turn (only if player hasn't busted)
    if calculate_score(player_cards) <= 21:
        while calculate_score(computer_cards) < 17:
            computer_cards.append(draw_card())
    
    # Show final hands and determine winner
    print("\n--- Final Hands ---")
    display_hands(player_name, player_cards, computer_cards, hide_computer=False)
    print(f"\n{determine_winner(player_cards, computer_cards)}")

def main():
    """Main game loop."""
    while True:
        play_again = input("\nDo you want to play a game of Blackjack? Type 'y' or 'n': ").lower()
        
        if play_again == 'y':
            play_blackjack()
        elif play_again == 'n':
            print("Thanks for playing!")
            break
        else:
            print("Invalid input! Please type 'y' or 'n'.")

if __name__ == "__main__":
    main()
