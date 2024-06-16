from flask import Flask, request, render_template, redirect, url_for
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
load_dotenv()

AZURE_COMPUTER_VISION_ENDPOINT = os.getenv("AZURE_COMPUTER_VISION_ENDPOINT")
AZURE_COMPUTER_VISION_KEY = os.getenv("AZURE_COMPUTER_VISION_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        image_data = file.read()
        ocr_result = perform_ocr(image_data)
        return render_template('result.html', ocr_result=ocr_result)

def perform_ocr(image_data):
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_COMPUTER_VISION_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params = {
        'language': 'unk',
        'detectOrientation': 'true'
    }
    response = requests.post(
        f"{AZURE_COMPUTER_VISION_ENDPOINT}//vision/v3.2/ocr",
        headers=headers,
        params=params,
        data=image_data
    )
    response.raise_for_status()
    analysis = response.json()
    ocr_text = ""
    for region in analysis['regions']:
        for line in region['lines']:
            for word in line['words']:
                ocr_text += word['text'] + " "
    return ocr_text.strip()

if __name__ == '__main__':
    app.run(debug=True)
