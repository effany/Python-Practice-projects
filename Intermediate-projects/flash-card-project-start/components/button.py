from tkinter import * 

class MyButton:
    def __init__(self, image_path, column, row, command):
        self.img = PhotoImage(file=image_path)
        self.button = Button(image=self.img, highlightthickness=0, command=command)
        self.button.grid(column=column, row=row)
    


    

