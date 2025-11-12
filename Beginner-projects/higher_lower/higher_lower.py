from game_data import data
import random

def description(celebrity, position_strings):
    celebrity_details = f"{celebrity["name"]}, {celebrity["description"]}, from {celebrity["country"]}"
    return f"{position_strings}: {celebrity_details}"

def select_celebrity():
    ppl = random.choice(data)
    return ppl

def correct_answer(compare_dic):
    return "a" if compare_dic["a"]["follower_count"] > compare_dic["b"]["follower_count"] else "b"

def user_is_correct(input, compare_dic):
    answer = correct_answer(compare_dic)
    if input.lower() == answer:
        print(f"\ncorrect\n")
        return True
    else:
        return False

def are_same_celebs(celeb1, celeb2):
    if celeb1 == celeb2:
        return True


def main():
        celeb1 = select_celebrity()
        celeb2 = select_celebrity()
        user_points = 0
        while True: 
            if are_same_celebs(celeb1, celeb2):
                celeb2 = select_celebrity()
            compare_dic = {"a": celeb1, "b": celeb2}
            print(description(celeb1, "Compare A"))
            print(description(celeb2, "Against B"))
            user_input = input("Who has more followers? Type 'A' and 'B' ")
            if user_is_correct(user_input, compare_dic):
                celeb1 = celeb2
                celeb2 = select_celebrity()
                user_points += 1
            else:
                print(f"\nThat's wrong! Your final score is {user_points}\n")
                break


if __name__ == "__main__":
    main()