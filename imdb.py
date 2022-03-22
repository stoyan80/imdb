from urllib import request
from bs4 import BeautifulSoup
import requests


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text
    else:
        exit()

html = get_html('https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm')
soup = BeautifulSoup(html, "html.parser")

urls = []
base_url = 'https://www.imdb.com'

for posterColumn in soup.select('.lister-list > tr > td.posterColumn'):
    rating = posterColumn.contents[3]['data-value']
    if float(rating) >= 6.8:
        a = posterColumn.find('a')
        url = base_url + a['href']
        urls.append(url)

for url in urls:
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    # TODO: refacture! Use a class, or at least a function for each sub-task, like get_genres()...

    # -------------------------------- get genres -------------------------------- #
    genres = ''
    genres_div = soup.find('div', attrs={'data-testid' : {'genres'}})
    for gs in genres_div.find_all('span'):
        genres+=';'+gs.text

    print('~'* 30)
    print(genres)
    print('~'* 30)


    # ------------------------------- get director ------------------------------- #
    span = soup.find("span", string="Director")
    div = span.find_next_sibling("div")
    director = div.find("a").text
    print(director)