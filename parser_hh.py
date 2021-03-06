# Parser HeahHunter.ru

import requests
import csv
from bs4 import BeautifulSoup as bs

from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
            }

SEARCH_TEXT = 'python'
base_url = 'https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&search_period=3&salary=&st=searchVacancy&text=' + SEARCH_TEXT

#function parse
def hh_parse(base_url, headers):
    jobs = []
    urls = [] #список доступных для парсинга страниц
    urls.append(base_url)
    session = requests.Session() #for emulation browser work
    request = session.get(base_url, headers=headers) #response from server

    if request.status_code == 200:
        request = session.get(base_url, headers=headers)
        soup = bs(request.content, 'lxml') #return all content on base_url
        try:
            pagination = soup.find_all('a', attrs={'data-qa': 'pager-page'})
            count = int(pagination[-1].text) #количество страниц доступных для парсинга
            for i in range(count):
                url = f'https://hh.ru/search/vacancy?clusters=true&area=1&enable_snippets=true&search_period=3&salary=&st=searchVacancy&text=' + SEARCH_TEXT + '&page={i}'
                if url not in urls:
                    urls.append(url) #формируем список url
        except:
            pass

        #парсим каждый url из urls
        for url in urls:
            request = session.get(url, headers=headers)
            soup = bs(request.content, 'lxml')
            divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'}) #all of divs (vacancies)
            for div in divs:
                try:
                    date = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-date'}).text
                    title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                    href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                    company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text

                    text1 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                    text2 = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text

                    content = text1 + ' ' + text2
                    jobs.append({
                        'date' : date,
                        'title': title,
                        'href': href,
                        'company': company,
                        'content': content
                    })
                except:
                    continue

                salary = None
                try:
                    salary = div.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                except:
                    pass

                jobs[-1]['salary'] = salary

            #print('Count of items in jobs: ' + str(len(jobs)))
    else:
        print('Error. Status code = ' + str(request.status_code))
    print('Done. Status code = ' + str(request.status_code))

    return jobs

jobs = hh_parse(base_url, headers)

def analisys(list_dates, dct):
    for job in jobs:
        list_dates.append(job['date'])

    for i in list_dates:
        if i in dct:
            dct[i] += 1
        else:
            dct[i] = 1

list_dates = []
dct = {}
analisys(list_dates, dct)

size = range(len(dct.keys()))
plt.title('Кол-во опубликованных вакансий по дням')
ax = plt.gca()

ax.bar(size, dct.values(), align='center')
ax.set_xticks(size)

ax.set_xticklabels(dct.keys())
plt.show()

def export_to_file(jobs):
    with open('parsed_jobs.csv', 'w', encoding='utf-8') as file_out: #открытие файла на добавление
        a_pen = csv.writer(file_out)
        a_pen.writerow(('Date of publication', 'Title of vacancy', 'Salary', 'URL', 'Company', 'About vacancy'))  # передаем tuple
        for job in jobs:
            a_pen.writerow((job['date'], job['title'], job['salary'],
                            job['href'], job['company'], job['content']))

export_to_file(jobs)