from tkinter import *

def convert_miles_to_km():
    miles = int(input_miles.get())
    km = round(miles * 1.609)
    display_km.config(text=km)

FONT = ("Arial", 20, "normal")
window = Tk()
window.minsize(width=500, height=300)
window.config(padx=100, pady=100)
window.title("Mile to Km Converter")
miles_label = Label(text="Miles", font=FONT)
miles_label.grid(column=2, row=0)
is_equal_to_lable = Label(text="is equal to", font=FONT)
is_equal_to_lable.grid(column=0, row=1)
km_label = Label(text="Km", font=FONT)
km_label.grid(column=2, row=1)
input_miles = Entry(width=10)
input_miles.grid(column=1, row=0)
display_km = Label(text=" ", font=FONT)
display_km.grid(column=1, row=1)
calculate_button = Button(text="Calculate", command=convert_miles_to_km)
calculate_button.grid(column=1, row=2)

    

window.mainloop()