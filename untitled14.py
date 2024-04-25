# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:49:36 2024

@author: IGNAOLSZ
"""

import wapi
from wapi import Session
ID = 'OE7t6tjKJVsFt3.5eNPhtSmXehtbFNeP'
secret = 'sMTOQr5s9gf4Ml95V8OzD9g-PWCy.hhLfCNpQXnZ0jBI2HIS7GQwpEfO9HqXMCxzIF1Wo58S0rrc9SQQZvMb_mHUdcG2uyWCfF4r'
ses = wapi.Session(client_id=ID, client_secret=secret, timeout=30000)
# retrieve information about any of the metadata groups that you are interested in.
#ses.get_areas()
#ses.get_categories()
#ses.get_commodities()
#ses.get_curve_types()
#ses.get_data_types()
#ses.get_frequencies()
#ses.get_scenarios()
#ses.get_sources()
#ses.get_stations()
#ses.get_time_zones()
#ses.get_units()

#curve = ses.get_curve(name='tt de con ec00 °c cet min15 f')
#curve.curve_type # check the type of the given curve
#ses.get_curve_types()
#ses.get_commodities()
#ses.get_units()

ses.get_frequencies()