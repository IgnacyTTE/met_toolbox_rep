# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 14:24:11 2024

@author: IGNAOLSZ
"""
def get_unit(categories):
    # Split the categories string into a list of individual categories
    category_list = categories.split()
    # Dictionary to map categories to their units
    category_units = {
        'tt': '°C',  # Degrees Celsius
        'res': 'GWh',  # Gigawatt hours
        'wind': 'MW',  # Megawatts
        # Add more categories and their units here
    }
    for category in category_list:
        if category in category_units:
            return category_units[category]
    return 'Unknown'  # Return 'Unknown' if no known category is found
    

def get_name(primary_category, area, secondary_category, model, freq, datatype, timezone='cet'):
    # Determine the unit
    unit = get_unit(primary_category)
    timezone = 'cet'
    
    # Components of the curve name, now including the time zone after the unit
    components = [primary_category, area, secondary_category, model, unit, timezone, freq, datatype]
    
    # Filter out empty components to avoid unnecessary spaces
    filtered_components = filter(lambda x: x and x.strip(), components)
    
    # Join the components with a space, ignoring any that are empty
    curve_name = ' '.join(filtered_components)
    
    return curve_name