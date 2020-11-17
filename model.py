from tweepy import OAuthHandler
from tweepy.streaming import StreamListener, Stream
import tweepy
import pandas as pd

api_key = "6KhSV0cD8hVwsIgVvNkO3Ey4u"
api_secret = "V6PoemcmnLh7KZlijAVqHvUkKZXPl9H1B6lpN1iibkQFoLvwiJ"
access_key = "1328537149264728070-gHBH3jn6IL3fDQlgPwXFpD0IJsKAoY"
access_secret = "QG9vVtw1kXmJAO8316wuyoURAD4RK8yjZovqRmkqbmI5g"

auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def get_tweets():
    geosearch = api.search(q="ducey -filter:retweets AND -filter:links",geocode="33.574450,-112.156970,150mi", tweet_mode="extended")
    nearme = []
    for x in geosearch:
        # data = {
        #     'author':  x.author.screen_name,
        #     'followers': x.author.followers_count,
        #     'text': x.full_text,
        #     'favorited': x.favorited,
        #     'fav_count' : x.favorite_count,
        #     'retweet_count': x.retweet_count,
        #     'retweeted': x.retweeted,
        #     'created_at': x.created_at,
        #    }
        # nearme.append(data)
        if len(x.full_text) > 120:
            pass
        else:
            try:
                api.retweet(x.id)
            except:
                pass