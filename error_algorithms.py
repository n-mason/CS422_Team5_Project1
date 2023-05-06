"""
Python file for MLE solution error calculations and graph generation. Results are returned in a dictionary

Authors: Carlos Villarreal-Elizondo
Group Name: Team 5

Creation date and modifications info found on GitHub

"""


import sys
import math
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import base64


#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               Functions to turn the dataframe/csv file to an array
#-------------------------------------------------------------------------------------------------------------------------------------------------
def column_search(arr,parameter):
    #searches dataframe array for a specific column, and returns a digit on which the column exists
    #and a -1 otherwise (to represent that the column was not found
    arr_len = len(arr)
    col = -1
    for n in range(arr_len):
        if arr[n] == parameter:
            col = n
    return col

def vector_to_array(vector):
    rowCount = len(vector)
    arr = [0]*rowCount
    i = 0
    while i < rowCount:
        arr[i] = vector[i][0]
        i+=1
    return arr

def mult_to_array(array):
    #print(array)
    rowCount = len(array)
    colCount = len(array[0])
    data = [[0] for x in range(rowCount)]
    i = 0
    while i < rowCount:
        j = 0
        while j < colCount:
            #print(array[i][j])
            data[i][0] += array[i][j]
            j +=1
        data[i][0] /= colCount
        i+=1
    return vector_to_array(data)


def csv_to_arr(file):
    #turns a csv file into an array
    csvreader = csv.reader(file)
    rows = list(csvreader)
    return rows

def dataframe_to_array(dataframe):
    #turns a pandas dataframe into array (more code is used because we needed to get the column headers as well)
    headers = [0]*len(dataframe.columns)
    n = 0
    for col in dataframe.columns:
        headers[n] = col
        n += 1
    vals = dataframe.to_numpy()
    rows = [[0 for y in range(len(headers))] for x in range(len(vals)+1)]
    rows[0] = headers
    for i in range(len(vals)):
        rows[i+1] = vals[i]
    return rows

def array_cut(rows,parameter=None):
    #if there is no parameter, it will cull the date column, and return the rest of the array
    rowCount = len(rows)
    colCount = len(rows[0])
    if parameter is not None:
        return array_splice(rows,parameter)
    else:
        col = column_search(rows[0], 'Date')
        data = [[0 for y in range(colCount - 1)] for x in range(rowCount - 1)]
        i, j, k = 0, 0, 0
        while i < rowCount - 1:
            while k < colCount - 1:
                if j == col:
                    j += 1
                else:
                    data[i][k] = float(rows[i + 1][j])
                    j += 1
                    k += 1
            j = 0
            k = 0
            i += 1
        return data

def array_splice(rows,parameter):
    #sorts through the array, culling the header row and returning the columns necessary for error algorithms
    rowCount = len(rows)
    j = 0
    data = [[0 for y in range(len(parameter))] for x in range(rowCount-1)]
    while j < len(parameter):
        col = column_search(rows[0], parameter[j])
        if col == -1:
            sys.exit("parameter not found\nreturning whole array")
        else:
            i = 0
            while i < rowCount - 1:
                data[i][j] = float(rows[i + 1][col])
                i += 1
        j += 1
    return data

def get_date(rows):
    rowCount = len(rows)
    col = column_search(rows[0], 'Date')
    if col == -1:
        print("parameter not found\nreturning whole array")
    else:
        data = [[0] for x in range(rowCount - 1)]
        i = 0
        while i < rowCount - 1:
            data[i][0] = (rows[i + 1][col])
            i += 1
    arr = [0]*rowCount
    arr = vector_to_array(data)
    return arr




#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               Functions that run the error algorithms (and a system exit error function
#-------------------------------------------------------------------------------------------------------------------------------------------------
def sys_exit(forecastResult,testSet):
    # if the array sizes don't match, causes a system exit error
    if len(forecastResult[0]) != len(testSet[0]):
        sys.exit("Error: incompatible array sizes")

#pattern is the same for all functions
#   A) checks that the sizes of the arrays are the same
#   B) Runs the sigma forumula for each algorithm, and stores it in an array
#   C) does final calculations that are done outside the sigma formula, and averages it into one usable percentage

