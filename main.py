from flask import Flask, url_for, render_template, request, g, jsonify
import sqlite3
from datetime import datetime
import base64

app = Flask(__name__)
DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def create_database():
    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS TOPIC (id INTEGER PRIMARY KEY AUTOINCREMENT, date_time TEXT, title TEXT, body TEXT, name TEXT, username TEXT DEFAULT NULL)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS MUSIC (id INTEGER PRIMARY KEY AUTOINCREMENT, date_time TEXT, abouts TEXT, music BLOB, name TEXT, username TEXT DEFAULT NULL)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS FINDFIREND (id INTEGER PRIMARY KEY AUTOINCREMENT, date_time TEXT, body TEXT, name TEXT, username TEXT DEFAULT NULL)""")
        db.commit()
        db.close()


@app.route('/set-topic', methods=['post'])
def get_topic():
    with app.app_context():
        try:
            username = request.form.get('username')
            name = request.form.get('name')
            title = request.form.get('title')
            body = request.form.get('body')
            now = datetime.now().strftime('%m/%d/%Y - %H:%M:%S')
            db = get_db()
            cur = db.cursor()
            cur.execute('''INSERT INTO TOPIC (date_time, title, body, name, username) VALUES (?,?,?,?,?)''', (now, title, body, name, username))
            db.commit()
            db.close()
            return jsonify({'result': 'Success'})
        except Exception:
            return jsonify({'result': 'Failed'})


@app.route('/send-music', methods=['post'])
def get_music():
    with app.app_context():
        try:
            username = request.form.get('username')
            name = request.form.get('name')
            abouts = request.form.get('about')
            music_ = request.files.get('music')
            now = datetime.now().strftime('%m/%d/%Y - %H:%M:%S')
            db = get_db()
            cur = db.cursor()
            cur.execute('''INSERT INTO MUSIC (date_time, abouts, music, name, username) VALUES (?,?,?,?,?)''', (now, abouts, music_.read(), name, username))
            db.commit()
            db.close()
            return jsonify({'result': 'Success'})
        except Exception as e:
            print(e)
            return jsonify({'result': 'Failed'})


@app.route('/send-firend', methods=['post'])
def get_firend():
    with app.app_context():
        try:
            username = request.form.get('username')
            name = request.form.get('name')
            body = request.form.get('body')
            now = datetime.now().strftime('%m/%d/%Y - %H:%M:%S')
            db = get_db()
            cur = db.cursor()
            cur.execute('''INSERT INTO FINDFIREND (date_time, body, name, username) VALUES (?,?,?,?)''', (now, body, name, username))
            db.commit()
            db.close()
            return jsonify({'result': 'Success'})
        except Exception:
            return jsonify({'result': 'Failed'})


@app.route('/')
def home():
    about_url = url_for('about')
    peopole_says = url_for('content')
    music_url = url_for('music')
    find_firend_url = url_for('find_firend')
    return render_template('index.html', about_url=about_url, peopole_says_url=peopole_says, music_url=music_url, find_firend_url=find_firend_url)


@app.route('/about')
def about():
    peopole_says = url_for('content')
    home_url = url_for('home')
    music_url = url_for('music')
    find_firend_url = url_for('find_firend')
    return render_template('about.html', home_url=home_url, peopole_says_url=peopole_says, music_url=music_url, find_firend_url=find_firend_url)


@app.errorhandler(404)
def error404(error):
    home_url = url_for('home')
    return render_template('404error.html', home_url=home_url, error=error), 404


@app.route('/people_says')
def content():
    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM TOPIC ORDER BY id DESC')
        all_topic = cur.fetchall()
        db.close()
    home_url = url_for('home')
    about_url = url_for('about')
    music_url = url_for('music')
    find_firend_url = url_for('find_firend')
    return render_template('content.html', find_firend_url=find_firend_url, home_url=home_url, about_url=about_url, music_url=music_url, all_topic=all_topic)


@app.route('/music')
def music():
    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM MUSIC ORDER BY id DESC')
        all_music = cur.fetchall()
        db.close()
    musics = [(base64.b64encode(mus[3]).decode('utf-8'), mus[1], mus[2], mus[4], mus[5]) for mus in all_music]
    home_url = url_for('home')
    about_url = url_for('about')
    people_says_url = url_for('content')
    find_firend_url = url_for('find_firend')
    return render_template('music.html', find_firend_url=find_firend_url, home_url=home_url, about_url=about_url, people_says_url=people_says_url, music=musics)


@app.route('/find-firend')
def find_firend():
    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM FINDFIREND ORDER BY id DESC')
        all_topic = cur.fetchall()
        db.close()
    home_url = url_for('home')
    about_url = url_for('about')
    music_url = url_for('music')
    people_says_url = url_for('content')
    return render_template('find_firend.html', home_url=home_url, about_url=about_url, music_url=music_url, all_topic=all_topic, people_says_url=people_says_url)


create_database()
if __name__ == '__main__':
    app.run(debug=True)
