# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 11:33:15 2024

@author: IGNAOLSZ
"""
import pandas as pd
from area_list_module import data 

area_list = pd.DataFrame(data)

# Function to get the area key from the area name
def get_area_key(area_name):
    result = area_list[area_list['name'] == area_name]['key']
    if not result.empty:
        return result.iloc[0].lower()
    else:
        return "Area name not found"

# Example usage
#print(get_area_key('Denmark'))
#print(get_area_key("Sweden"))