def mean_absolute_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_absolute_percentage_error
    error = [0]*len(forecastResult[0])
    length = len(forecastResult[0])
    sys_exit(forecastResult,testSet)
    #B
    for i in range(len(forecastResult)):
        j = 0
        while j < length:
            error[j] += abs(forecastResult[i][j]-testSet[i][j])
            j += 1
    #C
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
    #B
    for i in range(len(forecastResult)):
        j = 0
        while j < length:
            error[j] += abs((testSet[i][j]-forecastResult[i][j])/testSet[i][j])
            j += 1
    #C
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
    #B
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            change = abs(forecastResult[i][j]-testSet[i][j])
            change /= (abs(testSet[i][j]) + abs(forecastResult[i][j]))/2
            error[j] += change
            j += 1
    #C
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
    #B
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            error[j] += ((testSet[i][j] - forecastResult[i][j])**2)
            j += 1
    #C
    val = 0
    for j in range(len(forecastResult[0])):
        error[j] /= len(forecastResult)
        val += error[j]
    val /= length
    return val

def mean_squared_percentage_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_squared_error
    error = [0] * len(forecastResult[0])
    length = len(forecastResult[0])
    sys_exit(forecastResult,testSet)
    #B
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            error[j] += (((testSet[i][j] - forecastResult[i][j])/testSet[i][j])**2)
            j += 1
    #C
    val = 0
    for j in range(len(forecastResult[0])):
        error[j] *= 100/len(forecastResult)
        val += error[j]
    val /= length
    return val

def root_mean_squared_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_squared_error
    error = [0] * len(forecastResult[0])
    length = len(forecastResult[0])
    sys_exit(forecastResult,testSet)
    #B
    for i in range(len(forecastResult)):
        j = 0
        while j < length: #while loop with the sigma formula
            error[j] += ((testSet[i][j] - forecastResult[i][j])**2)
            j += 1
    #C
    val = 0
    for j in range(len(forecastResult[0])):
        error[j] /= len(forecastResult)
        error[j] = math.sqrt(error[j])
        val += error[j]
    val /= length
    return val


def root_mean_squared_percentage_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Root-mean-square_deviation
    error = [0] * len(forecastResult[0])
    length = len(forecastResult[0])
    sys_exit(forecastResult,testSet)
    #B
    for i in range(len(forecastResult)):
        j = 0
        while j < length:  # while loop with the sigma formula
            error[j] += (((testSet[i][j] - forecastResult[i][j])/testSet[i][j]) ** 2)
            j += 1
    #C
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
    #B
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
    #C
    val = 0
    for j in range(len(forecastResult[0])):
        numerator = (size*sumBoth[j])-(sumForecast[j]*sumTest[j])
        denominator = math.sqrt(((size*forecastSquared[j]) - (sumForecast[j]**2))*((size*testSquared[j]) - (sumTest[j]**2)))
        val += numerator/denominator
    val /= length
    return val

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               Functions that edit the error array by sorting it and giving it appropriate names
#                               Used in functions below this section
#-------------------------------------------------------------------------------------------------------------------------------------------------
def double_bubble(array):
    #sorts the error array using bubble sort, also adjusts the corresponding algorithms to match
    n = len(array[0])
    for i in range(n):
        for j in range(0, n - i - 1):
            if array[0][j] > array[0][j + 1]:
                array[0][j], array[0][j + 1] = array[0][j + 1], array[0][j]
                array[1][j], array[1][j + 1] = array[1][j + 1], array[1][j]
    return array

def int_to_alg(numArr):
    #turns the numbers used to represent the algorithms into strings that are the algorithm acronyms
    nameArr = ["" for x in range(len(numArr))]
    for i in range(len(numArr)):
        if numArr[i] == 1:
            nameArr[i] = "MAE"
        if numArr[i] == 2:
            nameArr[i] = "MAPE"
        if numArr[i] == 3:
            nameArr[i] = "SMAPE"
        if numArr[i] == 4:
            nameArr[i] = "MSE"
        if numArr[i] == 5:
            nameArr[i] = "MSPE"
        if numArr[i] == 6:
            nameArr[i] = "RMSE"
        if numArr[i] == 7:
            nameArr[i] = "RMSPE"
        if numArr[i] == 8:
            nameArr[i] = "r-Value"
    return nameArr

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               Functions that creates an array with all the different error algorithms
#                               One for original 6 functions, one for sorted percent errors
#-------------------------------------------------------------------------------------------------------------------------------------------------

def error_calculation(forecastResult, testSet):
    #creates 2D array, first row stores all the error calculations
    #second row stores a number corersponding to the algorithm used
    error = [[0 for i in range(6)] for j in range(2)]
    error[0][0] = mean_absolute_error(forecastResult, testSet)
    error[1][0] = 1
    error[0][1] = mean_absolute_percentage_error(forecastResult,testSet)
    error[1][1] = 2
    error[0][2] = symmetric_mean_absolute_percentage_error(forecastResult,testSet)
    error[1][2] = 3
    error[0][3] = mean_squared_error(forecastResult,testSet)
    error[1][3] = 4
    error[0][4] = root_mean_squared_error(forecastResult,testSet)
    error[1][4] = 6
    error[0][5] = correlation_coefficient(forecastResult,testSet)
    error[1][5] = 8
    error[1] = int_to_alg(error[1])
    return error

