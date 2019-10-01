import os
import csv
import tweepy as tw
import pandas as pd
import sys

from twitter_config import *

DATA_DIR = 'data/'
NO_OF_TWEETS = 200

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

if len(sys.argv) < 2:
	print('Usage: python3 ' + sys.argv[0] + ' <Space separated list of keywords to search for>')

os.makedirs(DATA_DIR, exist_ok=True)

# Define the search term and the date_since date as variables
search_words = sys.argv[1:]
# ['Edinburgh Castle', 'edinburgh castle', 'EdinburghCastle']

columns = ['created_at', 'id_str', 'text', 'longitude', 'latitude']

for word in search_words:
	print('Searching for tweets containing ' + word)
	# Create open csv file to write data
	f = open(DATA_DIR + word.replace(' ', '-') + '.csv', 'w', encoding="utf-8")
	csv_file=csv.writer(f)
	csv_file.writerow(columns)


	# Collect tweets
	tweets = tw.Cursor(api.search,
		        q=search_words,
	            lang="en"
			  ).items(NO_OF_TWEETS)

	# Store in csv file
	for tweet in tweets:
		if tweet.coordinates != None:
		    longitude, latitude = tweet.coordinates["coordinates"]
		    csv_file.writerow([tweet.created_at, tweet.id_str, tweet.text, longitude, latitude])

