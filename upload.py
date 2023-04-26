import os
import pandas as pd
from flask import Flask, render_template, request
from InfluxDBScript import send_to_DB
from werkzeug.datastructures import FileStorage # FileStorage used to represent uploaded files

app = Flask(__name__)

def file_to_df(file: FileStorage, file_ext: str): # Converts a file to a pandas dataframe
    dataframe = None
    # Use pandas fnx based on the file type:
    if file_ext == '.csv': # Pandas read_csv can read .csv and .txt files 
        dataframe = pd.read_csv(file)
    elif file_ext == '.txt':
        dataframe = pd.read_csv(file, sep=' ') # for .txt files, the separator is a space character
    elif file_ext in ['.xls', '.xlsx']:
        dataframe = pd.read_excel(file)     
    elif file_ext == '.json':
        dataframe = pd.read_json(file)
    
    return dataframe


@app.route('/')
@app.route('/index')
def home():
    return render_template('home.html')    

@app.route('/contributor_upload', methods=['GET', 'POST'])
def contributor_upload():
    if request.method == 'POST':
        # get the uploaded file
        uploaded_training_data = request.files['training_data']
        uploaded_test_data = request.files['test_data']

        # get the file extension, assuming user inputs data correctly so the file_ext will be the same for both uploaded files
        file_ext = os.path.splitext(uploaded_training_data.filename)[1]
        # save the file to a directory

        # next line currently does not work, need to host code somewhere that contains uploads directory
        #uploaded_training_data.save('uploads/' + uploaded_training_data.filename) # save the training data so that MLE can view, but only store test data in DB
        
        # Call fxn to get dataframe for training data and test data
        trng_df = None
        tst_df = None

        trng_df = file_to_df(uploaded_training_data, file_ext)
        tst_df = file_to_df(uploaded_test_data, file_ext)
        
        if((trng_df is not None) and (tst_df is not None)):
            res_trng = send_to_DB(trng_df) # pass the pandas dataframe to function which will store the data in DB
            res_tst = send_to_DB(tst_df)
            if((res_trng==True) and (res_tst==True)):
                return 'Files Were Submitted To Database'
            else:
                return 'Send functions did not return True, error sending files to Database'
        else:
            return 'Unsupported file type'
    else:
        return render_template('contributor_upload.html')


@app.route('/MLE_upload', methods=['GET', 'POST'])
def MLE_upload():
    # MLE will upload their new data after doing their Machine Learning with the training data
    # Then do the error analysis below
    if request.method == 'POST':
        MLE_file = request.files['MLE_file']
        file_ext = os.path.splitext(MLE_file.filename)[1]
        
        # perform analysis on the uploaded data
        if file_ext == '.csv':
            df = pd.read_csv('uploads/' + MLE_file.filename)
            # perform analysis on the CSV data
        elif file_ext == '.txt':
            with open('uploads/' + MLE_file.filename, 'r') as f:
                data = f.read()
            # perform analysis on the text data
        elif file_ext in ['.xls', '.xlsx']:
            df = pd.read_excel('uploads/' + MLE_file.filename)
            # perform analysis on the Excel data
        elif file_ext == '.json':
            with open('uploads/' + MLE_file.filename, 'r') as f:
                data = f.read()
            # perform analysis on the JSON data
        else:
            return 'Unsupported file type'
        # return the result to the user
        return 'Analysis result for ' + MLE_file.filename
    else:
        return render_template('MLEupload.html')




PORT=5000
DEBUG=True

if __name__ == "__main__":
    app.run(port=PORT, host="0.0.0.0", debug=DEBUG)