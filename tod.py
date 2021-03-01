# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 13:42:46 2018

@author: simonlousky
"""

"""
Program that receives a date and a list of shares from the user.
The program prints, for each share, the closing price and the daily profit
on the selected date.
Paremeters
----------
date: string
      The input date, need to be in format yyyy-mm-dd.
tickers: string
         The input of selected tickers(ID), need to be separate by commas.
lst_tickers: list
             list of selected tickers.
"""

import TickersData as td

date=input("Enter the desired date in the format yyyy-mm-dd:" )
tickers= input("Enter the ID of the shares you want to analyze on the same date (please separate the names with commas):")
lst_tickers= tickers.split(',')

for i in lst_tickers:
    try:
       print()
       print("Ticker {} in date {}:".format(i,date))
       print("The closing price:",td.get_data_for_ticker_in_range(i,date,date,['close']).iat[0,0])
       print("The daily profit:",float(format(td.get_profit_for_ticker_in_range(i,'1970-01-01',date).iat[-1,1],'.4f')))
    except ValueError:
       print("The share {} is not found in the database or on the date you choose.".format(i))
       continue
    