from colour_extract_manager import ColourExtractMaganer
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def home():
    display_file = "./static/user_upload/display.png"
    if os.path.exists(display_file):
        os.remove(display_file)
    dummy_image = "user_upload/dummy.png"
    return render_template('index.html', dummy_image=dummy_image)


@app.route('/submit_img', methods=['POST'])
def upload_image():
    selected_file = request.files['file']
    new_file = selected_file.save('./static/user_upload/display.png')

    img_path = "./static/user_upload/display.png"
    colour_manager = ColourExtractMaganer(img_path)
    all_colors = colour_manager.all_colors
    
    return render_template('index.html', all_colors=all_colors)


