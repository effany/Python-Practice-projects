import string 

alphabet = list(string.ascii_lowercase)



def encrypt(original_text, shift_amount):
    new_text = ""
    for item in original_text:
        if item in alphabet:
            item_index = alphabet.index(item)
            new_index = (item_index + shift_amount) % 26
            new_text += alphabet[new_index]
        else:
            new_text += item  # Keep spaces and other characters unchanged
    print(new_text)
    return new_text  


def decrypt(original_text, shift_amount):
    decrypt_text = ""
    for i in original_text:
        if i in alphabet:
            item_index = alphabet.index(i)
            decrypt_index = (item_index - shift_amount) % 26
            decrypt_text += alphabet[decrypt_index]
        else:
            decrypt_text += i
    print(decrypt_text)
    return 


def caesar(original_text, direction, shift_amount):
    new_text = ""
    for item in original_text:
        if item in alphabet:
            item_index = alphabet.index(item)
            if direction == "encode":
                new_index = (item_index + shift_amount) % len(alphabet)
                new_text += alphabet[new_index]
            elif direction == "decode":
                new_index = (item_index - shift_amount) % len(alphabet)
                new_text += alphabet[new_index]
        else:
                new_text += item
    print(new_text)
    return new_text
            
def check_continue():
    to_continue = input("Continue to encode or decode? Say 'No' to exit the program. ")
    if to_continue.lower() == "no":
        continue_to_run = False
        exit()

continue_to_run = True

while continue_to_run:
    direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
    text = input("Type your message:\n").lower()
    shift = int(input("Type the shift number:\n"))
    caesar(text, direction, shift)
    check_continue()
