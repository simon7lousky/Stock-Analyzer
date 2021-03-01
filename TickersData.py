# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 18:07:35 2018

@author: simonlousky
"""

import pandas as pd
import os
import datetime
import warnings
warnings.filterwarnings("ignore")




def fetch_ticker(ticker_name,timerange=''):
    """
    Function that imports the data of the appropriate ticker_name.

    Paremeters
    ----------
    ticker_name: string
                 The name of the share that the user selected. 
    timerange: string
               The parameter of length time series.
               2 options: '' returns only the latest 100 data points. 
                          'full' returns the full-length time series of up to 20 years of historical data.
    url: string
         A helped link variable.
    ready_data_ticker: pandas.core.frame.DataFrame
                       The basic data of the selected share.
    """
    ticker_name= str.upper(ticker_name)
    if timerange!="" and timerange!="full":
       raise ValueError("The parameter timerange can only accept the values: '' of 'full'.")
    if timerange=="":
       timerange="compact"
    try:
       url= "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={}&apikey=ROB5U3GW2F12PUIH&datatype=csv&outputsize={}".format(ticker_name, timerange)
       ready_data_ticker = pd.read_csv(url,sep=',', encoding='utf8', parse_dates=['timestamp'],dayfirst=True, index_col='timestamp')
       ready_data_ticker = ready_data_ticker.fillna(method='ffill')
       
       if os.path.exists("./data")==False:
           os.makedirs("./data")
       if os.path.exists("./data/{}.csv".format(ticker_name))==False:
           ready_data_ticker.to_csv("./data/{}.csv".format(ticker_name))
    except ValueError:
       raise ValueError("Sorry. The ticker_name that you choise is not found in the database of the site 'alphavantage'.")
    
#fetch_ticker('dell',timerange='full')
        





def get_data_for_ticker_in_range(ticker_name,from_date,to_date, data_type):
    """
    Function that receives a share ID, start date, end date, and list of data types 
    and returns a Pandas.DataFrame object that contains a table with the requested data.
    Paremeters
    ----------
    from_date: datetime.datetime
               The start date converted to type datetime.datetime.
    to_date: datetime.datetime
             The end date converted to type datetime.datetime.
    lst_col_data_ticker: list
                         The list of avaible data types in the database.
    data_ticker: pandas.core.frame.DataFrame
                 The basic data of the selected share.
    ready_data_ticker: pandas.core.frame.DataFrame
                       The returned object that contains a table with the requested data.                     
    """
    try:
       from_date=datetime.datetime.strptime(from_date,"%Y-%m-%d")
       to_date=datetime.datetime.strptime(to_date,"%Y-%m-%d")
    except:
       raise ValueError("The format of parameters from_date or to_date is not'%Y-%m-%d'.")    
    
    
    if to_date < from_date:
        raise ValueError("The date range you entered is in reversed order.")
    lst_col_data_ticker = ['open','high','low','close','volume']
    for i in data_type: 
       if i not in lst_col_data_ticker:
            raise ValueError("The list of variable types you entered includes a non-existent type in the database.")
    
    if os.path.exists("./data")==False:
        os.makedirs("./data")
    if os.path.exists("./data/{}.csv".format(ticker_name)):
        data_ticker = pd.read_csv("./data/{}.csv".format(ticker_name), sep=',', encoding='utf8', parse_dates=['timestamp'], index_col='timestamp')
    else:
        fetch_ticker(ticker_name, "full")
        data_ticker = pd.read_csv("./data/{}.csv".format(ticker_name),sep=',', encoding='utf8', parse_dates=['timestamp'], index_col='timestamp')
    
    ready_data_ticker = data_ticker[to_date:from_date]
    ready_data_ticker = ready_data_ticker[data_type]
    if ready_data_ticker.empty:
        raise ValueError("The date range you entered is not included in the database existing in your download file.")
    ready_data_ticker['ticker_name'] = ticker_name
    return(ready_data_ticker)
    
#x= get_data_for_ticker_in_range('MCD','2000-01-10','2000-01-01', ['open','high','low','close','volume'])      
#print(x)






def get_profit_for_ticker_in_range(ticker_name,from_date,to_date, accumulated=False):
    """
    Function that receives a share ID, start date, end date, and boolean parameter 'accumulated'.
    The function returns a Pandas.DataFrame object which contains a table with profit data in the time range requested. 
    Paremeters
    ----------
    data_close_ticker: pandas.core.frame.DataFrame
                       The basic data which includes ticker_name and closing price of the share.
                       He changes throughout the function.
    lst_close: list
               The list of closing price of the share.
    lst_daily_profit: list
                      The list of daily profit of the share.
    lst_cumulative_profit: list
                           The list of cumulative profit of the share.
    last: float
          A helped variable that saves the last cumulative profit calculated.
    
    """
    data_close_ticker= get_data_for_ticker_in_range(ticker_name,from_date,to_date,['close'])
    data_close_ticker= data_close_ticker.sort_index(ascending=True)
    lst_close= list(data_close_ticker['close'])
    
    lst_daily_profit = [0]
    for i in range(len(lst_close)-1):
        lst_daily_profit.append(lst_close[i+1]/lst_close[i]-1)
    lst_cumulative_profit = lst_daily_profit[:2]
    last = lst_cumulative_profit[-1]
    for i in range (2,len(lst_daily_profit)):
        lst_cumulative_profit.append(((1+last)*(1+lst_daily_profit[i])-1))
        last= lst_cumulative_profit[-1]
    data_close_ticker['daily_profit']= lst_daily_profit
    data_close_ticker['cumulative_profit']= lst_cumulative_profit

    if accumulated:
        return data_close_ticker[['ticker_name','cumulative_profit']]
    return data_close_ticker[['ticker_name','daily_profit']]
    
    
#x=get_profit_for_ticker_in_range('MSFT','2002-04-01','2002-04-04', accumulated=False)
#print(x)
#y=get_profit_for_ticker_in_range('DELL','2002-04-01','2002-04-04', accumulated=False)
#print(y)






def get_p2v_for_ticker_in_range(ticker_name,from_date,to_date):
    """
    Function that receives a share ID,a start date and an end date.
    The function returns the value(ratio) of peak_to_valley,the value of peak, the value of valley 
    and the number of trading days between them in the time range requested.
    Paremeters
    ----------
    data_close_ticker: pandas.core.frame.DataFrame
                       The data which includes ticker_name and closing price of the share.
    lst_close: list
               The list of closing price of the share.
    i: int
       A helped index that runs on the list lst_close.
    j: int
       A helped index that runs on the list lst_close from i+1 to the end(loop in loop).
    peak_to_valley: float
                    The value(ratio) of peak_to_valley.
    peak: float
          The value of peak.
    valley: float      
            The value of valley.
    days_between: int         
                  The number of trading days between peak and valley.
    """
    
    data_close_ticker= get_data_for_ticker_in_range(ticker_name,from_date,to_date,['close'])
    data_close_ticker= data_close_ticker.sort_index(ascending=True)
    lst_close= list(data_close_ticker['close'])
    peak_to_valley= 0
    for i in range(len(lst_close)):
        for j in range(len(lst_close[i+1:])):
            if (lst_close[i+1+j]/lst_close[i]-1) < peak_to_valley:
                peak_to_valley = lst_close[i+1+j]/lst_close[i]-1
                peak= lst_close[i]
                valley = lst_close[i+1+j]
                days_between = j+1
     
    return (float(format(peak_to_valley,'.4f')),float(format(peak,'.2f')),float(format(valley,'.2f')), days_between)          
                 
#y= get_p2v_for_ticker_in_range('dell','2015-02-10','2015-02-20')             
#print(y)                 
         

         
         
         
         
         
         
         
       



    
  




















