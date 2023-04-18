# Import libraries
import requests
import urllib
import re
import io
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import urljoin
import pandas as pd


# Set the URL you want to webscrape from

# Open and read urls from external input file

mb_pageurls = open('mb_pageurls-list.txt','r')
mb_outputFile = io.open('mortgagebroker-list-new.txt', 'a', encoding='utf-8')
mb_page_urls_list = mb_pageurls.readlines() # use this to read data in different lines

# run firefox webdriver from executable path of your choice
driver = webdriver.Firefox()

mb_outputFile.write("First Name\tLast Name\tEmail\tCity\tState\tCompany")
mb_outputFile.write("\n")

ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36','accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}

for eachurl in mb_page_urls_list:
    # get web page
    driver.get(eachurl)
    print(eachurl)

    # execute script to scroll down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")

    # sleep for 5s
    time.sleep(5)

    content = driver.page_source
    response = requests.get(eachurl, headers=ua)
    soup = BeautifulSoup(response.content, 'lxml')
    mb_tag_all = soup.find_all('div', attrs={"class": "broker col-lg-4 col-md-6 col-xs-12"})

    for eachdivtag in mb_tag_all:
        each_member_details_tag = eachdivtag.find_next('div', attrs={"class": "broker-tile-body standard"})
        print(each_member_details_tag)
        try:
            mb_firstname = each_member_details_tag.find('a', attrs={"class": "viewdetails_button standard"})['data-preferred_name']
            print(mb_firstname)
        except KeyError:
            print("None")
        try:
            mb_lastname = each_member_details_tag.find('a', attrs={"class": "viewdetails_button standard"})['data-last_name']
            print(mb_lastname)
        except KeyError:
            print("None")
        try:        
            mb_email = each_member_details_tag.find('a', attrs={"class": "viewdetails_button standard"})['data-email']
            print(mb_email)
        except KeyError:
            print("None")
        try:
            mb_city = each_member_details_tag.find('a', attrs={"class": "viewdetails_button standard"})['data-city']
            print(mb_city)
        except KeyError:
            print("None")
        try:
            mb_state = each_member_details_tag.find('a', attrs={"class": "viewdetails_button standard"})['data-state']
            print(mb_state)
        except KeyError:
            print("None")
        try:
            mb_company = each_member_details_tag.find('a', attrs={"class": "viewdetails_button standard"})['data-company']
            print(mb_company)
        except KeyError:
            print("None")
        mb_outputFile.write(mb_firstname + '\t' + mb_lastname + '\t' + mb_email + '\t' + mb_city + '\t' + mb_state + '\t' + mb_company + '\t' + eachurl)
driver.close

mb_outputFile.close()
print("File: ", mb_outputFile, "is completed")