# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 21:19:52 2018

@author: simonlousky
"""


import TickersData as td
import pandas as pd
import statistics as stat


def function_ctir(from_date, to_date, tickers):
    """
    Function that receives a start date, a end date and a list of shares from the user and return 
    a table with summaries of data for each share in the list.
    Paremeters
    ----------
    from_date: string
               The start date, need to be in format yyyy-mm-dd.
    to_date: string
             The end date, need to be in format yyyy-mm-dd.
    tickers: string
             The input of selected tickers(ID), need to be separate by commas.
    lst_tickers: list
                 The list of selected tickers(ID).
    up_lst_tickers: list
                    The list of selected tickers which exist in the databases.
    lst_total_profit: list
                      The list of total profit of selected tickers which exist in the databases.               
    lst_peak_to_valley: list
                        The list of peak_to_valley of selected tickers which exist in the databases.
    lst_max: list
             The list of max value of selected tickers which exist in the databases.
    lst_min: list
             The list of min value of selected tickers which exist in the databases.
    lst_mean: list
              The list of average of selected tickers which exist in the databases.
    lst_stdev: list
               The list of standard deviation of selected tickers which exist in the databases.       
    ticker_name: string
                 ticker name.
    data_close_ticker: pandas.core.frame.DataFrame
                                   
    lst_close: list
               The list of closing price of the share.
    final_data: pandas.core.frame.DataFrame
                The return table with summaries of data for each share in the list.          
    
    """
    
    lst_tickers= tickers.split(',')

    up_lst_tickers= []
    lst_total_profit= []
    lst_peak_to_valley= []
    lst_max= []
    lst_min= []
    lst_mean= []
    lst_stdev= []

    for ticker_name in lst_tickers:
    
       try:
           data_close_ticker= td.get_data_for_ticker_in_range(ticker_name,from_date,to_date, ['close'])
       except ValueError:
           print("The share {} is not found in the database or on the range date you choose.".format(ticker_name))
           continue
    
       lst_close= []
       for date in range(len(data_close_ticker)):
          lst_close.append(data_close_ticker["close"].ix[date])
    
       up_lst_tickers.append(ticker_name)
       lst_total_profit.append(float(format(lst_close[0]/lst_close[-1],'.4f')))
       lst_peak_to_valley.append(td.get_p2v_for_ticker_in_range(ticker_name,from_date,to_date)[0])
       lst_max.append(max(lst_close))
       lst_min.append(min(lst_close))
       lst_mean.append(float(format(stat.mean(lst_close),'.4f')))
       lst_stdev.append(float(format(stat.stdev(lst_close),'.4f')))
        
    
    final_data= pd.DataFrame(data=up_lst_tickers, columns=['ticker'])
    final_data['total_profit']= lst_total_profit
    final_data['peak_to_valley']= lst_peak_to_valley
    final_data['maximum']= lst_max
    final_data['minimum']= lst_min
    final_data['mean']= lst_mean
    final_data['stdev']=lst_stdev
    
    return(final_data)
    
if __name__ == "__main__":
    from_date= input("Enter the start date in the format yyyy-mm-dd:")
    to_date= input("Enter the end date in the format yyyy-mm-dd:")
    tickers= input("Enter the ID of the shares you want to analyze(please separate the names with commas):")
    print(function_ctir(from_date, to_date, tickers))
