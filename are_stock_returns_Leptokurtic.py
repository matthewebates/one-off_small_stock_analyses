# Matthew Bates, 2017
# Code written in Python 3
# This code calculates and plots stock daily returns, fits a Gaussian distribution to the
# mean and standard deviation of the data for each stock, and compares that Gaussian curve of 
# best fit to the historgram of daily returns to determine if each stock's returns are 
# Leptokurtic (narrower than the Gaussian, indicating a greater chance of tail risk events).


import urllib                               #for making web requests
import numpy as np                          #for data arrays and processing
import matplotlib.mlab as mlab              #for fitting the best Gaussian curve
import matplotlib.pyplot as plt             #for plotting histograms and curves


#identify the yahoo ticker symbols for the stocks that I want to analyze
stocks=['^GSPC','VIX','DIA','SPY','GDX','USO','VWO','GOOG','GS','F','JNJ','QCOM','BA']
#(note, these cover a range of industries via both ETFs and stocks.)

for stock in stocks:

  
  ##### RETRIEVE AND PARSE THE DATA #####  
  #build the url and read the full contents as a string (going back in time upto 1960)
  url = 'http://ichart.finance.yahoo.com/table.csv?s=' + stock + '&a=0&b=1&c=1960'
  fulltext = urllib.request.urlopen(url).read().decode('utf-8')
  
  #split the fulltext into individual lines based on the newline character
  fulltextlines = fulltext.splitlines()
  
  #Split the lines into headers and an array of data, based by comma characters
  header = fulltextlines[0].split(',')
  data = np.array([line.split(',') for line in fulltextlines[1:]])

  
  
  ##### COMPUTE THE NATURAL LOG FOR 1 DAY TRAILING RETURNS #####  
  #Note, to use acutal instead of adjusted close, use data[4] instead of data[6].
  #Note, There are an avg of 252 trading days per year, avg of 21 trading days per month.
  R1day = []
  for i in range(len(data)-1):              #-1 becuase the last day won't have a comparison.
    R1day.append(np.log(float(data[i,6]) / float(data[i+1,6])))


  
  ##### PLOT THE HISTOGRAM FOR THE RETURNS DATA AND IT'S GAUSSIAN CURVE OF BEST FIT #####  
  #generate the histogram and save the parameters for our line of best fit.
  n, bins, patches = plt.hist(R1day, bins=100, normed=True, alpha=0.4)
  
  #generate the Gaussian line of best fit for the histogram.
  y = mlab.normpdf(bins, np.mean(R1day), np.std(R1day, ddof=1))
  l = plt.plot(bins, y, 'r--', linewidth=2)
  
  #add labels and plot the histogram and Gaussian line of best fit.
  plt.title("Histogram and Gaussian curve of best fit for stock: " + stock)
  plt.xlabel("bins for: size of percent '+ n_day +' day returns")
  plt.ylabel("relative proportion of returns within each bin")
  #plt.axis([-.25, .25, 0, 1])
  plt.grid(True)
  plt.show()
  
  print("Mean  of distribution of log daily returns:", np.mean(R1day))
  print("StDev of distribution of log daily returns:", np.std(R1day, ddof=1))
