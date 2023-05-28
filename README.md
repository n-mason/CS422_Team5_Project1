# CS 422 P1 README
# Author: Nathaniel Mason
# Group Name: Team 5

## Brief System Description:
These files are for Team 5's system: Forecasting Time Series Library, or "FTL". The system is designed for two types of users, MLEs (Machine Learning Engineers) and Contributors. Contributors can upload pairs of files (training set and test set), and MLEs can download these files, perform some forecasting with Machine Learning, then upload their solution and see how their results compare to other solutions uploaded by other MLEs.

## Authors:
Julian Albert, Nathaniel Mason, Hannah Sagalyn, Carlos Villarreal-Elizondo

## File creation date:
April 25, 2023

## Course Name and Assignment:
CS 422/522 Software Method 1 - Project 1: Time Series Forecasting And Benchmarks

## Necessary Steps:
The system used to be hosted on heroku but was taken down. The app can still be tested/viewed by using the following docker commands...
## To start the application, the user should use the following docker commands:
* "docker compose up"
* "docker images" can be used to view running images, and "docker ps" can be used to view running containers
* Now that the container is running, go to "localhost:5001" to view the home page and navigate from there
## To stop the application, the user should use the following docker commands:
* "docker compose down --rmi all" to stop and remove all containers and images built by docker compose

### Additional instructions for testing the system:
#### In order to test the system, a folder called test_files has been created on the repo containing a training set file, test set file (for testing the contributor upload page), and an MLE solution test file as well (for testing the MLE upload page). On the MLE download page of the web app, files which are the training sets can be clicked and this will download a file that an MLE could use to do their forecasting. The key piece is that the headers of this file should not be changed, because an id is added to the last header of the training set, and as long as the headers of the MLE solution file remain the same, once the MLE solution file is uploaded, this id can be used to retrieve the appropriate test set file and perform error calculations to determine the accuracy of the MLE solution.

#### The database used is a NoSQL google cloud firestore database, access has been given to jflore10@uoregon.edu and ksharma2@uoregon.edu. In case it is needed, the database has also been shared with mahasanis@uoregon.edu
#### To view the database, you should be able to click the invite link that was sent to your email. There should be a button that says "Open Firebase Console" and this will take you to the firebase website on your browser, where you can then view the data in the firestore database by clicking "Firestore Database" on the left (under Project Overview). 
#### Alternatively, here is a link directly to the Google Firestore Database overview page: https://console.firebase.google.com/u/0/project/cs-422-project-1/overview

## Along with the test_files directory, this github repo also contains a "static" directory and "templates" directory. These directories are used by Flask to render the various HTML pages. The static directory contains files that do not change, like images and css styling files. The templates directory contains the html files which define the various pages of the system.
