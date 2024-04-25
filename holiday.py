# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:10:10 2024

@author: IGNAOLSZ
"""
from area_list_module import data
#import wapi
#from wapi import Session
#from datetime import date
import holidays
#ID = 'OE7t6tjKJVsFt3.5eNPhtSmXehtbFNeP'
#secret = 'sMTOQr5s9gf4Ml95V8OzD9g-PWCy.hhLfCNpQXnZ0jBI2HIS7GQwpEfO9HqXMCxzIF1Wo58S0rrc9SQQZvMb_mHUdcG2uyWCfF4r'
#ses = wapi.Session(client_id=ID, client_secret=secret, timeout=30000)

#country_list = ses.get_areas()
country_list = data
#def get_country(api_key):
#    def get_country_description(api_key, country_list):
#        country_code = extract_country_code(api_key)
#        if country_code:
#           for country in country_list:
#                # Convert both unit key and unit_code to lowercase for comparison
#                if country['key'].lower() == country_code.lower():
#                    return country['name']
#            return "Description not found"

    #unit_descriptions = []
#    description = get_country_description(api_key, country_list)

#   return description

#def extract_country_code(api_key):
    # Split the API key by spaces
#    parts = api_key.split()
    # Iterate over parts to find the unit code
#    for part in parts:
        # Convert both part and unit key to lowercase for comparison
#        part_lower = part.lower()
#        if any(country['key'].lower() == part_lower for country in country_list):
#            return part
#    return None

def extract_country_code(api_key):
    # Split the API key by spaces
    parts = api_key.split()
    # country_list = ses.get_areas()
    # Iterate over parts to find the country code, excluding 'tt'
    for part in parts:
        # Convert both part and country key to lowercase for comparison
        part_lower = part.lower()
        if part_lower != 'tt' and any(country['key'].lower() == part_lower for country in country_list):
            return part
    # Default to 'de' if no valid country code is found
    return 'de'

kupa = extract_country_code('tt fr con ec00ens °c cet min15 f')

kupa_d = kupa.upper()

kupa_d

#country_holidays = holidays.CountryHoliday(kupa)

#country_holidays

us_holidays = holidays.country_holidays(kupa_d)

'2000-01-01' in us_holidays