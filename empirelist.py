import requests
from bs4 import BeautifulSoup as bs
import json

url = 'https://www.empireonline.com/movies/features/best-movies-2/'
response = requests.get(url)
contents = response.text

soup = bs(contents,'html.parser')
data = json.loads(soup.select_one("#__NEXT_DATA__").contents[0])


print(isinstance(data,dict))
def find_articles(data):
    if isinstance(data, dict):
        for k, v in data.items():
            # print(k,v)
            if k.startswith("ImageMeta:"):
                yield v["titleText"]
            else:
                yield from find_articles(v)
    elif isinstance(data, list):
        for i in data:
            yield from find_articles(i)


movies = [a for a in find_articles(data)]

with open('movies.txt',mode='w',encoding='utf-8') as film_list:
    for i in reversed(movies):
        film_list.write(f'{i} \n')