def percent_error_calculation(forecastResult, testSet):
    #creates 2D array, first row stores all the error calculations
    #second row stores a number corersponding to the algorithm used
    error = [[0 for i in range(5)] for j in range(2)]
    error[0][0] = mean_absolute_percentage_error(forecastResult,testSet)
    error[1][0] = 2
    error[0][1] = symmetric_mean_absolute_percentage_error(forecastResult,testSet)
    error[1][1] = 3
    error[0][2] = mean_squared_percentage_error(forecastResult,testSet)
    error[1][2] = 5
    error[0][3] = root_mean_squared_percentage_error(forecastResult,testSet)
    error[1][3] = 7
    error[0][4] = correlation_coefficient(forecastResult,testSet)
    error[1][4] = 8
    error = double_bubble(error)
    error[1] = int_to_alg(error[1])
    return error

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               returns dictionary from error array, and for percent error array
#-------------------------------------------------------------------------------------------------------------------------------------------------

def error_array_to_dict(error_array):
    #creates dictionary from error array
    dict = {}
    i = 0
    while i < 6:
        dict[error_array[1][i]] = error_array[0][i]
        i +=1
    return dict

def percent_error_array_to_dict(error_array):
    #creates dictionary from error array
    dict = {}
    i = 0
    while i < 5:
        dict[error_array[1][i]] = error_array[0][i]
        i +=1
    return dict

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               creates bar graph from error metrics (probably will require revamp to make the graph look more professional)
#                               One for error array, one for percent error array
#-------------------------------------------------------------------------------------------------------------------------------------------------

def error_arr_to_bar(error_array):
    x_axis = [0]*len(error_array[0])
    for i in range(len(error_array[0])):
        x_axis[i] = error_array[1][i]
    bar = plt.figure()
    plt.title("Percent Error Difference")
    plt.xlabel("Algorithm")
    plt.ylabel("Percentage Error")
    plt.bar(x_axis,error_array[0])
    plt.ylim(0,10)
    plt.yticks(np.arange(0,10,1))
    return bar

def percent_error_arr_to_bar(error_array):
    x_axis = [0]*len(error_array[0])
    for i in range(len(error_array[0])):
        x_axis[i] = error_array[1][i]
    bar = plt.figure()
    plt.title("Percent Error Difference")
    plt.xlabel("Algorithm")
    plt.ylabel("Percentage Error")
    plt.bar(x_axis,error_array[0])
    plt.ylim(0,10)
    plt.yticks(np.arange(0,10,1))
    return bar

def error_plot(forecast_arr,test_array,date_arr):
    fig = plt.figure(figsize=(20,6))
    plt.plot(date_arr,forecast_arr,'m')
    plt.plot(date_arr,test_array,'b')
    plt.title("Raw Data Difference")
    buf = io.BytesIO()
    plt.savefig(buf,format='png')
    plt.show()
    buf.seek(0)
    return base64.b64encode(buf.getvalue())


#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               Main function. Takes 2 dataframes from forecast and testset, an optional parameter
#                               and returns the bar graph as a variable and the dictionary with the error metrics
#
#                               Use this function to implement the error_algorithms file
#-------------------------------------------------------------------------------------------------------------------------------------------------
def get_error_algorithm(forecastFrame,testFrame,parameter=None):
    forecastResult = array_cut(dataframe_to_array(forecastFrame),parameter)
    testSet = array_cut(dataframe_to_array(testFrame),parameter)
    plot_buf = error_plot(mult_to_array(forecastResult),mult_to_array(testSet),get_date(dataframe_to_array(testFrame)))
    error = error_calculation(forecastResult,testSet)
    error_dict = error_array_to_dict(error)
    result_dict = {'dict':error_dict,'graph':plot_buf,'parameter':parameter}

    return result_dict

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               used for testing, ignore
#-------------------------------------------------------------------------------------------------------------------------------------------------

"""
def main():
    '''
    with open('GOOG_MLE_upload.csv','r') as file:
        forecast = csv_to_arr(file,'Open')
    with open('GOOG_test_set.csv','r') as file2:
        test = csv_to_arr(file2,'Open')

    dict = error_array_to_dict(get_error_graph(forecast,test))
    '''


    dataframe = pd.read_csv('GOOG_MLE_upload.csv')
    dataframe2 = pd.read_csv('GOOG_test_set.csv')
    parameter = ['High','Low']
    dict_final = get_error_algorithm(dataframe,dataframe2,parameter)
    print(dict_final)

main()
"""


