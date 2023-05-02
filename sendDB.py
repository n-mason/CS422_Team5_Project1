"""
Script to take file sent from upload python script and send to Cloud Firestore Database
"""

import firebase_admin
from firebase_admin import credentials, firestore
import time, os
from datetime import datetime
import pandas as pd # pandas makes data analysis/manipulation easy
# Pandas has a read_csv function that reads column names based on CSV header and then chunks file

# Edit code so that have a function that takes in a Panda dataframe and then submits into the DB
# will consider pandas dataframe as df in function

def pair_to_DB(training_df, training_metadata: dict, tst_df, test_metadata: dict, pid: str, doc_name: str, task_description: str, db): 
    # function takes in the training set and test set pandas dataframes, the info_dict dictionary for each file, the pair id (a string), and task description
    # Add each metadata to its respective file, then store the pair of files as one document in cloud firestore
    # Then, later on when an MLE uploads a solution for a particular pair_id, we can store that as a solution in the solutions nested document
    
    if(db):
        outer_doc_ref = db.collection('time_series_data').document(doc_name)

        # define two nested documents: training set document and test set document, these will go in the overall document that contains the pair id
        # define data as a dictionary, so convert from pandas df to a dictionary
        training_data_dict = training_df.to_dict(orient='records') # records means dict is list like, [{col: val},{col: val}, etc.]
        test_data_dict = tst_df.to_dict(orient='records') 

        # training set document will contain all rows of data and its metadata
        training_set_document = {
            'training_set_metadata': training_metadata,
            
            'training_set_data': training_data_dict
        }

        test_set_document = {
            'test_set_metadata': test_metadata,
            'test_set_data': test_data_dict
        }


        # add these dicts, which are the nested documents to the main outer doc
        pair_dict = {
            'pair_id': pid,
            'task_desc': task_description, # new field for the text entered by the contributor
            'training_set': training_set_document,
            'test_set': test_set_document
        }

        try:
            outer_doc_ref.set(pair_dict) 
        except Exception as e:
            return e

        # define metadata dictionary
        """TS Metadata required from PDF: TS Name, Description, Domain(s), Units, Keywords, 
        Scalar/Vector(univariate/multivariate), Vector size, Length, Sampling Period"""

    return True     


def sol_to_DB(sol_df, sol_metadata: dict, pid: str, doc_name: str, db):
    if(db):
        doc_ref = db.collection('MLE_solutions').document(doc_name)

        # MLE solution document needs pair id (pid), sol metadata, and the sol data

        # define data as a dictionary, so convert from pandas df to a dictionary
        sol_data_dict = sol_df.to_dict(orient='records')  
        
        # retrieve the task description from the Firestore document corresponding to the file
        doc = db.collection('time_series_data').document(doc_name).get()
        task_description = doc.get('task_description')

        # training set document will contain all rows of data and its metadata
        sol_document = {
            'MLE_solution_metadata': sol_metadata,
            'MLE_solution_data': sol_data_dict,
            'solution_pair_id': pid,
            'task_description': task_description # new field for the text entered by the contributor
        }

        try:
            doc_ref.set(sol_document) 
        except Exception as e:
            return e

    return True 
