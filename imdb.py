from urllib import request
from bs4 import BeautifulSoup
import csv, sqlite3
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
    if float(rating) >= 7.0:
        a = posterColumn.find('a')
        url = base_url + a['href']
        urls.append(url)

def create_csv():
    with open('mpm.csv', 'w') as csvfile:
        # initialize csv headers
        fieldnames = ['title', 'director', 'genres', 'ratings']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for url in urls:
            html = get_html(url)
            print(url)
            soup = BeautifulSoup(html, "html.parser")



    # -------------------------------- get genres -------------------------------- #
            genres = ''
            try:
                genres_div = soup.find('div', attrs={'data-testid' : {'genres'}})
                print(genres_div)
                for gs in genres_div.find('span'):
                        genres+=' '+gs.text
            except:
                genres = 'None'






    # ------------------------------- get director ------------------------------- #
            try:
                director = soup.find('div', {'class': 'ipc-metadata-list-item__content-container'}).find('ul').findChildren("a")[0].text
            except:
                director = 'None'






    # ------------------------------- get film name ------------------------------- #
            try:
                movies_name = soup.find('div', {'class': 'sc-94726ce4-0 cMYixt'}).find('h1').text
            except:
                movies_name = 'None'

    # ------------------------------- get ratings ------------------------------- #
            try:
                ratings = soup.find('div', {'class': 'sc-7ab21ed2-0 fAePGh'}).find('span').text
            except:
                rating = 'None'

            writer.writerow({'title': movies_name, 'director': director, 'genres': genres, 'ratings': ratings})


def create_db():
    create_csv()
    conn = sqlite3.connect('mpm.db')
    c = conn.cursor()
    c.execute('CREATE TABLE mpm (title, director, genres, ratings);')
    with open('mpm.csv', 'r') as csv_file:
        dr = csv.DictReader(csv_file)
        to_db = [(i['title'], i['director'], i['genres'], i['ratings']) for i in dr]
    c.executemany('INSERT INTO mpm (title, director, genres, ratings) VALUES (?, ?, ?, ?);', to_db)
    conn.commit()
    conn.close()

create_db()