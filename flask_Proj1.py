import os
import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from sendDB import pair_to_DB, sol_to_DB
from retrieveDB import retrieve_DB
from werkzeug.datastructures import FileStorage # FileStorage used to represent uploaded files
import uuid # for generating unique id
import firebase_admin
from firebase_admin import credentials, firestore
import csv

app = Flask(__name__)
app.secret_key = "my_flask_secret"


# Start firestore client
cred = credentials.Certificate("cs-422-project-1-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get vars using request and names of vars, then send to user home page
        
        return redirect(url_for("home")) 
    else:
        return render_template('login_mod.html') 


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # get vars using request and names of vars
        
        return redirect(url_for("home")) 
    else:
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

        # Have the pair of dataframes, this pair needs an id so that can retrieve the corresponding test set when the MLE uploads
        # their solution (for testing, solution will be test set with noise added)

        """
        TS Metadata required from PDF: TS Name, Description, Domain(s), Units, Keywords, 
        Scalar/Vector(univariate/multivariate), Vector size, Length, Sampling Period
        
        TS data required from PDF: Date, Time, Magnitude, other non-magnitude features?
        """

        # Get TS Metadata values from POSTed variables

        TS_name = request.form['TS_pair_name']
        # Training Set Variables

        tr_TS_Name = request.form['tr_TS_name']
        tr_desc = request.form['tr_description']
        tr_dom = request.form['tr_domains']
        tr_uns = request.form['tr_unis']
        tr_univmult = request.form['tr_univmult']
        tr_vecsiz = request.form['tr_vecsiz']
        tr_len = request.form['tr_len']
        tr_samp = request.form['tr_samp']

        # Test Set Variables
        tst_TS_Name = request.form['tst_TS_name']
        tst_desc = request.form['tst_description']
        tst_dom = request.form['tst_domains']
        tst_uns = request.form['tst_units']
        tst_univmult = request.form['tst_univmult']
        tst_vecsiz = request.form['tst_vecsiz']
        tst_len = request.form['tst_len']
        tst_samp = request.form['tst_samp']

        # Get info dict with metadata
        trng_metdat  = {
            "TS Name": tr_TS_Name, # Name of the file
            "Description": tr_desc, # Description of the file
            "Domain(s)": tr_dom, # Domain of the file
            "Units": tr_uns, # Units of the file, for a stock case would be USD, Days (unit for YYYY-MM-DD) and Number of shares (Volume)
            "Univariate/Multivariate": tr_univmult,
            "Vector Size": tr_vecsiz, # number of vars at each time point
            "Length": tr_len, 
            "Sampling Period": tr_samp
        }

        tst_metdat  = {
            "TS Name": tst_TS_Name, # Name of the file
            "Description": tst_desc, # Description of the file
            "Domain(s)": tst_dom, # Domain of the file
            "Units": tst_uns, # Units of the file, for a stock case would be USD, Days (unit for YYYY-MM-DD) and Number of shares (Volume)
            "Univariate/Multivariate": tst_univmult,
            "Vector Size": tst_vecsiz, # number of vars at each time point
            "Length": tst_len, 
            "Sampling Period": tst_samp
        }
        
        if((trng_df is not None) and (tst_df is not None)):
            # Give the pair a unique id, then send each dataframe to the DB along with that id
            uniq_id = uuid.uuid4()
            pair_id = str(uniq_id) # id will be stored as a tag with type string in InfluxDB

            # pass the training set dataframe, training set metadata, test set dataframe, test set metadata, and the pair id to the function
            res = pair_to_DB(trng_df, trng_metdat, tst_df, tst_metdat, pair_id, TS_name, db)
            if(res is True):
                flash('Files Were Submitted To Database', 'info')
            else:
                flash('Send functions did not return True, error sending files to Database', 'info')
        else:
            flash('Unsupported file type', 'info')

        return redirect(url_for("contributor_upload"))
    else:
        return render_template('contributor_upload.html')
    


@app.route('/MLE_view_data', methods=['GET'])
def MLE_view_data():
    # MLE will go to this page and view the training sets that are saved in the database (each training set needs a unique id, so that it can be linked with the test set with the same pair id)
    documents_arr = retrieve_DB(db) # each Firestore document has the keys 'pair_id', 'test_set', 'training_set'
    
    # The MLE just needs to view the training set, and we can store the pid as part of last column header
    # Then, as long as the MLE keeps the same column header format for their solution, we can retrieve the pid and compare with the test set

    # Filter out the test set, so make a new display dict which contains the training_set data and pair_id as part of last column header
    for doc in documents_arr:
        display_dict = {
            'training_set_data': doc['training_set']['training_set_data'],
            'training_set_metadata': doc['training_set']['training_set_metadata'],
            'pid': doc['pair_id'],
            }
        
        # Add pid as string to the last column of csv file
        fields_arr = list(display_dict['training_set_data'][0].keys())
        fields_arr[-1] = f"{fields_arr[-1]}#{display_dict['pid']}" 
        # last column header gets written as string, but others dont in csv file, this is ok though because all headers will be get read as strings later

        # Now, take the display_dict new version and write it to a csv file, which will then get sent to html
        
        csv_file_name = display_dict['training_set_metadata']['TS Name']
        csv_file_name = f"{csv_file_name}.csv"
        csv_file_path = f"training_sets_for_MLE/{csv_file_name}"

        with open(csv_file_path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields_arr)
            for dict_row in display_dict['training_set_data']:
                vals_arr = dict_row.values()
                writer.writerow(vals_arr)

        csvfile.close()

    return render_template('MLE_view_data.html', files=os.listdir('training_sets_for_MLE'))

@app.route('/MLE_view_data/<filename>')
def download(filename):
    return send_from_directory('training_sets_for_MLE', filename)


@app.route('/MLE_upload', methods=['GET', 'POST'])
def MLE_upload():
    if request.method == 'POST':
        # get the uploaded file
        MLE_solution = request.files['solution_file']

        # get the file extension, assuming user inputs data correctly so the file_ext will be the same for both uploaded files
        file_ext = os.path.splitext(MLE_solution.filename)[1]
        # save the file to a directory

        # Call fxn to get dataframe for training data and test data
        sol_df = None
        sol_df = file_to_df(MLE_solution, file_ext)

        # Have the solution dataframe, the solution is expected to have the correct format based on the training data set, 
        # so the solution dataframe will have a pid that can access, then we will use this pid to compare it with the test set
        # (for testing, solution will be test set with noise added)

        # Get TS Metadata values from POSTed variables
        # Solution Variables

        solution_title = request.form['sol_title']

        solution_metadata = { # Need to think about what other metadata a MLE would need to add for their uploaded solution
            'MLE_solution_title': solution_title
        }
        
        if(sol_df is not None):
            # Need to access the pair id from the pandas dataframe, it will be the last element
            last_col = sol_df.columns[-1]

            col_split_lst = last_col.split('#') # list has two elems, the header itself, and then the pid
            last_col_header = col_split_lst[0]
            pid = col_split_lst[1]

            last_col = last_col_header # get rid of the pid from the header now that we have it stored as a variable
            # Now, send the dataframe and the pid to our function that stores solution in database

            sol_res = sol_to_DB(sol_df, solution_metadata, pid, solution_title, db)
            if(sol_res is True):
                flash('MLE Solution Was Submitted To Database', 'info')
            else:
                flash('Send functions did not return True, error sending MLE solution to Database', 'info')
        else:
            flash('Unsupported file type', 'info')

        return redirect(url_for("MLE_upload"))
    else:
        return render_template('MLE_upload.html')
    


PORT=5000
DEBUG=True

if __name__ == "__main__":
    app.run(port=PORT, host="0.0.0.0", debug=DEBUG)