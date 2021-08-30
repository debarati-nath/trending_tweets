#import necessary library
import tweepy
import pandas as pd
import numpy as np
import os
import json

# Get the necessary API information (obtained from Twitter)
consumer_key="X"
consumer_key_secret = "XX"
access_token = "XXX"
access_token_secret = "XXXX"

# Authorization of Consumer Key and Consumer Secret
auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)

# Set Access to the User's Access Key and Access Secret
auth.set_access_token(access_token, access_token_secret)

# Calling the User's API
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# using any WOEID (Where On Earth IDentifier) for getting trending tweets
woeid = 23424977       #USA

# Fetching the Trends
trends = api.trends_place(id = woeid,lang='en')
for trend in trends[0]['trends']:
  print(trend['name'])    #print the name of the trends

# Loading the trends as json
trends = json.loads(json.dumps(trends, indent=1))

# Fetching the hashtags and print the hashtags
y1=[x['name'] for x in trends[0]['trends'] if x['name'].find('#') ==0]
print(y1)
y.extend(y1)
print(y)

#Print the tweets using the search name
y="EnoughIsEnough"
search_name=y
tweets=[]
for x in search_name:
    tweets = tweepy.Cursor(api.search, q=x, lang="en", result_type="recent").items(2)
    tweet_text=[]
    for tweet_text in tweets:
          tweet_text.append(tweet_text.text)
           print(tweet_text)

# Another way to get Tweets using search words and hashtags and save tweets as csv file

# Define any function to get tweets
def get_tweets(search, is_Hashtag):
    # Create a pandas DataFrame
    df_temp = pd.DataFrame(
        columns=["Content", "Location", "Username", "Retweet-Count", "Favorites", "Created at"])

    # Get the tweets
    tweets = tweepy.Cursor(api.search, q=search + " -filter:retweets", lang="en", since="2020-12-06",
                           tweet_mode='extended').items(100)

    # Iterate over tweets
    for tweet in tweets:
        content = tweet.full_text
        username = tweet.user.screen_name
        location = tweet.user.location
        created_at = tweet.created_at
        retweetcount = tweet.retweet_count
        favorites = tweet.favorite_count

        # Create a list consists of the features
        retrieved = [content, location, username, retweetcount, favorites, created_at]

        # Append list to the DataFrame
        df_temp.loc[len(df_temp)] = retrieved

    # Generate unique filename
    path = os.getcwd()

    # Generate a filename for hashtags or specific word in google drive
    if is_Hashtag:
        filename = path + '/drive/MyDrive/travel/' + search[1:] + '_hashtag.csv'
    else:
        filename = path + '/drive/MyDrive/travel/' + search.replace(" ", "") + '_wordsearch.csv'
    # Save the csv file
    df_temp.to_csv(filename)


# Call get_tweets function for each hashtag and search word

 for hashtag in hashtags:
   get_tweets(hashtag, is_Hashtag=True)

for search in search_list:
    get_tweets(search, is_Hashtag=False)

# Concatenate the DataFrames and load tweets from Google Drive

# Get csv file names in output directory or google drive
path = os.getcwd() + "/drive/MyDrive/folder_name/"
files = os.listdir(path)

# Create a list to store DataFrames
df_list = []

# Iterate over files in output dir and append DataFrames into df_list
for file in files:
    df = pd.read_csv(path + file, index_col=None)
    df_list.append(df)

# Create a DataFrame
name_dataframe_tweets = pd.concat(df_list, axis=0, ignore_index=True)

# Save the DataFrame as a csv file
name_dataframe_tweets.to_csv("specific_tweets.csv")




