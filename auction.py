
still_bidding = True
bidder_dic = {}

while still_bidding:
    user = input("what's your name? ")
    bid = int(input("Type your bid "))
    print(f"${user} bid for ${bid}")
    bidder_dic[user] = bid
    print(bidder_dic)
    while True:
        another_user = input("Is there another user? Yes/No ").lower()
        if another_user == "no":
            still_bidding = False
            break
        elif another_user == "yes":
            print("\n" * 100)
            break
        else:
            print("I don't understand this answer, type again")
    
    bidder_dic

print(bidder_dic)    
winner = max(bidder_dic, key=bidder_dic.get)

print(f"Congratulations for winner {winner}")