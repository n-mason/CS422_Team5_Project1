import sys
import math

def mean_absolute_error(forecastResult, testSet): #formula taken from https://en.wikipedia.org/wiki/Mean_absolute_error
    error = 0
    length = len(forecastResult)
    if length != len(testSet):
        sys.exit("Error: incompatible array sizes") #if the array sizes don't match, causes an error
    i = 0
    while i < length: #while loop with the sigma formula
        error += abs(forecastResult[i]-testSet[i])
        i += 1
    print("Mean Absolute Error is " + str(round((error/length),2))) #prints results with final calculations
    return round((error/length),2)

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




'''
def main():
    guess = [1,2,3,4,5]
    truth = [2,4,3,5,6]
    mean_absolute_error(guess,truth) #tested with https://www.statology.org/mean-absolute-error-calculator/
    mean_absolute_percentage_error(guess,truth) #tested with https://www.statology.org/mape-calculator/
    symmetric_mean_absolute_percentage_error(guess,truth) #only calculator found with sMAPE option had wrong formula, was not able to test with online calculator (should still work though)
    mean_squared_error(guess,truth) #tested with https://www.statology.org/mse-calculator/
    root_mean_squared_error(guess,truth) #tested with https://www.statology.org/rmse-calculator/
    correlation_coefficient(guess,truth) #tested with https://www.socscistatistics.com/tests/pearson/default2.aspx
'''


