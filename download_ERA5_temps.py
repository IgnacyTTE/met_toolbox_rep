# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 14:27:23 2024

@author: corsquil
updated by: IGNAOLSZ
"""

import datetime as dt
import requests
import calendar

#save_dir = r"C:\Users\IGNAOLSZ\Documents\Python Scripts\reanalysis_RES_dist\Raw_Data\era5_temp"

def download_era5(in_date,out_date, save_dir):
    '''
    Parameters
    ----------
    in_date : datetime.date object
        start date of reanalysis data we're interested
    out_date : datetime.date object
        end date of reanalysis data we're interested

    Returns None.
    Saves the reanalysis file in save_dir
    
    '''
    
    user = 'CORSQUIL'
    # central_date = dt.datetime(2020, 10, 4)
    var = 't_mean_2m_24h:C'
    area = '75,-15_32,40'
    res = '1.00,1.00'
    
    #check last available era-5 date
    # print('query')
    query_string = f'http://cmdp_prod:9000/v1/meteo/get_time_range?model=ecmwf-era5&parameters={var}&remoteUser={user}&timeout=900000'
    r = str(requests.get(query_string, allow_redirects=True).content)
    # print(r)
    
    era5_start = in_date
    
    last_date = r.split(';')[-1]
    era5_end = dt.date(int(last_date[:4]), int(last_date[5:7]), int(last_date[8:10]))
    if out_date < era5_end:
        era5_end = out_date
    
    
    # os.mkdir('C:/Users/CORSQUIL/Desktop/Projects/tropical_forcing/ERA5_speed201') #' {str(era5_start.day).zfill(2)}_{str(era5_start.month).zfill(2)}_{str(era5_start.year)}_precip')
    # print('ready')
    #need to split the time interval in order to make the query
    time_int = f'{str(era5_start.year)}-{str(era5_start.month).zfill(2)}-{str(1).zfill(2)}T00:00:00Z--{str(era5_end.year)}-{str(era5_end.month).zfill(2)}-{str(era5_end.day).zfill(2)}T23:59:00Z:P1D'
    
    
    query_string = f'http://cmdp_prod:9000/v1/meteo/{time_int}/'+var+'/'+area+':'+res+'/netcdf?model=ecmwf-era5&remoteUser={user}&timeout=900000'
    # print(query_string)
    # print('ready for r')
    r = requests.get(query_string, allow_redirects=True)
    # print('got the data')
    
    file_name = '/era5_temp_x_dist.nc'
    file_dir = save_dir + file_name
    
    # f = open(f'P:\QFA\TonyWeather\Corso_Intern\reanalysis_RES_dist\era5_{year}-{month}_temp.nc','wb')
    
    f = open(file_dir,'wb')
    f.write(r.content)
    f.close()


            
if __name__ == '__main__':       
    
    selected_month = 3
    selected_year = 2024
    
    save_dir = r"C:\Users\IGNAOLSZ\Documents\Python Scripts\reanalysis_RES_dist\Raw_Data\era5_temp"
    
    in_date = dt.date(selected_year,selected_month,1)
    out_date = dt.date(selected_year, selected_month, calendar.monthrange(selected_year, selected_month)[1])
    
    download_era5(in_date,out_date, save_dir)
    
    print('Data saved to file:' + save_dir)
