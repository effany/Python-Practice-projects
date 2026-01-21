from text_to_speech import TextToSpeech
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pdf_processor import PDFProcessor
import threading
from tkinter.filedialog import asksaveasfile

# Create custom httpx client with SSL verification disabled




window = Tk()
window.title("Convert Your PDF to Voice memo!")
window.config(padx=20, pady=20)

pdf_processor = PDFProcessor()


# user's input on AI instructions

instruction_label = Label(text="Enter your ideal tone instructions")
instruction_label.grid(column=2, row=1)
instruction_input = Text(width=30, height=20, bg="#F4F4F4")
instruction_input.grid(column=2, row=2)
instructions = ""
voice = ""

voices = [
    "alloy",
    "ash",
    "ballad",
    "coral",
    "echo",
    "fable",
    "nova",
    "onyx",
    "sage",
    "shimmer",
    "verse",
    "marin",
    "cedar"
]

voice_label = Label(text="Select a voice")
voice_label.grid(column=3, row=1)
cb = ttk.Combobox(window, values=voices)
cb.set("Select a voice type")
cb.grid(column=3, row=2)

status_label = Label(text="")
status_label.grid(column=4, row=2)

def grab_data():
    global instructions, voice
    instructions = instruction_input.get("1.0", END).strip()  # .strip() removes trailing newline
    voice = cb.get()

def convert_to_voice():
    global status_label
    grab_data()
    status_label.config(text="Converting... Please wait")

    if not pdf_processor.full_text:
        status_label.config(text="Error: No PDF selected or extracted", bg="#FF8FB7")
        return
    
    if voice == "Select a voice type" or not voice:
        status_label.config(text="Error: Please select a voice", bg="#FF8FB7")
        return

    def run_conversion():
        global speech_file_path
        try:
            agent = TextToSpeech(pdf_processor.full_text, instructions, voice)
            status_label.config(text="✓ Conversion complete!")
            speech_file_path = agent.speech_file_path
            download_btn = Button(text="Download file", command=lambda: save_voice_file(speech_file_path))
            download_btn.grid(column=4, row=3)
            clear_selections()
        except Exception as e:
            status_label.config(text=f"Error: {e}")

    thread = threading.Thread(target=run_conversion)
    thread.start()

def clear_selections():
    global pdf_processor, instructions, voice, window
    pdf_processor.file_path = ""
    instructions = ""
    voice = ""
    window.update()

pdf_processor.select_button.config(command=lambda: [pdf_processor.select_file(), pdf_processor.on_file_selected()])

convert_button = Button(text='Convert to Voice', command=convert_to_voice)
convert_button.config(width=20, height=1 , bg="#005461")
convert_button.grid(column=4, row=1)


# implement download file function

def save_voice_file(source_file):
    destination = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")]
    )
    if destination: 
        import shutil 
        shutil.move(source_file, destination)

window.mainloop()