# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 10:41:43 2024

@author: IGNAOLSZ
"""
from get_volue_2 import fetch_curve_by_name_and_category
from transform import transform_data

result = fetch_curve_by_name_and_category("Poland", "Temperature")
if result is not None:
    print(result)
else:
    print("Could not fetch data.")
    
type(result)

transform_data(result)