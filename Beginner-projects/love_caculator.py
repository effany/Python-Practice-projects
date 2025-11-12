def calculate_love_score(name1, name2):
    combined_name = name1 + name2
    true_total = 0
    love_total = 0
    true_love_total = 0
    for letter in "true":
        true_total += combined_name.count(letter)
    for letter in "love":
        love_total += combined_name.count(letter)
    true_love_total = int(str(true_total) + str(love_total))
    return true_love_total


