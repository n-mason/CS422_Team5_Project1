#CS 422 P1 README
#Author: Nathaniel Mason
#Group Name: Team 5

##Brief System Description:
These files are for Team 5's system: Forecasting Time Series Library, or "FTL". The system is designed for two types of users, MLEs (Machine Learning Engineers) and Contributors. Contributors can upload pairs of files (training set and test set), and MLEs can download these files, perform some forecasting with Machine Learning, then upload their solution and see how their results compare two other solutions uploaded by other MLEs.

##Authors:
Julian Albert, Nathaniel Mason, Hannah Sagalyn, Carlos Villarreal-Elizondo

##File creation date:
April 25, 2023

##Course Name and Assignment:
CS 422/522 Software Method 1 - Project 1: Time Series Forecasting And Benchmarks

##Necessary Steps:
The system is hosted on heroku and can be found at the following link: https://cs422-team5-project1.herokuapp.com/

###Additional instructions for testing the system:
###In order to test the system, a folder called test_files has been created on the repo containing a training set file, test set file (for testing the contributor upload page), and an MLE solution test file as well (for testing the MLE upload page)
###The database used is a NoSQL google cloud firestore database, access has been given to jflore10@uoregon.edu and ksharma2@uoregon.edu. In case it is needed, the database has also been shared with mahasanis@uoregon.edu

##Along with the test_files directory, this github repo also contains a "static" directory and "templates" directory. These directories are used by Flask to render the various HTML pages. The static directory contains files that do not change, like images and css styling files. The templates directory contains the html files which define the various pages of the system.