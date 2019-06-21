from flask import Flask, render_template, request
from sentiment_analyzer import *
import requests
import json

with open('data/database.json', 'r') as f:
    database_tweets = json.load(f)
    print(database_tweets)

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/tweet_submit',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        tweet = request.form["input_tweet"]
        name = request.form["input_username"]
        if name not in database_tweets:
            database_tweets[name] = []
        database_tweets[name].append(tweet)

        with open('data/database.json', 'w+') as g:
            json.dump(database_tweets, g)
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