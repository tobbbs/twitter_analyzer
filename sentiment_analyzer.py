import csv

def open_csv(x):
	tweets = []
	with open(x, 'r') as d:
		reader = csv.DictReader(d)
		for row in reader:
			tweets.append(row['SentimentText'])
	return tweets

def open_program(x):
	with open(x, 'r') as f:
		return set(f.read().splitlines())

def clean_tweet(tweet):
	remove = '!@#$%^&*'
	for char in remove:
		tweet = tweet.replace(char, '')
	tweet = tweet.lower().strip()
	return tweet

def sentiment_count_within_tweet(split_tweet, sentiment_words):
	count = 0
	for word in split_tweet:
		if word in sentiment_words:
			count += 1 
	return count

def total_sentiment_count(total, sentiment):
	return 'The total %s is %d ' % (sentiment, total) 

def sentiment_analysis(comment):
	negative_words = open_program('data/negative.txt')
	positive_words = open_program('data/positive.txt')

	total_positive = 0
	total_negative = 0

	comment = clean_tweet(comment)
	split_tweet = comment.split(" ")

	positive_count = sentiment_count_within_tweet(split_tweet, positive_words)
	negative_count = sentiment_count_within_tweet(split_tweet, negative_words)

	return positive_count, negative_count
