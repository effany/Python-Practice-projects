import random 

word_list = ["Apple", "Galaxy", "Python", "Horizon", "Quantum", "Eclipse", "Velocity", "Nebula", "Zenith", "Cascade"]
random_word = random.choice(word_list)
lives = 6

stages = ['''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========
''', 
'''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========
''', 
'''
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
''', 
'''
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
''', 
'''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
''', 
'''
  +---+
  |   |
  O   |
      |
      |
      |
=========
''', 
'''
  +---+
  |   |
      |
      |
      |
      |
=========
''']

guesses = []


def generate_placeholder():
    placeholder = []
    for i in random_word:
        placeholder.append("_")
    return placeholder

placeholders = generate_placeholder()
print(" ".join(placeholders))

def replace(guess):
    global lives
    for index, letter in enumerate(random_word):
        if guess == letter.lower():
            placeholders[index] = letter
    print(" ".join(placeholders))
    return placeholders


game_playing = True

def check_life(placeholders, guess_letter):
    global game_playing, lives
    if "_" not in placeholders:
        print("Congratulations!")
        game_playing = False
        exit()
    elif guess_letter not in random_word.lower():  # Ensure case-insensitive comparison
        if guess_letter not in placeholders and guess_letter not in guesses:  # Prevent deducting lives for already guessed letters
            lives -= 1
            guesses.append(guess_letter)
            print(stages[lives])
        elif guess_letter not in placeholders and guess_letter in guesses:
            print("You've guessed this word before! Try again")
            if lives == 0:
                print("You are DEAD!")
                game_playing = False
                exit()
            print(f"You have {lives} lives left")
            

def game():
    global game_playing
    while game_playing:
        guess_letter = input(f"please enter a letter: ").lower()
        check_life(placeholders, guess_letter)
        replace(guess_letter)
    
game()
