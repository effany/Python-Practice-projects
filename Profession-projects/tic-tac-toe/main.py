def has_winner():
    win_combinations = [
        [1,2,3],[4,5,6],[7,8,9],
        [1,4,7],[2,5,8],[3,6,9],
        [1,5,9],[3,5,7]
    ]

    for combo in win_combinations:
        if (pick_dict[combo[0]] == pick_dict[combo[1]] == pick_dict[combo[2]]) and pick_dict[combo[0]] != "?":
            return True
    else:
        False


GAME_IS_ON = True

pick_dict = {
    1: "?",
    2: "?", 
    3: "?",
    4: "?",
    5: "?",
    6: "?",
    7: "?",
    8: "?",
    9: "?",
}

print("""
Here is your position choices

1 | 2 | 3 
-------
4 | 5 | 6
-------
7 | 8 | 9

""")

available_positions = 9

while GAME_IS_ON:
    if available_positions == 0:
        print("Game over! ")
        GAME_IS_ON = False
        exit()
    elif has_winner():
        print("We have a winner!")
        GAME_IS_ON = False
        exit()

    pos = int(input("Pick a position 1 - 9: "))
    if 0 < pos <= 9 and pick_dict[pos] == "?":
        shape = input("Enter a shape O or X: ")
        shape = shape.upper()
        if shape == "O" or shape == "X":
            pick_dict[pos] = shape
            available_positions -= 1
            print(f"""
            {pick_dict[1]} | {pick_dict[2]} | {pick_dict[3]}
            ----------------
            {pick_dict[4]} | {pick_dict[5]} | {pick_dict[6]}
            ----------------
            {pick_dict[7]} | {pick_dict[8]} | {pick_dict[9]}
            """)
            print(f"available positions: {available_positions}")
        else:
            print("I dont recognize the shape. Sorry! Try Again")
    else:
        print("That position is already occupied or out of range. Pick another one!")
        

