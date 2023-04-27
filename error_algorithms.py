import sys
import math
import csv
from flask_Proj1 import file_to_df
import pandas as pd
import numpy as np

#TODO: update all functions to work with 2D arrays
#TODO: update both array functions to look for date column and cull it

def csv_to_arr(file):
    csvreader = csv.reader(file)
    rows = list(csvreader)
    rowCount = len(rows)
    colCount = len(rows[0])
    data = [[0 for i in range(colCount-1)] for j in range(rowCount-1)]
    i,j = 0,0
    while i < rowCount-1:
        while j < colCount-1:
            data[i][j] = float(rows[i+1][j+1])
            j+=1
        j = 0
        i+=1
    return data

def dataframe_to_array(dataframe):
    array = dataframe.to_numpy()
    array = np.delete(array,0,1)
    return array

def mean_absolute_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_absolute_error
    error = [0]*len(forecastResult[0])
    length = len(forecastResult[0])
    if length != len(testSet[0]):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            error[j] += abs(forecastResult[i][j]-testSet[i][j])
            j += 1
    for j in range(len(error)):
        error[j] /= len(forecastResult)
    #print("Mean Absolute Error is " + str(error)) #prints results with final calculations
    return error

def mean_absolute_percentage_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_absolute_percentage_error
    error = 0
    length = len(forecastResult)
    if length != len(testSet):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error
    i = 0
    while i < length: #while loop with the sigma formula
        error += abs((testSet[i]-forecastResult[i])/testSet[i])
        i += 1
    return round(((100*error)/length),2)

def symmetric_mean_absolute_percentage_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Symmetric_mean_absolute_percentage_error
    error = 0
    length = len(forecastResult)
    if length != len(testSet):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error
    i = 0
    while i < length: #while loop with the sigma formula
        change = abs(forecastResult[i]-testSet[i])
        change /= (abs(testSet[i]) + abs(forecastResult[i]))/2
        error += change
        i += 1
    return round(((100*error)/length),2)

def mean_squared_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_squared_error
    error = 0
    length = len(forecastResult)
    if length != len(testSet):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error
    i = 0
    while i < length: #while loop with the sigma formula
        error += ((testSet[i]-forecastResult[i])**2)
        i += 1
    return round((error/length),2)

def root_mean_squared_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Root-mean-square_deviation
    error = 0
    length = len(forecastResult)
    if length != len(testSet):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error
    i = 0
    while i < length: #while loop with the sigma formula
        error += ((testSet[i]-forecastResult[i])**2)
        i += 1
    return round(math.sqrt(error / length), 2)

def correlation_coefficient(forecastResults, testSet): #formula taken from https://www.youtube.com/watch?v=11c9cs6WpJU
    length = len(forecastResults)
    if length != len(testSet):
        sys.exit("Error: incompatible array sizes")  # if the array sizes don't match, causes an error
    i, sumForecast, sumTest, sumBoth, forecastSquared, testSquared = 0,0,0,0,0,0
    while i < length:
        sumForecast += forecastResults[i]
        sumTest += testSet[i]
        sumBoth += forecastResults[i] * testSet[i]
        forecastSquared += forecastResults[i]**2
        testSquared += testSet[i]**2
        i += 1
    numerator = (length*sumBoth)-(sumForecast*sumTest)
    denominator = math.sqrt(((length*forecastSquared) - (sumForecast**2))*((length*testSquared) - (sumTest**2)))
    return round((numerator/denominator), 4)

def error_arr_to_plot(error_array):
    #TODO: implement
    return





def main():
    with open('GOOG_MLE_upload.csv','r') as file:
        forecast = csv_to_arr(file)
        #print(forecast)
    with open('GOOG_test_set.csv','r') as file2:
        test = csv_to_arr(file2)
        #print(test)
    mean_absolute_error(forecast,test)

    dataframe = file_to_df('GOOG_MLE_upload.csv','.csv')
    dataframe2 = file_to_df('GOOG_test_set.csv', '.csv')
    forecast = dataframe_to_array(dataframe)
    observed = dataframe_to_array(dataframe2)
    mean_absolute_error(forecast,observed)

main()


