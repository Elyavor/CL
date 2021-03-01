import requests
from bs4 import BeautifulSoup as bs
import json

url = 'https://www.kinopoisk.ru/film/2360/reviews/ord/date/status/all/perpage/50/'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

def get_html(url, params=''):
    req = requests.get(url, headers=headers, params=params)
    return req

def get_content(html):
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='reviewItem userReview')
    reviews = []
    
    for item in items:
        reviews.append(
            {
                'title': item.find('p', class_='sub_title').get_text(strip=True),
                'description': item.find('span', class_='_reachbanner_').get_text(strip=True)
            }
        )
    return reviews

def parser():
    pagenation = input('укажите количество страниц: ')
    pagenation = int(pagenation)
    html = get_html(url)
    if html.status_code == 200:
        reviews = []
        for page in range(1, pagenation):
            print(f'собираю данные со страницы: {page}')
            html = get_html(url, params={'page': page})
            reviews.extend(get_content(html.text))
            with open('reviews.json', 'w') as file:
                json.dump(reviews, file, indent=2, ensure_ascii=False)
            print(reviews)
    else:
        print('error')

parser()