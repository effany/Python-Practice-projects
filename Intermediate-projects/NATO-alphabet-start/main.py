import pandas

data = pandas.read_csv("nato_phonetic_alphabet.csv")
df = pandas.DataFrame(data)

def generate_phonetic():
    user_input = input("Enter your word: ")
    try:
        input_array = list(user_input.strip().upper())
        alphabet_dict = {row.letter: row.code for (index, row) in df.iterrows()}
        reply_array = [alphabet_dict[letter] for letter in input_array]

    except KeyError:
            print("Sorry only letters")
            generate_phonetic()
    else:
         print(reply_array)

generate_phonetic()



# with open("nato_phonetic_alphabet.csv") as file:
#     file = file.readlines()
#     alphabet_dict = {word.split(",")[0]: word.split(",")[1].strip() for word in file if "letter" and "code\n" not in word.split(",")}
#     print(alphabet_dict)