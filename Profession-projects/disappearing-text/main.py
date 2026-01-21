from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta


window = Tk()
window.title('If you dont write, you will LOST everything')
window.minsize(width=1600, height=800)
window.config(padx=20, pady=20, bg="#FFE4EF")
instruction_label = Label(text="Welcome, If you stop for over the seconds you set, all your writings will be gone!",
                          bg="#FFE4EF",
                          font=('Arial', 24, 'bold'),
                          padx=80
                        )
instruction_label.grid(column=2, row=2)



# user enter the timer they want
timer_label = Label(text="enter the seconds you'd like to have:", font=('Arial', 20, 'bold'), bg="#F39EB6")
timer_label.grid(column=2, row=0)
timer_box = Entry(width=24, font=('Arial', 15))
timer_box.grid(column=2, row=1)
timer_box.insert(0, "5")
SECONDS = int(timer_box.get())

#typed in text box
text_box = Text(window, height=30, width=120, wrap=WORD, font=('Arial', 15), bg="#F7F6D3", highlightthickness=0)
text_box.grid(column=2, row=4)

# count down label 

count_down_label = Label(text=SECONDS, font=('Arial', 20, 'bold'), bg="#B8DB80")
count_down_label.grid(column=2, row=3)

def key_handler(event):
    global SECONDS
    # every keystrok will reset the timer. 
    SECONDS = int(timer_box.get())
    window.after_cancel(current_timer)
    timer(SECONDS)

window.bind('<Key>', key_handler)

def timer(count):
    global current_timer, count_down_label
    if count > 0:
        current_timer = window.after(1000, timer, count - 1)
        count_down_label.config(text=count)
    
    elif count == 0:
        count_down_label.config(text=count)
        text_box.delete('1.0', END)

current_timer = timer(5)


window.mainloop()