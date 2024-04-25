# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 15:41:04 2024

@author: IGNAOLSZ
"""

#import wapi
#from wapi import Session
#ID = 'OE7t6tjKJVsFt3.5eNPhtSmXehtbFNeP'
#secret = 'sMTOQr5s9gf4Ml95V8OzD9g-PWCy.hhLfCNpQXnZ0jBI2HIS7GQwpEfO9HqXMCxzIF1Wo58S0rrc9SQQZvMb_mHUdcG2uyWCfF4r'
#ses = wapi.Session(client_id=ID, client_secret=secret, timeout=30000)

#unit_list = ses.get_units()

from unit_list_module import data

unit_list = data

#api_key = 'res fr hydro sgw GWh cet h n'

def get_unit(api_key):

    def extract_unit_code(api_key):
        # Split the API key by spaces
        parts = api_key.split()
        # Iterate over parts to find the unit code
        for part in parts:
            # Convert both part and unit key to lowercase for comparison
            part_lower = part.lower()
            if any(unit['key'].lower() == part_lower for unit in unit_list):
                return part
        return None

    def get_unit_description(api_key, unit_list):
        unit_code = extract_unit_code(api_key)
        if unit_code:
            for unit in unit_list:
                # Convert both unit key and unit_code to lowercase for comparison
                if unit['key'].lower() == unit_code.lower():
                    return unit['name']
            return "Description not found"

    #unit_descriptions = []
    description = get_unit_description(api_key, unit_list)

    return description

#kupa = get_unit('res fr hydro sgw GWh cet h n')

#kupa


#from unit_list_module import data

#unit_list = data

#data