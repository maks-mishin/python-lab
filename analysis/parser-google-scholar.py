# Parser scholar.google.com

import requests
import csv
from bs4 import BeautifulSoup as bs

from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
            }

# list of query text for requests
QUERY_TEXT = ['coronavirus', 'COVID-19', 'SARS-CoV-19']

# list of years for research
YEARS = [i for i in range(2000, 2021)]

# maximum number of the search results page
MAX_PAGE = 101

# base url
ROOT_URL = 'https://scholar.google.com'

# function for
def generate_initial_data():
    list_of_dicts = []
    # dicts for each query
    # key - number of year
    # value - list of all pages for research
    coronavirus_dict = {}
    covid_dict = {}
    sars_sict = {}

    for year in YEARS:
        temp_list_cor = []
        temp_list_covid = []
        temp_list_sars = []

        # addind to temporary list first page for each year from YEARS
        # because it address is different from the others (2-100)
        temp_list_cor.append(ROOT_URL + f'/scholar?q={QUERY_TEXT[0]}&hl=ru&as_sdt=0%2C5&as_vis=1&as_ylo={year}&as_yhi={year}')
        temp_list_covid.append(ROOT_URL + f'/scholar?q={QUERY_TEXT[1]}&hl=ru&as_sdt=0%2C5&as_vis=1&as_ylo={year}&as_yhi={year}')
        temp_list_sars.append(ROOT_URL + f'/scholar?q={QUERY_TEXT[2]}&hl=ru&as_sdt=0%2C5&as_vis=1&as_ylo={year}&as_yhi={year}')
        
        # adding to temporary list all of pages from 2 to 100
        for num_page in range(1, 100):
            temp_list_cor.append(ROOT_URL + f'/scholar?start={num_page}0&q=coronavirus&hl=ru&as_sdt=0,5&as_ylo={year}&as_yhi={year}&as_vis=1')
            temp_list_covid.append(ROOT_URL + f'/scholar?start={num_page}0&q=%22COVID-19%22&hl=ru&as_sdt=0,5&as_ylo={year}&as_yhi={year}&as_vis=1')
            temp_list_sars.append(ROOT_URL + f'/scholar?start={num_page}0&q=SARS-CoV-2&hl=ru&as_sdt=0,5&as_ylo={year}&as_yhi={year}&as_vis=1')
        
        # add temporary list to dict for each query
        coronavirus_dict[year] = temp_list_cor
        covid_dict[year] = temp_list_covid
        sars_sict[year] = temp_list_sars

    list_of_dicts.append(coronavirus_dict)
    list_of_dicts.append(covid_dict)
    list_of_dicts.append(sars_sict)
    return list_of_dicts

def parse_one_query(session, root_dict):
    temp_dict = {}
    # for one query
    for year in root_dict.keys():
        temp_list = []
        for url in root_dict[year]:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            # all divs of publications
            divs_pub = soup.find_all('div', attrs={'class' : 'gs_r gs_or gs_scl'})
            
            # for current page
            for div in divs_pub:
                # here we get all the necessary data about each publication
                # for example - title of publication
                title = div.find('h3', attrs={'class':'gs_rt'})
                temp_list.append({
                    # here we add the necessary data to temporary list
                    'title': title                    
                })
        temp_dict[year] = temp_list
    return temp_dict

def parse_google_scholar(root_url, headers):
    # list of dicts for to store the necessary data
    # key - year, value - list of dicts with the necessary data
    publications_cor = {}
    publications_covid = {}
    publications_sars = {}


    session = requests.Session() #for emulation browser work
    request = session.get(root_url, headers=headers) #response from server
    
    if request.status_code == 200:
        # initial data for analysis
        list_urls = generate_initial_data()

        publications_cor = parse_one_query(session, list_urls[0])
        publications_covid = parse_one_query(session, list_urls[1])
        publications_sars = parse_one_query(session, list_urls[2])            
    else:
        print('Error. Status code = ' + str(request.status_code))
    print('Done. Status code = ' + str(request.status_code))

    return 0

# function for export data to csv-file
# (not fully implemented)
def export_to_file(dict_user, file_name):
    with open(file_name + '.csv', 'w', encoding='utf-8') as file_out:
        a_pen = csv.writer(file_out)
        a_pen.writerow(('Year', 'List'))
        for key in dict_user.keys():
            a_pen.writerow((key, dict_user[key]))