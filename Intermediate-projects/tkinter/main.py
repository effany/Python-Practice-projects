from tkinter import *
window = Tk()
window.title("My first GUI program")
window.minsize(width=500, height=300)
window.config(padx=20, pady=20)

def button_clicked():
    user_input = input.get()
    my_label.config(text=f"{user_input}")

#Label

my_label = Label(text="I am a Label", font=("Arial", 24, "bold"))
my_label.config(text="New text")
## place is to place it at specific position
# my_label.place(x=100, y=200)
# grid is relative to other componenet 
my_label.grid(column=0, row=0)
# my_label.pack()

# Button
button = Button(text="Click Me", command=button_clicked)
button.grid(column=1, row=1)
# button.pack()

# entry 
input = Entry(width=10)
# input.pack()
input.grid(column=3, row=2)

new_button = Button(text="Click Me 2 ")
new_button.grid(column=2, row=0)



window.mainloop()   