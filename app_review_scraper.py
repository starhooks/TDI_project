#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 1 19:52:40 2019

@author: xma
"""

import requests
import datetime
import time
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import pandas as pd

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
targetURL = 'https://play.google.com/store/apps/details?id=com.passportparking.mobile.parkchicago&showAllReviews=true'
head = 'https://play.google.com'


def setbrower():
   

    # Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(chrome_options=options)

    driver.get(targetURL)
    target = 0
    count = 0
    numReviews = 1960
    #numReviews = 200
    while target <=numReviews:
        print('parsing', str(numReviews) ,'count......')
        ## Simulate the behavior of human browsing
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #driver.execute_script("document.getElementById('show-more-button').click();")
        if count == 4 :  
            print('clicking...')
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div').click()
            print('clicked')
            time.sleep(0.5)
            count = 0
        time.sleep(0.5)
        driver.execute_script("window.scrollTo(2, 22);")
        time.sleep(0.5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        #data_list = soup.select('.id-card-list .card')
        #data_list = soup.select('.W4P4ne ')
        data_list = soup.find('div',jsname='fk8dgd')
        index = len(data_list)
        print('index',index)
        count += 1
        
        #driver.find_element_by_class_name('CwaK9').click()
        
        #target = int(data_list[index - 1].select('.title')[0].text.split('.')[0])
        target = len(data_list)
        print("target count:", target)
    driver.close()
    driver.quit()
    return data_list



if __name__ == "__main__":
    tStart = time.time()
    print('Start parsing google play...(1/2)')
    data_list = setbrower()
    #app_item = getAppLink(data_list)
    print('Start parsing google play...(2/2)')



    reviews_df = []
    
    len_data = len(list(data_list.children))
    #len_data = 1
    for i in range(len_data):
        item = list(data_list.children)[i]
        time = item.find('span', class_='p2TkOb').text # time
        
        rate_obj = item.find('div', class_ = 'pf5lIe')
        rate = rate_obj.findAll('div')[0]
        rate_txt = rate.attrs['aria-label']    
        rating = rate_txt.split(' ')[1] # rate score
        
        comment = item.find('span', jsname='bN97Pc').text # comment
        
        temp = pd.DataFrame({'Time':time,'Rating':rating,'Review Text':comment},index=[0])
    
        reviews_df.append(temp)
    
    
    
    reviews_df = pd.concat(reviews_df,ignore_index=True)
    reviews_df.to_csv('reviews_list.csv', encoding='utf-8')
    
    print('DONE')





