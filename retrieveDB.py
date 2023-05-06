"""
Python file to retrieve documents from Cloud Firestore Database based on the collection name,
and in the last two functions based on the pid, which is the pair id associated with a file pair (a training set and a test set that was uploaded by a contributor)

Authors: Nathaniel Mason
Group Name: Team 5

Creation date and modifications info found on GitHub
"""

import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd # pandas makes data analysis/manipulation easy
# Pandas has a read_csv function that reads column names based on CSV header and then chunks file

# Edit code so that have a function that takes in a Panda dataframe and then submits into the DB
# will consider pandas dataframe as df in function

def retrieve_DB(db): 
    # function retrieves all documents for our time series data
    # Add each metadata to its respective file, then store the pair of files as one document in cloud firestore
    # Then, later on when an MLE uploads a solution for a particular pair_id, we can store that as a solution in the solutions nested document
    trng_arr = []
    
    if(db):
        docs = db.collection('time_series_data').get()

        for doc in docs:
            trng_arr.append(doc.to_dict())
        
    return trng_arr 


def retrieve_test_set_DB(db, pair_id: str): 
    # function retrieves the corresponding test set (a firestore document) given a pid (the pair id for the original training set and test set)
    # the MLE already downloaded the training set, did their forecasting, and uploaded so now we need the original test set associated with the pid
    doc_test_set = None

    if(db):
        doc_test_set = db.collection("time_series_data").where("pair_id", "==", pair_id).get()

    
    return doc_test_set

def retrieve_MLE_sols(db, pair_id: str): 
    # function retrieves the corresponding test set (a firestore document) given a pid (the pair id for the original training set and test set)
    # the MLE already downloaded the training set, did their forecasting, and uploaded so now we need the original test set associated with the pid
    doc_list = None

    if(db):
        doc_list = db.collection("MLE_solutions").where("solution_pair_id", "==", pair_id).get()


    return doc_list