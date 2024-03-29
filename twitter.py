import tweepy
import pandas as pd 
import json
from datetime import datetime
import s3fs 

def run_twitter_etl():

    access_key = "" 
    access_secret = "" 
    consumer_key = ""
    consumer_secret = ""


   
    auth = tweepy.OAuthHandler(access_key, access_secret)   
    auth.set_access_token(consumer_key, consumer_secret) 

   
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='@elonmusk', 
                            
                            count=200,
                            include_rts = False,
                            tweet_mode = 'extended'
                            )

    list = []
    for tweet in tweets:
        text = tweet._json["full_text"]

        refined_tweet = {"user": tweet.user.screen_name,
                        'text' : text,
                        'favorite_count' : tweet.favorite_count,
                        'retweet_count' : tweet.retweet_count,
                        'created_at' : tweet.created_at}
        
        list.append(refined_tweet)

    df = pd.DataFrame(list)
    df.to_csv("s3://deveshbadolia08/df_new.csv",
          storage_options={'key': '<your_access_key_id>',
                           'secret': '<your_secret_access_key>'})
    print("Dataframe is saved as CSV in S3 bucket.")
