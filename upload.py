import os
import pandas as pd
from flask import Flask, render_template, request
from InfluxDBScript import send_to_DB
from werkzeug.datastructures import FileStorage # FileStorage used to represent uploaded files
from error_algorithms import dataframe_to_array
from error_algorithms import mean_absolute_error

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
@app.route('/home')
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
        MLE_file_ext = os.path.splitext(MLE_file.filename)[1]

        # next line currently does not work, need to host code somewhere that contains uploads directory
        #uploaded_training_data.save('uploads/' + uploaded_training_data.filename) # save the training data so that MLE can view, but only store test data in DB
        
        # perform analysis on the uploaded data
        MLE_df = file_to_df(MLE_file, MLE_file_ext)

        if MLE_df is not None:
            # perform analysis on the MLE pandas dataframe
            MLE_arr = dataframe_to_array(MLE_df) #turns panda dataframe to usable array (cuts out date column, needs iterating to work on different files)
            # TODO: implement test set
            error_arr = mean_absolute_error(MLE_arr,'''testSet_arr''') #gives MAE value for error calculations, currently has placeholder for test set
            # TODO: add different error analysis functions
            result = "Error analyis gets performed"
        else:
            return 'Unsupported file type'
        
        # return the result to the user
        return 'Analysis result for ' + MLE_file.filename
    else:
        return render_template('MLE_upload.html')



PORT=5000
DEBUG=True

if __name__ == "__main__":
    app.run(port=PORT, host="0.0.0.0", debug=DEBUG)