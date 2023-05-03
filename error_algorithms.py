import sys
import math
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               Functions to turn the dataframe/csv file to an array
#-------------------------------------------------------------------------------------------------------------------------------------------------
def column_search(arr,parameter):
    arr_len = len(arr)
    col = -1
    for n in range(arr_len):
        if arr[n] == parameter:
            col = n
    return col


def csv_to_arr(file):
    csvreader = csv.reader(file)
    rows = list(csvreader)
    return rows

def dataframe_to_array(dataframe):
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

def array_sort(rows,parameter=''):
    rowCount = len(rows)
    colCount = len(rows[0])
    if parameter != '':
        col = column_search(rows[0], parameter)
        if col == -1:
            parameter = ''
            print("parameter not found\nreturning whole array")
        else:
            data = [[0] for x in range(rowCount - 1)]
            i = 0
            while i < rowCount - 1:
                data[i][0] = float(rows[i + 1][col])
                i += 1
            return data

    if parameter == '':
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

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               Functions that run the error algorithms (and a system exit error function
#-------------------------------------------------------------------------------------------------------------------------------------------------
def sys_exit(forecastResult,testSet):
    if len(forecastResult[0]) != len(testSet[0]):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error


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

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               Function that creates an array with all the different error algorithms
#-------------------------------------------------------------------------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               Functions that edit the error array by sorting it and giving it appropriate names
#-------------------------------------------------------------------------------------------------------------------------------------------------
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

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               returns dictionary from error array
#-------------------------------------------------------------------------------------------------------------------------------------------------

def error_array_to_dict(error_array):
    dict = {}
    i = 0
    while i < 5:
        dict[error_array[1][i]] = error_array[0][i]
        i +=1
    return dict

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               creates bar graph from error metrics (probably will require revamp to make the graph look more professional)
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

#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               Main function. Takes 2 dataframes from forecast and testset, an optional parameter
#                               and returns the bar graph as a variable and the dictionary with the error metrics
#
#                               Use this function to implement the error_algorithms file
#-------------------------------------------------------------------------------------------------------------------------------------------------
def get_error_algorithm(forecastFrame,testFrame,parameter=''):
    forecastResult = array_sort(dataframe_to_array(forecastFrame),parameter)
    testSet = array_sort(dataframe_to_array(testFrame),parameter)
    error = error_calculation(forecastResult,testSet)
    error = double_bubble(error)
    error[1] = int_to_alg(error[1])
    error_graph = error_arr_to_bar(error)
    error_dict = error_array_to_dict(error)
    result_dict = {'graph':error_graph,'dict':error_dict}

    return result_dict




#-------------------------------------------------------------------------------------------------------------------------------------------------
#                               used for testing, ignore
#-------------------------------------------------------------------------------------------------------------------------------------------------

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
    dict_final = get_error_algorithm(dataframe,dataframe2)
    print(dict_final['dict'])
    plt.show()

main()


