import sys
import math
import csv
#from flask_Proj1 import file_to_df
import pandas as pd
import numpy as np
import matplotlib.pyplot as plp

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
    #array = np.delete(array,0,1)
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
    error = [0]*len(forecastResult[0])
    length = len(forecastResult[0])
    if length != len(testSet[0]):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            error[j] += abs((testSet[i][j]-forecastResult[i][j])/testSet[i][j])
            j += 1
    for j in range(len(error)):
        error[j] *= 100/len(forecastResult)
    return error

def symmetric_mean_absolute_percentage_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Symmetric_mean_absolute_percentage_error
    error = [0] * len(forecastResult[0])
    length = len(forecastResult[0])
    if length != len(testSet[0]):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            change = abs(forecastResult[i][j]-testSet[i][j])
            change /= (abs(testSet[i][j]) + abs(forecastResult[i][j]))/2
            error[j] += change
            j += 1
    for j in range(len(error)):
        error[j] *= 100/len(forecastResult)
    return error

def mean_squared_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_squared_error
    error = [0] * len(forecastResult[0])
    length = len(forecastResult[0])
    if length != len(testSet[0]):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            error[j] += ((testSet[i][j]-forecastResult[i][j])**2)
            j += 1
    for j in range(len(error)):
        error[j] /= len(forecastResult)
    return error

def root_mean_squared_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Root-mean-square_deviation
    error = mean_squared_error(forecastResult,testSet)
    for i in range(len(error)):
        error[i] = math.sqrt(error[i])
    return error

def correlation_coefficient(forecastResult, testSet): #formula taken from https://www.youtube.com/watch?v=11c9cs6WpJU
    length = len(forecastResult[0])
    size = len(forecastResult)
    if length != len(testSet[0]):
        sys.exit("Error: incompatible array sizes")  # if the array sizes don't match, causes an error
    sumForecast, sumTest, sumBoth, forecastSquared, testSquared = [0] * len(forecastResult[0]), [0] * len(forecastResult[0]), [0] * len(forecastResult[0]), [0] * len(forecastResult[0]), [0] * len(forecastResult[0])
    for i in range(size):
        j = 0
        while j < length:
            sumForecast[j] += forecastResult[i][j]
            sumTest[j] += testSet[i][j]
            sumBoth[j] += forecastResult[i][j] * testSet[i][j]
            forecastSquared[j] += forecastResult[i][j]**2
            testSquared[j] += testSet[i][j]**2
            j += 1
    error = [0] * len(forecastResult[0])
    for j in range(len(error)):
        numerator = (size*sumBoth[j])-(sumForecast[j]*sumTest[j])
        denominator = math.sqrt(((size*forecastSquared[j]) - (sumForecast[j]**2))*((size*testSquared[j]) - (sumTest[j]**2)))
        error[j] = numerator/denominator
    return error

def error_arr_to_plot(error_array,title):
    x_axis = [0]*len(error_array)
    for i in range(len(error_array)):
        x_axis[i] = i
    plp.title(title)
    plp.xlabel("columns")
    plp.ylabel("error values")
    plp.plot(x_axis,error_array,color='red')
    plp.show()
    return 0

def the_big_one(forecastResult,testSet):
    meanError = mean_absolute_percentage_error(forecastResult,testSet)
    symmetricMeanError = symmetric_mean_absolute_percentage_error(forecastResult,testSet)
    rootError = root_mean_squared_error(forecastResult,testSet)
    correlationCoefficient = correlation_coefficient(forecastResult,testSet)







def main():
    with open('GOOG_MLE_upload.csv','r') as file:
        forecast = csv_to_arr(file)
        #print(forecast)
    with open('GOOG_test_set.csv','r') as file2:
        test = csv_to_arr(file2)
        #print(test)
    error_arr_to_plot(correlation_coefficient(forecast,test),"correlation coefficient")


    '''
    dataframe = file_to_df(GOOG_MLE_upload.csv,'.csv')
    dataframe2 = file_to_df(GOOG_test_set.csv, '.csv')
    #forecast = dataframe_to_array(dataframe)
    #observed = dataframe_to_array(dataframe2)
    #mean_absolute_percentage_error(forecast,observed)
    '''

main()


