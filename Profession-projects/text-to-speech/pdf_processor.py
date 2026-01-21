from tkinter import *
from tkinter import filedialog
from pypdf import PdfReader
import fitz
from PIL import Image, ImageTk
import os


class PDFProcessor:
    def __init__(self):
        self.select_button = Button(text='Select File', command=self.select_file)
        self.select_button.config(width=20, height=1 , bg="#005461")
        self.select_button.grid(column=1, row=1)
        
        self.full_text = ""
        self.file_path = ""

    
    def select_file(self):
        print(self.file_path.split('/'))
        self.file_path = filedialog.askopenfilename()

    def process_file(self):
        try:
            doc = fitz.open(self.file_path)
            full_text = ""
            for page in doc:
                text = page.get_text()
                full_text += text
            self.full_text = full_text
            
        
        except Exception as e:
            return f"Some error has occur {e}"
    
    def on_file_selected(self):
        if self.file_path != "":
            print(self.file_path )
            img = Image.open("./assets/pdf.png")
            img = img.resize((100, 100))
            icon = ImageTk.PhotoImage(img)
            icon_label = Label(image=icon)
            icon_label.image = icon 
            icon_label.grid(column=1, row=2)
            sanitize_file_name = os.path.basename(self.file_path)
            file_name = Label(text=sanitize_file_name)
            file_name.grid(column=1, row=3)
        
        self.process_file()
        
            
        
