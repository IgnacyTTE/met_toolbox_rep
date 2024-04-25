# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 15:06:27 2024

@author: IGNAOLSZ
"""

import ftplib

def connect_metelogica_ftp():

    # FTP Information:
    HOSTNAME = "ftp.meteologica.com"
    USERNAME = "axpo_IT_variables"
    PASSWORD = "k.qQ533D"

    # Create server connection
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

    return ftp_server