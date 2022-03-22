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

# seed = []
base_url = 'https://www.imdb.com'

for posterColumn in soup.select('.lister-list > tr > td.posterColumn'):
    rating = posterColumn.contents[3]['data-value']
    if float(rating) >= 6.8:
        a = posterColumn.find('a')
        seed = base_url + a['href']
        print(seed)