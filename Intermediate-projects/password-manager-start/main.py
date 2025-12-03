from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []
    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += ([random.choice(symbols) for _ in range(nr_symbols)])
    password_list += ([random.choice(numbers) for _ in range(nr_numbers)])

    random.shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def clear_data():
    website_entry.delete(0,END)
    password_entry.delete(0, END)

def save_data_to_file():
    website_data = website_entry.get().capitalize()
    email_data = email_entry.get()
    password_data = password_entry.get()
    
    new_data = {
        website_data: {
            "email": email_data, 
            "password": password_data
        }
        }

    if len(website_data) == 0 or len(password_data) ==0:
        messagebox.showwarning(title="Opps!", message="Dont leave a blank field!")
    else:
        # is_ok = messagebox.askokcancel(title=website_data, message=f"These are the details entered {entry_data}, Is it ok?")
        if len(website_data) != 0 and len(password_data) != 0:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("data.json", "w") as file:
                    json.dump(new_data, file, indent=4) 
            else:
                data.update(new_data)

                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                clear_data()
    
# ---------------------------- SEARCH WEBSITE ------------------------------- #

def search_web():
    search_term = website_entry.get().capitalize()
    try: 
        with open("data.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
        print("Data File doesn't exist, put some entry first")
    else:
        if search_term in data:
            result_email = data[search_term]["email"]
            result_password = data[search_term]["password"]
            messagebox.showinfo(title=search_term, message=f"email: {result_email}, password: {result_password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for website {search_term}")
    

    
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website: ")
email_username_label = Label(text="Email/Username: ")
password_label = Label(text="Password: ")

website_label.grid(column=0, row=1)
email_username_label.grid(column=0, row=2)
password_label.grid(column=0, row=3)

website_entry = Entry(width=21)
email_entry = Entry(width=35)
password_entry = Entry(width=21)
website_entry.focus()
email_entry.insert(0, "effany28119@gmail.com")


website_entry.grid(column=1, row=1, columnspan=2, sticky=W)
email_entry.grid(column=1, row=2, columnspan=2, sticky=W)
password_entry.grid(column=1, row=3, sticky=W)

generate_button = Button(text="Generate Password", highlightthickness=0, command=generate_password)
add_button = Button(text="Add", width=36, command=save_data_to_file)
search_button = Button(text="Search Website", highlightthickness=0, command=search_web)


generate_button.grid(column=2, row=3)
add_button.grid(column=1, row=4, columnspan=2)
search_button.grid(column=2, row=1)

window.mainloop()