import sys
import math
import csv
#from flask_Proj1 import file_to_df
import pandas as pd
import numpy as np
import matplotlib.pyplot as plp

#TODO: update both array functions to look for date column and cull it

def column_search(arr,parameter):
    arr_len = len(arr)
    col = -1
    for n in range(arr_len):
        if arr[n] == parameter:
            col = n
    return col


def csv_to_arr(file,parameter=''):
    csvreader = csv.reader(file)
    rows = list(csvreader)
    rowCount = len(rows)
    colCount = len(rows[0])
    if parameter != '':
        col = column_search(rows[0],parameter)
        if col == -1:
            parameter = ''
            print("parameter not found\nreturning whole array")
        else:
            data = [[0] for x in range(rowCount-1)]
            i = 0
            while i < rowCount-1:
                data[i][0] = float(rows[i+1][col])
                i += 1
            return data


    if parameter == '':
        col = column_search(rows[0],'Date')
        data = [[0 for y in range(colCount-1)] for x in range(rowCount-1)]
        i,j,k = 0,0,0
        while i < rowCount-1:
            while k < colCount-1:
                if j == col:
                    j+=1
                else:
                    data[i][k] = float(rows[i+1][j])
                    j+=1
                    k+=1
            j = 0
            k = 0
            i+=1
        return data

def dataframe_to_array(dataframe):
    array = dataframe.to_numpy()
    #array = np.delete(array,0,1)
    return array

def sys_exit(forecastResult,testSet):
    if len(forecastResult[0]) != len(testSet[0]):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error

def mean_absolute_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_absolute_error
    error = [0]*len(forecastResult[0])
    length = len(forecastResult[0])
    sys_exit(forecastResult,testSet)
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            error[j] += abs(forecastResult[i][j]-testSet[i][j])
            j += 1
    val = 0
    for j in range(len(forecastResult[0])):
        error[j] /= len(forecastResult)
        val += error[j]
    val /= length
    return val

def mean_absolute_percentage_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_absolute_percentage_error
    error = [0]*len(forecastResult[0])
    length = len(forecastResult[0])
    sys_exit(forecastResult,testSet)
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            error[j] += abs((testSet[i][j]-forecastResult[i][j])/testSet[i][j])
            j += 1
    val = 0
    for j in range(len(forecastResult[0])):
        error[j] *= 100/len(forecastResult)
        val += error[j]
    val /= length
    return val

def symmetric_mean_absolute_percentage_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Symmetric_mean_absolute_percentage_error
    error = [0] * len(forecastResult[0])
    length = len(forecastResult[0])
    sys_exit(forecastResult,testSet)
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            change = abs(forecastResult[i][j]-testSet[i][j])
            change /= (abs(testSet[i][j]) + abs(forecastResult[i][j]))/2
            error[j] += change
            j += 1
    val = 0
    for j in range(len(forecastResult[0])):
        error[j] *= 100/len(forecastResult)
        val += error[j]
    val /= length
    return val

def mean_squared_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_squared_error
    error = [0] * len(forecastResult[0])
    length = len(forecastResult[0])
    sys_exit(forecastResult,testSet)
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            error[j] += (((testSet[i][j] - forecastResult[i][j])/testSet[i][j])**2)
            j += 1
    val = 0
    for j in range(len(forecastResult[0])):
        error[j] *= 100/len(forecastResult)
        val += error[j]
    val /= length
    return val

def root_mean_squared_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Root-mean-square_deviation
    error = [0] * len(forecastResult[0])
    length = len(forecastResult[0])
    sys_exit(forecastResult,testSet)
    for i in range(len(forecastResult)):
        j = 0
        while j < length:  # while loop with the sigma formula
            error[j] += (((testSet[i][j] - forecastResult[i][j])/testSet[i][j]) ** 2)
            j += 1
    val = 0
    for j in range(len(forecastResult[0])):
        error[j] *= 100/len(forecastResult)
        error[j] = math.sqrt(error[j])
        val += error[j]
    val /= length
    return val

def correlation_coefficient(forecastResult, testSet): #formula taken from https://www.youtube.com/watch?v=11c9cs6WpJU
    length = len(forecastResult[0])
    size = len(forecastResult)
    sys_exit(forecastResult,testSet)
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
    val = 0
    for j in range(len(forecastResult[0])):
        numerator = (size*sumBoth[j])-(sumForecast[j]*sumTest[j])
        denominator = math.sqrt(((size*forecastSquared[j]) - (sumForecast[j]**2))*((size*testSquared[j]) - (sumTest[j]**2)))
        val += numerator/denominator
    val /= length
    return val

def error_calculation(forecastResult, testSet):
    error = [[0 for i in range(5)] for j in range(2)]
    error[0][0] = mean_absolute_percentage_error(forecastResult,testSet)
    error[1][0] = 1
    error[0][1] = symmetric_mean_absolute_percentage_error(forecastResult,testSet)
    error[1][1] = 2
    error[0][2] = mean_squared_error(forecastResult,testSet)
    error[1][2] = 3
    error[0][3] = root_mean_squared_error(forecastResult,testSet)
    error[1][3] = 4
    error[0][4] = correlation_coefficient(forecastResult,testSet)
    error[1][4] = 5
    return error

def double_bubble(array):
    n = len(array[0])
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[0][j] > array[0][j + 1]:
                array[0][j], array[0][j + 1] = array[0][j + 1], array[0][j]
                array[1][j], array[1][j + 1] = array[1][j + 1], array[1][j]
    return array

def int_to_alg(numArr):
    nameArr = ["" for x in range(5)]
    for i in range(len(numArr)):
        if numArr[i] == 1:
            nameArr[i] = "MAPE"
        if numArr[i] == 2:
            nameArr[i] = "SMAPE"
        if numArr[i] == 3:
            nameArr[i] = "MSE"
        if numArr[i] == 4:
            nameArr[i] = "RMSE"
        if numArr[i] == 5:
            nameArr[i] = "r-Value"
    return nameArr

def error_arr_to_plot(error_array):
    x_axis = [0]*len(error_array[0])
    for i in range(len(error_array[0])):
        x_axis[i] = error_array[1][i]
    x_axis = int_to_alg(x_axis)
    plp.title("Percent Error Difference")
    plp.xlabel("Algorithm")
    plp.ylabel("Percentage Error")
    plp.bar(x_axis,error_array[0])
    plp.show()
    return 0

def get_error_graph(forecastResult,testSet):
    error = error_calculation(forecastResult,testSet)
    error = double_bubble(error)
    error_arr_to_plot(error)







def main():
    with open('GOOG_MLE_upload.csv','r') as file:
        forecast = csv_to_arr(file,'Open')
    with open('GOOG_test_set.csv','r') as file2:
        test = csv_to_arr(file2,'Open')

    get_error_graph(forecast,test)


    '''
    dataframe = file_to_df(GOOG_MLE_upload.csv,'.csv')
    dataframe2 = file_to_df(GOOG_test_set.csv, '.csv')
    #forecast = dataframe_to_array(dataframe)
    #observed = dataframe_to_array(dataframe2)
    #mean_absolute_percentage_error(forecast,observed)
    '''

main()


