# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 12:01:46 2024

@author: IGNAOLSZ
"""

from datetime import datetime

def input_with_validation(prompt, validation_func=None):
    while True:
        user_input = input(prompt)
        if validation_func:
            if validation_func(user_input):
                return user_input
            else:
                print("Invalid input. Please try again.")
        else:
            return user_input

def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_datetime(datetime_text):
    try:
        datetime.strptime(datetime_text, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def validate_boolean(boolean_text):
    return boolean_text.lower() in ['true', 'false']

def validate_integer(integer_text):
    return integer_text.isdigit()

def get_parameters():
    parameters = {}

    # Handling multiple values
    parameters['tag'] = input_with_validation("Enter tags (comma-separated): ").split(',')
    parameters['issue_date'] = input_with_validation("Enter issue dates (comma-separated, format YYYY-MM-DD): ", validate_date).split(',')

    # Handling single values with validation
    parameters['issue_date_from'] = input_with_validation("Enter issue date from (format YYYY-MM-DD): ", validate_date)
    parameters['issue_date_to'] = input_with_validation("Enter issue date to (format YYYY-MM-DD): ", validate_date)
    parameters['issue_month'] = input_with_validation("Enter issue month (1 - 12 or jan - dec): ")
    parameters['issue_weekday'] = input_with_validation("Enter issue weekday (0 - 6 or sun - mon): ")
    parameters['issue_day'] = input_with_validation("Enter issue day (1-31): ", validate_integer)
    parameters['issue_time'] = input_with_validation("Enter issue time (HH, HH:mm:ss or HH:mm): ")
    parameters['with_data'] = input_with_validation("Get instance with data? (true/false): ", validate_boolean)
    parameters['data_from'] = input_with_validation("Enter data from datetime (format YYYY-MM-DD HH:MM:SS): ", validate_datetime)
    parameters['data_to'] = input_with_validation("Enter data to datetime (format YYYY-MM-DD HH:MM:SS): ", validate_datetime)
    parameters['time_zone'] = input("Enter time zone: ")
    parameters['output_time_zone'] = input("Enter output time zone: ")
    parameters['filter'] = input("Enter filter: ")
    parameters['function'] = input("Enter function: ")
    parameters['frequency'] = input("Enter frequency: ")
    parameters['modified_since'] = input_with_validation("Enter modified since date (format YYYY-MM-DD): ", validate_date)

    return parameters

# Example of using the get_parameters function
if __name__ == "__main__":
    parameters = get_parameters()
    print(parameters)
