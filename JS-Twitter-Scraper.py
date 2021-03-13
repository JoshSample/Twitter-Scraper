# Imports
import tweepy
import pandas as pd
import time
from configparser import ConfigParser

# read ini file for keys
read_config = ConfigParser()
read_config.read("config.ini")

# define keys
consumer_key = read_config.get("Key", "consumer_key")
consumer_secret = read_config.get("Key", "consumer_secret")
access_token = read_config.get("Key", "access_token")
access_token_secret = read_config.get("Key", "access_token_secret")

# authorize Tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)


# Scrape a users tweets
def username_tweets_to_csv(username,count):
    tweets = []
    try: 
    # Pulling individual tweets from query
        for tweet in api.user_timeline(id=username, count=count):

            # Adding to list that contains all tweets
            tweets.append((tweet.created_at,tweet.id,tweet.text))

            # Creation of dataframe from tweets list
            tweetsdf = pd.DataFrame(tweets,columns=['Datetime', 'Tweet Id', 'Text'])

            # Converting dataframe to CSV
            tweetsdf.to_csv('{}-tweets.csv'.format(username)) 

    except BaseException as e:
          print('failed on_status,',str(e))
          time.sleep(3)

# Scrape tweets from keyword
def text_query_to_csv(text_query,count):
    tweets = []
    try:
    # Pulling individual tweets from query
        for tweet in api.search(q=text_query, count=count):

          # Adding to list that contains all tweets
          tweets.append((tweet.created_at,tweet.id,tweet.text))

          # Creation of dataframe from tweets list
          tweetsdf = pd.DataFrame(tweets,columns=['Datetime', 'Tweet Id', 'Text'])

          # Converting dataframe to CSV
          tweetsdf.to_csv('{}-tweets.csv'.format(text_query)) 

    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)
    

  
def main():
    username = 'POTUS'    # a persons @
    text_query = 'COVID-19'     # the keywords you want to look for
    count = 100          # count = most recent tweets you want to scrape
    
    # scrape tweets from user
    username_tweets_to_csv(username, count)
    # scrape tweets from text
    text_query_to_csv(text_query,count)
if __name__ == "__main__":
    main()
    