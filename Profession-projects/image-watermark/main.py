from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil



# im = Image.open('./assets/test.png')
# im.show()

def get_img():
    global file_path
    fileTypes = [("Image files", "*.png;*.jpg;*.jpeg")]
    file_path = filedialog.askopenfilename(filetypes=fileTypes)
    return ImageTk.PhotoImage(file=file_path)

def select_img():
    global img, image_label, sample_img
    img = get_img()
    if img:
        sample_img_pil = Image.open(file_path)
        sample_img_pil.thumbnail((1000, 1000))  # Tuple! Modifies in-place
        sample_img = ImageTk.PhotoImage(sample_img_pil)
        image_label = Label(window, image=sample_img)
        image_label.grid(column=2, row=5)

def add_water_mark():
    global watermarked_img, processed_image_sample, img
    watermark_path = filedialog.askopenfilename()
    watermark = Image.open(watermark_path)
    img = Image.open(file_path)
    img.paste(watermark, ((img.width - watermark.width) // 2,
                       (img.height - watermark.height) // 2), watermark)
    # Now img is the watermarked result
    img.thumbnail((1000, 1000))  # Shrink for display
    watermarked_img = ImageTk.PhotoImage(img)
    image_label.destroy()
    processed_image_sample = Label(window, image=watermarked_img)
    processed_image_sample.grid(column=2, row=5)

def download_watermarked_img():
    file_path_to_save = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")]
    )
    if file_path_to_save:
        img.save(file_path_to_save)
    processed_image_sample.destroy()

window = Tk()
window.title("Upload your image here")
window.config(padx=20, pady=20)


select_file_btn = Button(text="select file", command=select_img)
select_file_btn.config(width=15, height=1)
select_file_btn.grid(column=1, row=2)
upload_btn = Button(text="Select and add water mark", command=add_water_mark)
upload_btn.grid(column=2, row=2)
download_btn = Button(text="Download the watermarked image",command=download_watermarked_img)
download_btn.grid(column=3, row=2)



window.mainloop()
