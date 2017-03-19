# Matthew Bates, 2017
# Code written in Python 3
# Compute historical volatilities for time series of stock adjusted closing prices, and then 
# calculates the correlation coefficient between the volatility and a time series of 21 day 
# (i.e., monthly) trailing returns for each stock.

#Import packages
import urllib                               #for making web requests
import numpy as np                          #for data arrays and processing
import matplotlib.pyplot as plt             #for plotting histograms and curves
import datetime as DT                       #for manipulating datetimes
from matplotlib.dates import date2num       #for plotting datetimes
from matplotlib.dates import DateFormatter  #for plotting datetimes

month = 21       #21 trading days per month.
year = 252       #252 trading days per year.

##### Define a function to download & parse time series of stock adjusted closing prices #####
def getYahooFinanceStockData(stock = '^GSPC', fromEarliestYear = 1960):
    '''Description: Function to get historical stock data from Yahoo Finance
    Input: a string with the stock symbol (in the format known to Yahoo Finance; defaults to the symbol for the S&P 500;
     also an integer for the staring four-digit year from which to pull data from then until present (defaults to 1960).
    Output: a numpy array of string dates (for market closing events), a list of real number adjusted closing prices on those dates.
    Note: the returned dates and prices are indexed from 0 = most recent clsoing price to max = earliest closing price available or found in period.'''

    #build the url and read the full contents as a string (going back in time upto start of specified year)
    url = 'http://ichart.finance.yahoo.com/table.csv?s=' + stock + '&a=0&b=1&c='+str(fromEarliestYear)
    fulltext = urllib.request.urlopen(url).read().decode('utf-8')
  
    #split the fulltext into individual lines based on the newline character
    fulltextlines = fulltext.splitlines()

    #split the lines into headers and an array of data, based by comma characters
    header = fulltextlines[0].split(',')    #for now, fine to just discard the header...
    data = np.array([line.split(',') for line in fulltextlines[1:]])
  
    #note, reported closing values are column data[4], adjusted closing prices are data[6].
    adjustedClosingPrices = list(map(float, data[:,6]))  #convert it to a list of floats instead of strings.
    closing_dates = data[:,0]
  
    return closing_dates, adjustedClosingPrices

##### Define a function to calculate lognormal n-day trailing stock returns #####
def calcLogNormalStockReturns(stockPrices = np.empty(0), n_days=1):   
    '''Description: calcualtes the lognormal return from a specified stock over n days; is an alternative to fn: calcPercentStockReturns().
    Input: a numpy array of real number stock prices over time (defaults to an empty array); and an integer 
     for the number of days difference in the past to use in calculating the trailing returns (defaults to one day prior)
    Output: a list of real numbers for lognormal stock returns over the previous n days, for each day in the initial array.
    Note: there are an avg of 5 trading days per week, 21 trading days per month, 252 trading days per year.'''

    #COMPUTE THE N-DAY TRAILING PERCENT RETURNS  
    n_day_lognormal_returns = np.empty(len(stockPrices) - n_days)
    for i in range(len(stockPrices) - n_days):      #n-day training return; use "-n" to omit oldest n days that won't have a pair with which to compare
        n_day_lognormal_returns[i] = np.log(float(stockPrices[i]) / float(stockPrices[i+n_days]))
  
    return n_day_lognormal_returns



##### Define a function that calculates historic stock volatility #####
def calcStockVolatility(stockPrices = []):
    volatility = []  #empty list to record results
    for i in range(len(stockPrices) - month):    #"- month" becuase last 21 days have truncated past.
        mysum = 0
        for j in range(month):
            mysum += np.log(stockPrices[i+j] / stockPrices[i+j+1])**2
            #note, using i+j to go back in time becuase my data is indexed w/ newer data at front.

        volatility.append( np.sqrt(year * mysum / month ))
    
    return volatility


##### Define a function to calculate the correlation coefficient between two time series #####
def calcTimeSeriesCorrelation(x = [], y = []):
    avg_x = np.average(x)
    avg_y = np.average(y)
    stdev_x = np.std(x)
    stdev_y = np.std(y)
    mysum = 0
    for i in range(len(x)):
        mysum += (x[i] - avg_x) * (y[i] - avg_y)
    #mysum = sum((x[i] - avg_x) * (y[i] - avg_y) for i in range(len(x)))
    correlCoeff = mysum / (len(x) * stdev_x * stdev_y)
    #correlCoeff = np.corrcoef(stock_prices[:-month], volatilities)
    
    return correlCoeff


##### Define a function to plot a time series of stock price data #####
def plotStockReturns(stock_name, closing_dates, stock_prices, axis_label):

    pltdata = []
    for i in range(len(stock_prices)):
        pltdata.append((DT.datetime.strptime(closing_dates[i], "%Y-%m-%d"), stock_prices[i]))
                
    x = [date2num(date) for (date, value) in pltdata]
    y = [value for (date, value) in pltdata]
  
    fig, ax = plt.subplots()
    ax.plot(x,y, linewidth=0.5)
    ax.xaxis.set_major_formatter(DateFormatter('%d %b %Y')) #('%b %d %Y'))
    ax.xaxis_date()  #tell matplotlib to interpret the x-axis values as dates
    plt.gcf().autofmt_xdate(rotation=45) #rotate the x labels
    plt.title('Stock ' + stock_name + ': ' + axis_label)  
    plt.ylabel(axis_label)
    plt.xlabel('dates prior to the present')
    plt.show()


##### Demonstrate the functions above for some example stocks #####
stocks = ['DIA','^GSPC','SPY','GDX','GOOG','GS','F','JNJ','QCOM','BA','WMT','NKE','AMZN','AAPL']
myyear = 1995

for stock in stocks:
    plt.style.use('ggplot')                     #set ploting style
    closing_dates, stock_prices = getYahooFinanceStockData(stock, myyear)
    plotStockReturns(stock, closing_dates, stock_prices, 'adjusted closing price ($)')
  
    log_returns = calcLogNormalStockReturns(stock_prices, month)
    plotStockReturns(stock, closing_dates[month::], log_returns, '21-day trailing lognormal returns')
  
    plt.style.use('bmh')                        #set ploting style
    volatilities = calcStockVolatility(stock_prices)
    plotStockReturns(stock, closing_dates, volatilities, 'annualized volatility')
    
    correl = calcTimeSeriesCorrelation(log_returns, volatilities)
    print('Correlation between stock prices & annualized volatility is:', correl, '\n')
    print('---------------------------------------------------------------------------------')
