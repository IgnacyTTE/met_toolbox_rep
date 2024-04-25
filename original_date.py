# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:00:08 2024

@author: IGNAOLSZ
"""

def transform_original_date(df):
    df.index.name = 'Original Date'
    df['Year'] = df.index.year
    df['Month'] = df.index.month
    df['Day'] = df.index.day
    
    # Remove leap year
    mask = (df['Day'] == 29) & (df['Month'] == 2)
    df = df[~mask].copy(deep=True)
    
    return df