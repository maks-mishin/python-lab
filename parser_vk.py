import requests
import time
import csv

# Function for parse posts from group 'tproger_web'
def get_posts_vk():
    token = '952810fd952810fd952810fd9e95583c8a99528952810fdcb4e05a7f76f85cad15f4067'
    version = 5.103
    domain = 'tproger_web'
    count = 100
    offset = 0
    all_posts = []

    while offset < 500:
        # return json-object
        response = requests.get(
            'https://api.vk.com/method/wall.get',
            params={
                'access_token': token,
                'v': version,
                'domain': domain,
                'count': count,
                'offset': offset
            }
        )
        data = response.json()['response']['items']
        offset += 100
        all_posts.extend(data)
        time.sleep(0.5)
    return all_posts

def file_writer(all_posts):
    with open('tproger_web.csv', 'w', encoding='utf-8') as file:
        a_pen = csv.writer(file)
        a_pen.writerow(('likes', 'body', 'url'))
        for post in all_posts:
            try:
                if post['attachments'][0]['type']:
                    img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
                else:
                    img_url = 'pass'
            except: 
                pass
            a_pen.writerow(( post['likes']['count'], post['text'], img_url ))
    
all_posts = get_posts_vk()
file_writer(all_posts)
