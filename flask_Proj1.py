"""
Main python file for routing pages using Flask, parsing data and storing/pulling data from Firestore.
When data gets parsed, it gets converted to pandas dataframes which are used for the firestore storing functions.
The error calculations code also takes in pandas dataframes. 

Authors: Julian Albert, Nathaniel Mason
Group Name: Team 5

Creation date and modifications info found on GitHub

"""


import os
import pandas as pd
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, jsonify, session
from sendDB import pair_to_DB, sol_to_DB
from retrieveDB import retrieve_DB, retrieve_test_set_DB, retrieve_MLE_sols
from werkzeug.datastructures import FileStorage # FileStorage used to represent uploaded files
import uuid # for generating unique id
import firebase_admin
from firebase_admin import credentials, firestore
import csv
import json
from error_algorithms import get_error_algorithm
import base64
import shutil


app = Flask(__name__)
app.secret_key = "my_flask_secret_123_321"

# Start firestore client
DB_key_json_str = os.environ.get("DB_KEY") # this is a JSON string stored as an environment variable
#print(DB_key_json_str)


if(DB_key_json_str is not None):
    DB_key_dict = json.loads(DB_key_json_str)
    #print(DB_key_dict)

    cred = credentials.Certificate(DB_key_dict)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    print("DB Key not found, can't start firebase client")
    exit()

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


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/login', methods=['GET'])
@app.route('/home', methods=['GET'])
def login():
    return render_template('login_mod.html') 
  

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
        tr_dom = request.form['tr_domains']
        tr_uns = request.form['tr_unis']
        tr_univmult = request.form['tr_univmult']
        tr_vecsiz = request.form['tr_vecsiz']
        tr_len = request.form['tr_len']
        tr_samp = request.form['tr_samp']

        # Test Set Variables
        tst_TS_Name = request.form['tst_TS_name']
        tst_desc = request.form['task_description']
        tst_dom = request.form['tst_domains']
        tst_uns = request.form['tst_units']
        tst_univmult = request.form['tst_univmult']
        tst_vecsiz = request.form['tst_vecsiz']
        tst_len = request.form['tst_len']
        tst_samp = request.form['tst_samp']

        tr_task_desc = tst_desc # Forecasting task will be the same for the pair of files
        target_vars = request.form['target_vars'] # The column names that the MLE needs to worry about, like 'Close' for example in the GOOG stock file


        # Get info dict with metadata
        trng_metdat  = {
            "TS Name": tr_TS_Name, # Name of the file
            "Domain(s)": tr_dom, # Domain of the file
            "Units": tr_uns, # Units of the file, for a stock case would be USD, Days (unit for YYYY-MM-DD) and Number of shares (Volume)
            "Univariate/Multivariate": tr_univmult,
            "Vector Size": tr_vecsiz, # number of vars at each time point
            "Length": tr_len, 
            "Sampling Period": tr_samp,
            "Task Description": tr_task_desc, # Task Description for file
            "Target Variables": target_vars # The variables that need to be forecasted
        }

        tst_metdat  = {
            "TS Name": tst_TS_Name, # Name of the file
            "Domain(s)": tst_dom, # Domain of the file
            "Units": tst_uns, # Units of the file, for a stock case would be USD, Days (unit for YYYY-MM-DD) and Number of shares (Volume)
            "Univariate/Multivariate": tst_univmult,
            "Vector Size": tst_vecsiz, # number of vars at each time point
            "Length": tst_len, 
            "Sampling Period": tst_samp,
            "Task Description": tst_desc, # Task Description for file
            "Target Variables": target_vars # The variables that need to be forecasted
        }
        
        if((trng_df is not None) and (tst_df is not None)):
            # Give the pair a unique id, then send each dataframe to the DB along with that id
            uniq_id = uuid.uuid4()
            pair_id = str(uniq_id) # id will be stored as a tag with type string

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
    


