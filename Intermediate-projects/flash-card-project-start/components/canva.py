from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")

class MyCanvas:
    def __init__(self):
        self.canva = Canvas(width=800, height=526, highlightthickness=0, background=BACKGROUND_COLOR)
        self.front_img = PhotoImage(file="./images/card_front.png")
        self.back_img = PhotoImage(file="./images/card_back.png")
        self.canva.create_image(400, 263, image=self.front_img, tags="front_img")
        self.title_text = self.canva.create_text(400, 150, text="", font=TITLE_FONT, fill="black")
        self.word_text = self.canva.create_text(400, 263, text="", font=WORD_FONT, fill="black")
        self.canva.grid(column=0, row=0, columnspan=2)
        self.current_word = None
        try:
            original_data = pandas.read_csv("./data/cz_words_1000-2000.csv")
            known_data = pandas.read_csv("./data/known_words.csv")
            # Load existing known words into the list
            self.known_list = known_data.to_dict(orient='records')
            filtered_data = original_data[~original_data['cz'].isin(known_data["cz"])]
            self.df = filtered_data.to_dict(orient='records')
                
        except FileNotFoundError:
            data = pandas.read_csv("./data/cz_words_1000-2000.csv")
            self.df = data.to_dict(orient="records")
            self.known_list = []
        

    def new_word_pair(self):
        return random.choice(self.df)


    def update_cz_word(self):
        new_word_pair = self.new_word_pair()
        # Use itemconfig to update existing text instead of creating new text
        self.canva.itemconfig("front_img", image=self.front_img)
        self.canva.itemconfig(self.title_text, text="Czech", fill="black")
        self.canva.itemconfig(self.word_text, text=new_word_pair["cz"], fill="black")
        self.current_word = new_word_pair
        

    def show_en_answer(self):
        self.canva.itemconfig("front_img", image=self.back_img)
        self.canva.itemconfig(self.title_text, text= "English", fill="white")
        self.canva.itemconfig(self.word_text, text=self.current_word["en"], fill="white")

    def add_to_known_list(self, know_word):
        self.known_list.append(know_word)
        self.df.remove(know_word)  # Remove from current session too
        df = pandas.DataFrame(self.known_list)
        df.to_csv("./data/known_words.csv", index=False)