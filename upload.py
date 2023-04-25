import os
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # get the uploaded file
        uploaded_file = request.files['file']
        # get the file extension
        file_ext = os.path.splitext(uploaded_file.filename)[1]
        # save the file to a directory
        uploaded_file.save('uploads/' + uploaded_file.filename)
        # perform analysis on the uploaded data
        if file_ext == '.csv':
            df = pd.read_csv('uploads/' + uploaded_file.filename)
            # perform analysis on the CSV data
        elif file_ext == '.txt':
            with open('uploads/' + uploaded_file.filename, 'r') as f:
                data = f.read()
            # perform analysis on the text data
        elif file_ext in ['.xls', '.xlsx']:
            df = pd.read_excel('uploads/' + uploaded_file.filename)
            # perform analysis on the Excel data
        elif file_ext == '.json':
            with open('uploads/' + uploaded_file.filename, 'r') as f:
                data = f.read()
            # perform analysis on the JSON data
        else:
            return 'Unsupported file type'
        # return the result to the user
        return 'Analysis result for ' + uploaded_file.filename
    else:
        return render_template('fileupload.html')

if __name__ == '__main__':
    app.run(debug=True)