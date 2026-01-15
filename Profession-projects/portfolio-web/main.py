from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import requests
import datetime as dt
import os
import json

app = Flask(__name__)
bootstrap = Bootstrap5(app)


def load_certifications():
    try:
        data_path = os.path.join(app.root_path, 'static', 'data', 'certifications.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

CERTIFICATIONS = load_certifications()

def load_volunteering():
    try:
        data_path = os.path.join(app.root_path, 'static', 'data', 'volunteering.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []

VOLUNTEERING = load_volunteering()

@app.route('/')
def home():
    today = dt.datetime.today()
    return render_template('home.html', datetime=today.year, certifications=CERTIFICATIONS, volunteering=VOLUNTEERING)
    


