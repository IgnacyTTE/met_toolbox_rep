# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 13:37:51 2024

@author: IGNAOLSZ
"""


import wapi
import os
from wapi import Session
ID = 'OE7t6tjKJVsFt3.5eNPhtSmXehtbFNeP'
secret = 'sMTOQr5s9gf4Ml95V8OzD9g-PWCy.hhLfCNpQXnZ0jBI2HIS7GQwpEfO9HqXMCxzIF1Wo58S0rrc9SQQZvMb_mHUdcG2uyWCfF4r'
ses = wapi.Session(client_id=ID, client_secret=secret, timeout=30000)

#unit_list = ses.get_units()

#def save_units_as_py(ses, directory, filename='unit_list.py'):
#    """Fetch units from API and save them to a Python file in the specified directory."""
#    # Ensure the directory exists
#    if not os.path.exists(directory):
#        os.makedirs(directory)
#    full_path = os.path.join(directory, filename)
#
#    # Fetch the data from the API
#    print("Fetching data from API...")
#    unit_list = ses.get_units()
    
    # Save the data to a Python file
#    with open(full_path, 'w') as file:
        # Write data to Python file as a dictionary
#        file.write(f"data = {unit_list}\n")
    
#    print(f"Data saved to {full_path}")

def save_units_as_py(ses, directory, filename='unit_list_module.py'):
    """Fetch units from API and save them to a Python file in the specified directory using UTF-8 encoding."""
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    full_path = os.path.join(directory, filename)

    # Fetch the data from the API
    print("Fetching data from API...")
    unit_list = ses.get_units()
    
    # Save the data to a Python file with UTF-8 encoding
    with open(full_path, 'w', encoding='utf-8') as file:
        # Write data to Python file as a dictionary
        file.write(f"data = {unit_list}\n")
    
    print(f"Data saved to {full_path}")

# Specify the directory where you want to save the file
directory = r"C:\Users\IGNAOLSZ\Documents\Python Scripts\wraper"

# Call the function to fetch and save the data
#save_units_as_py(ses, directory)

#country_list = ses.get_areas()

def save_areas_as_py(ses, directory, filename='area_list_module.py'):
    """Fetch units from API and save them to a Python file in the specified directory using UTF-8 encoding."""
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    full_path = os.path.join(directory, filename)

    # Fetch the data from the API
    print("Fetching data from API...")
    area_list = ses.get_areas()
    
    # Save the data to a Python file with UTF-8 encoding
    with open(full_path, 'w', encoding='utf-8') as file:
        # Write data to Python file as a dictionary
        file.write(f"data = {area_list}\n")
    
    print(f"Data saved to {full_path}")
    
save_areas_as_py(ses, directory)