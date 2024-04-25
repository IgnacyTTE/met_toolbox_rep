# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 10:41:43 2024

@author: IGNAOLSZ
"""
from get_volue_5 import fetch_voule
from transform_3 import transform_data

#Input parameters for your curve type - supply zero if given parameter not required for your curve

tag = 'Ave'
issue_date = '2018-01-01T00:00'
issue_date_from = '2018-01-01T00:00'
issue_date_to = '2018-01-03T00:00'
data_from = '2018-01-01T00:00'
data_to = '2018-01-03T00:00'
function ='AVERAGE'
frequency ='H'
area = 'France'
category = 'Temperature'


curve_key = 'tt de con ec00 °c cet min15 f'

df = fetch_voule(area, category, curve_key, tag, issue_date, issue_date_from, issue_date_to, data_from, data_to, function, frequency)

df = transform_data(df, curve_key)

df