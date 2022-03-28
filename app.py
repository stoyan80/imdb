from flask import Flask, request, jsonify, render_template
import os, csv, sqlite3

# initialize flask app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mpm.db')

# database info
db = 'mpm.db'
tb_name = 'mpm'
col_title, col_director, col_genres, col_rating = 'title', 'director', 'genres', 'rating'

# option for using csv besides sqlite3
def get_csv():
    csv_file = open('./mpm.csv', 'r')
    csv_list = list(csv.DictReader(csv_file))
    return csv_list

# endpoint to display all movies
@app.route('/')
def index():
    csv_list = get_csv()
    return render_template('index.html', object_list=csv_list)

# endpoint to query by title
@app.route('/title=<title>/')
def find_title(title):
    conn = sqlite3.connect('mpm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM {} WHERE UPPER({}) LIKE UPPER("%{}%")'.\
            format(tb_name, col_title, title))
    rows = c.fetchall()
    c.close()
    return jsonify(rows)

# endpoint to query by year
@app.route('/genres=<genres>/')
def find_year(year):
    conn = sqlite3.connect('mpm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM {} WHERE {}="{}"'.\
            format(tb_name, col_genres, genres))
    rows = c.fetchall()
    c.close()
    return jsonify(rows)

# endpoint to query by director
@app.route('/director=<director>/')
def find_director(director):
    conn = sqlite3.connect('mpm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM {} WHERE UPPER({}) LIKE UPPER("%{}%")'.\
            format(tb_name, col_director, director))
    rows = c.fetchall()
    c.close()
    return jsonify(rows)

# endpoint to query by cast
# @app.route('/cast=<cast>/')
# def find_cast(cast):
    # need FIND_IN_SET alternative
#    pass

#    endpoint to query by rating
@app.route('/rating>=<rating>/')
def find_rating(rating):
    conn = sqlite3.connect('mpm.db')
    c = conn.cursor()
    c.execute('SELECT * FROM {} WHERE {}>="{}"'.\
            format(tb_name, col_imdb_rating, rating))
    rows = c.fetchall()
    c.close()
    return jsonify(rows)

if __name__=='__main__':
    app.run(debug=True, use_reloader=True)