import json
import random

class RandomWordsGenerator:
   
    def __init__(self):
         with open('random-text.json') as file:
            self.word_list = json.load(file)['words']

    def get_random_words(self, count):
        picked_words = random.choices(self.word_list, k=count)
        return picked_words
        

