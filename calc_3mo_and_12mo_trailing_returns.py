# Matthew Bates, 2017
# Code written in Python 3
# This code computes and plots the trailing 3 months and 12 month returns for a small 
# portfolio of stocks, stock indexes, and funds and shows each one's greatest drawdown.

import urllib
import numpy as np
import matplotlib.pyplot as plt
import datetime as DT
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter


#identify the yahoo ticker symbols for which I want data
stocks=['^GSPC','VIX','DIA','SPY','GDX','USO','VWO','GOOG','GS','F','JNJ','QCOM','BA','KO']
#(note, these cover a range of industries via both ETFs and stocks.)

for stock in stocks:
  
  ##### READ AND PARSE THE DATA #####  
  #build the url and read the full contents as a string (going back to 1960, if able)
  url = 'http://ichart.finance.yahoo.com/table.csv?s=' + stock + '&a=0&b=1&c=1960'
  fulltext = urllib.request.urlopen(url).read().decode('utf-8')
  
  #split the fulltext into individual lines based on the newline character
  fulltextlines = fulltext.splitlines()
  
  #Split the lines into headers and an array of data, based by comma characters
  header = fulltextlines[0].split(',')
  data = np.array([line.split(',') for line in fulltextlines[1:]])
  
  
  
  ##### COMPUTE THE 3 & 12 MONTH TRAILING PERCENT RETURNS #####  
  #Note, to use acutal instead of adjusted close, use data[4] instead of data[6].
  #Note, There are an avg of 252 trading days per year, avg of 21 trading days per month.
  R3 = []                           
  for i in range(len(data)-63):            #3mo*21 day/mo = avg of 63days in 3 months.
    R3.append([(float(data[i,6]) - float(data[i+63,6])) / float(data[i+63,6]) *100])
    
  R12 = []                           
  for i in range(len(data)-252):            #3mo*21 day/mo = avg of 63days in 3 months.
    R12.append([(float(data[i,6]) - float(data[i+252,6])) / float(data[i+252,6]) *100])
 


  ##### MAKE PLOTS FOR CLOSING PRICES & 3/12MO TRAILING RETURNS #####
  ## PLOT THE ADJUSTED CLOSING PRICE ##
  pltdata = []
  for i in range(len(data)):
    pltdata.append((DT.datetime.strptime(data[i][0], "%Y-%m-%d"), data[i][6]))
                
  x = [date2num(date) for (date, value) in pltdata]
  y = [value for (date, value) in pltdata]
  
  fig, ax = plt.subplots()
  ax.plot(x,y, linewidth=0.5)
  ax.xaxis.set_major_formatter(DateFormatter('%d %b %Y')) #('%b %d %Y'))
  ax.xaxis_date()  #tell matplotlib to interpret the x-axis values as dates
  plt.gcf().autofmt_xdate(rotation=45) #rotate the x labels
  plt.title(stock + ' - Adjusted Closing Price')  
  plt.ylabel('$')
  plt.xlabel('time')
  plt.show()

  ## PLOT THE CALCUALTED 3 MONTH PERCENT RETURNS ##
  pltdata = []
  for i in range(len(data)-63):
    pltdata.append((DT.datetime.strptime(data[i][0], "%Y-%m-%d"), R3[i]))
                
  x = [date2num(date) for (date, value) in pltdata]
  y = [value for (date, value) in pltdata]
  
  fig, ax = plt.subplots()
  ax.plot(x,y, linewidth=0.5)
  ax.xaxis.set_major_formatter(DateFormatter('%d %b %Y')) #('%b %d %Y'))
  ax.xaxis_date()  #tell matplotlib to interpret the x-axis values as dates
  plt.gcf().autofmt_xdate(rotation=45) #rotate the x labels
  plt.title(stock + ' - 3 Month Trailing Returns (%)'
  + '\n(the largest drawdown in this period was ' + '%.2f' % min(R3)[0] + '%)')  
  plt.ylabel('3mo % change in value')
  plt.xlabel('dates before present')
  plt.show()

  ## PLOT THE CALCUALTED 12 MONTH PERCENT RETURNS ##
  pltdata = []
  for i in range(len(data)-252):
    pltdata.append((DT.datetime.strptime(data[i][0], "%Y-%m-%d"), R12[i]))
                
  x = [date2num(date) for (date, value) in pltdata]
  y = [value for (date, value) in pltdata]
  
  fig, ax = plt.subplots()
  ax.plot(x,y, linewidth=0.5)
  ax.xaxis.set_major_formatter(DateFormatter('%d %b %Y')) #('%b %d %Y'))
  ax.xaxis_date()  #tell matplotlib to interpret the x-axis values as dates
  plt.gcf().autofmt_xdate(rotation=45) #rotate the x labels
  plt.title(stock + ' - 12 Month Trailing Returns (%)'
  + '\n(the largest drawdown in this period was ' + '%.2f' % min(R12)[0] + '%)')  
  plt.ylabel('12mo % change in value')
  plt.xlabel('dates before present')
  plt.show()

  ##Note, the greatest drawdown is shown below each chart's title.