@app.route('/MLE_view_data', methods=['GET', 'POST'])
def MLE_view_data():
    # MLE will go to this page and view the training sets that are saved in the database (each training set needs a unique id, so that it can be linked with the test set with the same pair id)
    documents_arr = retrieve_DB(db) # each Firestore document has the keys 'pair_id', 'test_set', 'training_set'
    
    # The MLE just needs to view the training set, and we can store the pid as part of last column header
    # Then, as long as the MLE keeps the same column header format for their solution, we can retrieve the pid and compare with the test set

    # Create metadata array for the MLE view page
    file_names = []
    display_dicts = []

    # Filter out the test set, so make a new display dict which contains the training_set data and pair_id as part of last column header
    for doc in documents_arr:
        display_dict = {
            'training_set_data': doc['training_set']['training_set_data'],
            'training_set_metadata': doc['training_set']['training_set_metadata'],
            'test_set_metadata': doc['test_set']['test_set_metadata'],
            'pid': doc['pair_id'],
            }
        
        # Add pid as string to the last column of csv file
        fields_arr = list(display_dict['training_set_data'][0].keys())
        fields_arr[-1] = f"{fields_arr[-1]}#{display_dict['pid']}" 
        # last column header gets written as string, but others dont in csv file, this is ok though because all headers will be get read as strings later

        # Now, take the display_dict new version and write it to a csv file, which will then get sent to html
        
        csv_file_name = display_dict['training_set_metadata']['TS Name']
        csv_file_name = f"{csv_file_name}.csv" 

        if(os.path.exists("training_sets_for_MLE") == False): # Need to create the directory if it does not exist
            os.mkdir("training_sets_for_MLE")

        csv_file_path = f"training_sets_for_MLE/{csv_file_name}" 

        file_names.append(csv_file_name)
        display_dicts.append(display_dict)

        with open(csv_file_path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(fields_arr)
            for dict_row in display_dict['training_set_data']:
                vals_arr = dict_row.values()
                writer.writerow(vals_arr)

        # Have the csvfile with the correct name, it is saved in training_sets_for_MLE
        # Need to also pass the metadata for each file to html, then can list that next to the file
        # for each file, use display_dict and store in array

    return render_template('MLE_view_data.html', files_and_dicts = zip(file_names, display_dicts))

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
        name_for_MLE = request.form['MLE_name']

        solution_metadata = {
            'MLE Name': name_for_MLE
        }

        # Give the MLE a unique id, then send the data to DB and name the document the id
        MLE_uniq_id = uuid.uuid4()
        id_MLE = str(MLE_uniq_id)
        
        if(sol_df is not None):
            # Need to access the pair id from the pandas dataframe, it will be the last element
            df_cols = sol_df.columns.tolist()
            last_col = df_cols[-1]
            col_lst = last_col.split('#') # list has two elems, the header itself, and then the pid
            last_col_header = col_lst[0]
            pid = col_lst[1]
            df_cols[-1] = last_col_header
            sol_df.columns = df_cols

            ts_firestore_doc = retrieve_test_set_DB(db, str(pid)) 
            ts_doc_snapshot = ts_firestore_doc[0]
            ts_dict = ts_doc_snapshot.to_dict() # this time series dictionary has pair_id, test_set and training_set
 
            test_set_data = ts_dict['test_set']['test_set_data'] 
            target_vars_str = ts_dict['training_set']['training_set_metadata']['Target Variables'] #this is a string,
            # target vars in string are separated by commas
            target_vars_arr = target_vars_str.split(',')

            """test_doc_dict has the structure:
            'test_set_data': [{},{},{},{}...] # Array of dicts, each dict contains csv col values, for ex 'Close': 102, 'High': 103, etc
            'test_set_metadata': {} # Dictionary with metadata like 'Description', 'Domain(s)', 'TS Name', etc
            """

            test_set_data_df = pd.DataFrame(test_set_data) # the keys of the dicts in test_set_data will become the columns in the pd dataframe
            # the error functions should take in the MLE solution and the test set (both dataframes) and return dict + error graph

            error_dict_result = get_error_algorithm(sol_df, test_set_data_df, target_vars_arr)
            error_parameters_arr = error_dict_result['parameter']
            error_test_results = error_dict_result['dict']
            error_graph_encoded_png = error_dict_result['graph'] #base64 encoded
            
            if(os.path.exists("graph_folder")):
                shutil.rmtree("graph_folder") # delete the old folder, just need folder temporarily for the one MLE graph
            os.mkdir("graph_folder")

            graph_file_path = "graph_folder/graph_MLE.png" 
            graph_filename = "graph_MLE.png"

            with open(graph_file_path, "wb") as fs:
                fs.write(base64.b64decode(error_graph_encoded_png))
            
            session['pid'] = pid
            
            # In the DB, MLE_solutions documents will be split by MLE name (if have time, look into generating id per MLE solution and using that as the document name in the DB)
            sol_res = sol_to_DB(sol_df, solution_metadata, error_test_results, pid, id_MLE, db)
            if(sol_res is True):
                flash('MLE Solution Was Submitted To Database', 'info')
                return redirect(url_for("solution_for_MLE"))
            else:
                flash('Send functions did not return True, error sending MLE solution to Database', 'info')
                return redirect(url_for("MLE_upload"))
        else:
            flash('Unsupported file type', 'info')
            return redirect(url_for("MLE_upload"))
    else:
        return render_template('MLE_upload.html')

def training_set_table_data(target_vars: str, pid: str): 
    table_rows_data = []
    sols_docsnapshot_list = retrieve_MLE_sols(db, pid)
    #flash(pid)

    for sol_doc in sols_docsnapshot_list:
        sol_doc_dict = sol_doc.to_dict() 
        sol_name_MLE = sol_doc_dict['MLE_solution_metadata']['MLE Name']
        sol_doc_errors = sol_doc_dict['error_results']
        sol_error_results_list = list(sol_doc_errors.values())
        sol_error_results_list.reverse()
        sol_error_results_list.insert(0, sol_name_MLE)
        sol_error_results_list.insert(1, target_vars)
        table_rows_data.append(sol_error_results_list)
    
    return table_rows_data

@app.route('/solution_for_MLE', methods=['GET', 'POST'])
def solution_for_MLE():
    sesh_pid = session['pid']
    #flash(sesh_pid)
    ts_firestore_doc = retrieve_test_set_DB(db, str(sesh_pid)) 
    ts_doc_snapshot = ts_firestore_doc[0]
    ts_dict = ts_doc_snapshot.to_dict() # this time series dictionary (from time_series_data Collection) 
    #has pair_id, test_set and training_set
    training_set_doc = ts_dict['training_set']
    training_set_name = training_set_doc['training_set_metadata']['TS Name']
    tr_target_vars = training_set_doc['training_set_metadata']['Target Variables']

    tab_rows_data = training_set_table_data(tr_target_vars, sesh_pid)

    return render_template('comparison_graph_MLE.html', table_rows_data=tab_rows_data, training_set_name = training_set_name) 

@app.route('/graph_download', methods=['GET', 'POST'])
def graph_download():
    if(os.path.exists("graph_folder")):
        filename = "graph_MLE.png"
        return send_from_directory("graph_folder", filename)
    else:
        return None

@app.route('/all_solutions', methods=['GET', 'POST'])
def all_solutions():
    # Need code to pull error data from DB and then create tables and send to html so that JS Datatable can style it
    # need to pull all training set docs, so that each one will have its unique pid, then we go through
    # our trainiign set array, for each pid get all MLE sols for that pid and then do table code
    time_series_data_docs = retrieve_DB(db)

    training_sets = []

    trng_tables = []
    trng_table_names = []

    for ts_doc in time_series_data_docs:
        doc_pid = ts_doc['pair_id']
        training_set_name = ts_doc['training_set']['training_set_metadata']['TS Name']
        target_vars = ts_doc['training_set']['training_set_metadata']['Target Variables']
        trng_tbl_info = {}
        trng_tbl_info['tr_name'] = training_set_name
        trng_tbl_info['target_vars'] = target_vars
        trng_tbl_info['pid'] = doc_pid

        training_sets.append(trng_tbl_info)

    
    for tr_dict in training_sets:
        trng_pid = tr_dict['pid']
        trng_target_vars = tr_dict['target_vars']
        trng_name = tr_dict['tr_name']
        trng_rows_data = training_set_table_data(trng_target_vars, trng_pid)
        trng_tables.append(trng_rows_data)
        trng_table_names.append(trng_name)


    return render_template('all_analyses.html', rows_and_names = zip(trng_tables, trng_table_names))



PORT=int(os.environ.get("PORT", 5000)) # returns the value if the key is present, otherwise the second argument, port 5000 is used
DEBUG=True

if __name__ == "__main__":
    app.run(port=PORT, host="0.0.0.0", debug=DEBUG)