import pandas

user_input = input("Enter your word: ")
input_array = list(user_input.strip().upper())

# with open("nato_phonetic_alphabet.csv") as file:
#     file = file.readlines()
#     alphabet_dict = {word.split(",")[0]: word.split(",")[1].strip() for word in file if "letter" and "code\n" not in word.split(",")}
#     print(alphabet_dict)

data = pandas.read_csv("nato_phonetic_alphabet.csv")
df = pandas.DataFrame(data)

alphabet_dict = {row.letter: row.code for (index, row) in df.iterrows()}

reply_array = [alphabet_dict[letter] for letter in input_array]

print(reply_array)

#TODO 1. Create a dictionary in this format:
# {"A": "Alfa", "B": "Bravo"}

#TODO 2. Create a list of the phonetic code words from a word that the user inputs.

