import random

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    
def draw_cards(initial_card_array):
    new_card = random.choice(cards)
    initial_card_array.append(new_card)
    return initial_card_array

def is_over_21(player_card_array):
    player_score = sum(player_card_array)
    if player_score > 21:
        return True
    else:
        return False

def computer_final_card_draw(computers_card):
    while sum(computers_card) < 17:
        new_cards = random.choice(cards)
        computers_card.append(new_cards)
    print(f"computer final cards {computers_card}")
    return computers_card

def player_win(players_card, computers_card):
    if sum(computers_card) > 21 and 11 in computers_card:
        computers_card.remove(11)
        computers_card.append(1)
        print("remove 11 and append 1")
    sum_computer_score = sum(computers_card)
    sum_player_score = sum(players_card)
    if sum_computer_score == sum_player_score:
        return "equal"
    elif sum_player_score <= 21 and (sum_computer_score > 21 or sum_player_score > sum_computer_score):
        return True
    else:
        return False

def print_statement(name, cards, round, score):
    print(f"{name}'s cards: {cards}, {round} score: {score}")


continue_playing = True

while continue_playing:
    to_play = input("Do you want to play a game of Blackjack? Type 'y' or 'n': ").lower()
    if to_play == 'y':
        player_name = input("Tell me your name: ")
        players_card = random.sample(cards, 2)
        player_init_score = sum(players_card)
        computers_card = random.sample(cards, 1)
        computer_init_score = sum(computers_card)
        print_statement(player_name, players_card, "current", player_init_score )
        print(f"Computer's first card: {computers_card}")
        while True:
            get_another_card = input("Type 'y' to get another card, type 'n' to pass: ").lower()
            if get_another_card == 'y':
                draw_cards(players_card)
                player_accumulative_score = sum(players_card)
                print_statement(player_name, players_card, "current", player_accumulative_score )
                if is_over_21(players_card) and 11 in players_card:
                    print("remove 11 and append 1")
                    players_card.remove(11)
                    players_card.append(1)
                elif is_over_21(players_card) and 11 not in players_card:
                    print_statement(player_name,players_card, "final", sum(players_card) )
                    print_statement("Computer", computers_card, "final", sum(computers_card))
                    print(f"You went over. You lose!! ")
                    break
            elif get_another_card == 'n':
                final_computer_cards = computer_final_card_draw(computers_card)
                if sum(final_computer_cards) > 21:
                    print_statement(player_name,players_card, "final", sum(players_card) )
                    print_statement("Computer", final_computer_cards, "final", sum(final_computer_cards))
                    print(f"Computer overdrown! {player_name} win!")
                elif player_win(players_card, final_computer_cards):
                    print_statement(player_name,players_card, "final", sum(players_card) )
                    print_statement("Computer", final_computer_cards, "final", sum(final_computer_cards))
                    print(f"Congratulations! {player_name} win!")
                elif player_win(players_card, final_computer_cards) == "equal":
                    print({"You're equal! No winner"})
                else:
                    print_statement(player_name,players_card, "final", sum(players_card) )
                    print_statement("Computer", final_computer_cards, "final", sum(final_computer_cards))
                    print("Opps! Computer win!")
                break
            else:
                print("invalid response!")
    elif to_play == "n":
        continue_playing = False
    else: 
        print("Invalid input")

        
