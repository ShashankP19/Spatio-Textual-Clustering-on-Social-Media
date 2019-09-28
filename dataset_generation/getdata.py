import os
import csv
import tweepy as tw
import pandas as pd

# Edit this with your keys
consumer_key= "<CONSUMER_KEY>"
consumer_secret= "<CONSUMER_SECRET_KEY>"
access_token= "<ACCESS_TOKEN>"
access_token_secret= "<ACCESS_TOKEN_SECRET>"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


# Define the search term and the date_since date as variables
search_words = 'Hyde Park'
date_since = "2016-05-30"
date_until = "2019-09-26"

# Create open csv file to write data
f = open('collected_tweets.csv', 'w', encoding="utf-8")
csv_file=csv.writer(f)
columns = ['created_at', 'id_str', 'text', 'longitude', 'latitude']
csv_file.writerow(columns)


# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              lang="en",
              until=date_until,
              since=date_since).items(20)

# Store in csv file
for tweet in tweets:
    if tweet.coordinates != None:
        longitude, latitude = tweet.coordinates["coordinates"]
        csv_file.writerow([tweet.created_at, tweet.id_str, tweet.text, longitude, latitude])

    # else:
    #     longitude = 'None'
    #     latitude = 'None'
    
    # csv_file.writerow([tweet.created_at, tweet.id_str, tweet.text, longitude, latitude])

