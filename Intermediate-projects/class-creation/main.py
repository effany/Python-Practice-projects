class User:
    def __init__(self, user_id, username):
        self.username = username
        self.id = user_id
        # provide default value, meaning we dont need to pass it when creating users
        self.followers = 0
        self.following = 0
    
    def follow(self, user):
        user.followers += 1
        self.following += 1


user_1 = User("001", "Amy")
user_2 = User("002", "Jack")



user_1.follow(user_2)

print(user_1.followers)
print(user_1.following)