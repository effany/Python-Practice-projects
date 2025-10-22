import string
import random

letters = list(string.ascii_letters)
numbers = [str(i) for i in range(0, 10)]
symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]

nr_letters = int(input("How many letters would you like in your passwrod?\n"))

nr_symbols = int(input("How many symbols do you like?\n"))

nr_numbers = int(input("How many numbers woulr you like?\n"))

def random_picks(array, number_of_item):
    random_picks = random.sample(array, number_of_item)
    return random_picks

def generate_password():
    random_letters = random_picks(letters, nr_letters)
    random_symbols = random_picks(symbols, nr_symbols)
    random_numbers = random_picks(numbers, nr_numbers)

    password = random_letters + random_symbols + random_numbers

    random.shuffle(password)
    
    password = ''.join(password)

    print(f"Your password is {password}")


generate_password()

