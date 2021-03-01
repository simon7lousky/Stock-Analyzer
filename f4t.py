# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 17:28:23 2018

@author: simonlousky
"""

"""
Program that receives start date, end_date, share ID, 
name(or path and name) of the file and format of the file from the user.
The program stores all the share data in the requested time range, in the 
requested format into a file with the name and the requested path.
If there is no path, the file will be saved in the current directory.
Paremeters
----------
from_date: string
           The start date, need to be in format yyyy-mm-dd.
to_date: string
         The end date, need to be in format yyyy-mm-dd.
ticker_name: string
             The share ID.
name_file_or_path_and_name_file: string
                                 The name(or path and name) of the file.
format_file: string
             The format of the file.
lst_name_file_or_path_and_name_file: list
                                     The list of the parts of the path and name 
                                     or list with only file name.
name_file: string
           The file name.
lst_path: list
          The list of the parts of the path or empty list.
path: string
      The path of the file.
data_ticker: pandas.core.frame.DataFrame
             The data of the selected share.                                     
"""

import os
import TickersData as td

from_date= input("Enter the start date in the format yyyy-mm-dd:")
to_date= input("Enter the end date in the format yyyy-mm-dd:")
ticker_name= input("Enter the ID of the share:")
name_file_or_path_and_name_file= input("Enter the file name or path and name of a file:")
format_file= input("Enter your selected format, csv or json:")

lst_name_file_or_path_and_name_file= name_file_or_path_and_name_file.split('/')
name_file= lst_name_file_or_path_and_name_file[-1]
lst_path= lst_name_file_or_path_and_name_file[:-1]
path="/".join(lst_path)


data_ticker= td.get_data_for_ticker_in_range(ticker_name,from_date,to_date, ['open','high','low','close','volume'])
if len(lst_name_file_or_path_and_name_file)==1:
    if format_file=="csv":
        data_ticker.to_csv("./{}.csv".format(name_file))
    if format_file=="json":
        data_ticker.to_json("./{}.json".format(name_file))
        
if len(lst_name_file_or_path_and_name_file)>1:
    try:
       if os.path.exists(path):
           if format_file=="csv":
               data_ticker.to_csv("{}.csv".format(name_file_or_path_and_name_file))
           if format_file=="json":
               data_ticker.to_json("{}.json".format(name_file_or_path_and_name_file))
       else:
           os.makedirs(path)
           if format_file=="csv":
               data_ticker.to_csv("{}.csv".format(name_file_or_path_and_name_file))
           if format_file=="json":
               data_ticker.to_json("{}.json".format(name_file_or_path_and_name_file))
    except:
        print("You have error in your format path.")

        