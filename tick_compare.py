# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 00:52:03 2018

@author: simonlousky
"""
"""
Program that receives a start date, a end date,a list of shares and a variable the user wants 
to compare and analyze. The program will create a graph in the given period, 
which compares the  selected variable for the shares on the list.
In addition, the program will display a table with summaries data for each share in the list.
Paremeters
----------
from_date: string
           The start date, need to be in format yyyy-mm-dd.
    to_date: string
             The end date, need to be in format yyyy-mm-dd.
    tickers: string
             The input of selected tickers(ID), need to be separate by commas.
    var_test: string
              The variable the user wants to compare(can get:'close','high','low','daily_profit','cumulative_profit').
    lst_tickers: list
                 The list of selected tickers(ID).
    ticker_data: pandas.core.frame.DataFrame
                 The data which includes the variable to compare of the share.
                 An auxiliary variable that changes along the loop
                 
"""


import TickersData as td
from ctir import function_ctir
import matplotlib.pyplot as plt

from_date= input("Enter the start date in the format yyyy-mm-dd:")
to_date= input("Enter the end date in the format yyyy-mm-dd:")
tickers= input("Enter the ID of the shares you want to analyze(please separate the names with commas):")
var_test= input("Enter the variable you want to compare:")
 
lst_tickers= tickers.split(',')
while var_test not in ['close','high','low','daily_profit','cumulative_profit']:
    print("You did not give an appropriate variable for comparison. Try again.")
    var_test= input("Enter the variable you want to compare:")


for ticker_name in lst_tickers:
    try:
       if var_test== 'close':
           ticker_data= td.get_data_for_ticker_in_range(ticker_name,from_date,to_date, ['close'])
           plt.plot(ticker_data.index, ticker_data.close, label= ticker_name)
       if var_test== 'high':
           ticker_data= td.get_data_for_ticker_in_range(ticker_name,from_date,to_date, ['high'])
           plt.plot(ticker_data.index, ticker_data.high, label= ticker_name)
       if var_test== 'low':
           ticker_data= td.get_data_for_ticker_in_range(ticker_name,from_date,to_date, ['low'])
           plt.plot(ticker_data.index, ticker_data.low, label= ticker_name)    
       if var_test== 'daily_profit':
           ticker_data= td.get_profit_for_ticker_in_range(ticker_name,from_date,to_date)
           plt.plot(ticker_data.index, ticker_data.daily_profit, label=ticker_name) 
       if var_test== 'cumulative_profit':
           ticker_data= td.get_profit_for_ticker_in_range(ticker_name,from_date,to_date,accumulated="true")
           plt.plot(ticker_data.index, ticker_data.cumulative_profit, label= ticker_name)
    except ValueError:
           print("The share {} is not found in the database or on the range date you choose.".format(ticker_name))
           continue



plt.title(str.upper(var_test))
plt.legend()
plt.show()

print(function_ctir(from_date,to_date, tickers))
    