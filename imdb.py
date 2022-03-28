from urllib import request
from bs4 import BeautifulSoup
import csv, sqlite3, re
import requests



# initialize csv headers
def create_csv():
    with open('mpm.csv', 'w') as csvfile:
        fieldnames = ['title', 'director', 'genres', 'rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

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
    if float(rating) >= 7.0:
        a = posterColumn.find('a')
        url = base_url + a['href']
        urls.append(url)

for url in urls:
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")




    genres = ' '
    genres_div = soup.find('div', attrs={'data-testid' : {'genres'}})
    for gs in genres_div.find_all('span'):
        genres+=' '+gs.text


    director = soup.find('div', {'class': 'ipc-metadata-list-item__content-container'}).find('ul').findChildren("a")[0].text

    movies_name = soup.find('div', {'class': 'sc-94726ce4-0 cMYixt'}).find('h1').text

    rating = soup.find('div', {'class': 'sc-7ab21ed2-0 fAePGh'}).find('span').text

    writer.writerow({'title': movies_name, 'director': director, 'genres': genres, 'IMDb Rating': rating})



def create_db():
    create_csv()
    conn = sqlite3.connect('mpm.db')
    c = conn.cursor()
    c.execute('CREATE TABLE mpm (title, director, genres, rating);')
    with open('mpm.csv', 'r') as csv_file:
        dr = csv.DictReader(csv_file)
        to_db = [(i['title'], i['director'], i['genres'],['rating']) for i in dr]
        c.executemany('INSERT INTO mpm (title, director, genres, rating) VALUES (?, ?, ?, ?);', to_db)
        conn.commit()
        conn.close()

create_db()