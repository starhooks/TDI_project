#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 23:21:12 2019

@author: xma
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Read the dataset in csv
#data = pd.read_csv('temp_datalab_records_social_facebook.csv', sep=',')

year_vector =['2010','2011','2012','2013','2014','2015','2016','2017','2018']
#year_vector =['2015']

for i in range(len(year_vector)):

    chunk_size = 10000
    
    filename = 'parking_tickets.csv'
    df = pd.DataFrame()
    #year = '2016'
    year = year_vector[i]
    dim = 'issue_date'
    
    for chunk in pd.read_csv(filename, sep=',', chunksize=chunk_size):
        #print(chunk)
        #if pd.isnull(chunk['brand']).all() == False:
        if chunk[dim].str.contains(year).any():
            chunk_concern = chunk.loc[chunk[dim].str.contains(year)]
            df = pd.concat([df,chunk_concern])
            print('logging...'+year)
    
    
    #df.to_csv(r'data_2018.csv', header=True,index=False)
        
    saveFileName = 'issue_' + str(year) + '.csv'
    #df.to_csv(r'issue_2016.csv', header=True,index=False)
    df.to_csv(saveFileName, header=True,index=False)

