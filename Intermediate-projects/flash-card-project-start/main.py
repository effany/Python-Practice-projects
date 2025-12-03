from tkinter import *
from components.canva import MyCanvas
from components.button import MyButton
import pandas

BACKGROUND_COLOR = "#B1DDC6"
CORRECT_IMG = "./images/right.png"
WRONG_IMG = "./images/wrong.png"

#timer = window.after(3000, count_down, count - 1)

def known_word():
    global flip_timer
    window.after_cancel(flip_timer)
    current_word = canva.current_word
    canva.add_to_known_list(current_word)
    canva.update_cz_word()
    flip_timer = window.after(3000, canva.show_en_answer)


def flip_card():
    global flip_timer
    window.after_cancel(flip_timer)
    canva.update_cz_word()
    flip_timer = window.after(3000, canva.show_en_answer)


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canva = MyCanvas()
canva.update_cz_word()
flip_timer = window.after(3000, canva.show_en_answer)

correct_button = MyButton(CORRECT_IMG, 1, 1, known_word)
wrong_button = MyButton(WRONG_IMG, 0, 1, flip_card)






window.mainloop()