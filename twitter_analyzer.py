from flask import Flask, render_template, request, redirect, make_response
from sentiment_analyzer import *
import requests
import json
import sqlite3
conn = sqlite3.connect("twitter.db")
conn.execute('CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT, username text not null, password text not null)');
conn.execute('CREATE TABLE IF NOT EXISTS tweet(id INTEGER PRIMARY KEY AUTOINCREMENT, body text not null, user_id INTEGER, FOREIGN KEY(user_id) REFERENCES user(id) )');
conn.commit()
conn.close()

with open('data/database.json', 'r') as f:
    database_tweets = json.load(f)
    print(database_tweets)

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/register',methods = ['POST', 'GET'])
def register():
    with sqlite3.connect("twitter.db") as conn:
        c = conn.cursor()
        if request.method == 'POST':
            new_username = request.form["input_username"]
            new_password = request.form["input_password"]
            c.execute("INSERT INTO user(username, password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()
            resp = make_response(redirect("/tweet_submit", code=302))
            resp.set_cookie('username', new_username)
            return resp 
        return render_template("register.html")

@app.route('/login',methods = ['POST', 'GET'])
def login():
    with sqlite3.connect("twitter.db") as conn:
        username = request.form["username"]
        password = request.form["password"]
        c = conn.cursor()
        c.execute("SELECT username,password from user WHERE username=? password=?", (username, password))
        return render_template("login.html")


@app.route('/tweet_submit',methods = ['POST', 'GET'])
def result():
    with sqlite3.connect("twitter.db") as conn:
        c = conn.cursor()
        name = request.cookies.get('username')
        if request.method == 'POST':
            tweety = request.form["input_tweet"]
            print(name)
            user_id = c.execute("SELECT user.id FROM user WHERE user.username=?",(name,)).fetchone()[0]
            print(user_id)
            c.execute("INSERT INTO tweet(body, user_id) VALUES (?, ?)", (tweety, user_id))
            conn.commit()
        database_tweets = list(map(lambda x: x, c.execute('SELECT * FROM tweet, user WHERE tweet.user_id=user.id AND user.username=?', (name,))))   
    return render_template("interactive_tweet.html", all_tweets=database_tweets)

@app.route('/twitter_analyzer')
def analyze_tweet():
    search_item = request.args.get('search_item')
    tweets = get_tweets(search_item)
    tweet_text = list(map(lambda x: x['text'], tweets))
    analysis = list(map(lambda x: (x,) + sentiment_analysis(x), tweet_text))
    return render_template('index.html', tweet_text=analysis)

def get_tweets(searchitem):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23{}&result_type=recent'.format(searchitem)
    headers = {'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAEpv%2FAAAAAAAPs2v4MSzKBYmvtZ40lydf7Q9d1w%3DAlXYCgFpawt3NvxbgEVMLu174P90rbrl47O7DTOEGSbrhuCUbA'}
    res = requests.get(url, headers=headers).json()
    return res['statuses']

if __name__ == '__main__':
	app.run()