# try:
#     file = open("a_file.txt")
#     a_dictionary = {"key":"value"}
#     print(a_dictionary["key"])
# except FileNotFoundError:
#     file = open("a_file.txt", "w")
#     file.write("something")
# except KeyError as error_message:
#     print(f"that key {error_message} doens't exist")

# else:
#     # execute when other stuff all goes well
#     content = file.read()
#     print(content)

# finally:
#     # no matter what happen it'll always run 
#     file.close()
#     print("file was closed")

height = float(input("height: "))
weight = int(input("weight: "))

if height > 3:
    # raise is for the error that we made up and we want to catch it
    raise ValueError("Human height should not be over 2 meters")

bmi = weight /height ** 2
print(bmi)