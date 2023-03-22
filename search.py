import tweepy
from constants import *
import json
import pandas as pd


class MyStream(tweepy.StreamingClient):
    def on_connect(self):
        print("Connected")
        self.f = open('tweets.txt','w',encoding='UTF-8')
        
    def on_tweet(self, tweet):
        if tweet.referenced_tweets is None and tweet.lang == 'en':
            self.f.write(tweet.text)
            # print(tweet.data)
    
    def on_disconnect(self):
        rules = self.get_rules()
        for i in rules[0]:
            self.delete_rules([i[2]])
        self.f.close()
        print('disconnected')
        
class Stream:
    
    def __init__(self, search):        
        client = tweepy.Client(BEARER,API_KEY,API_SECRET,ACCESS_KEY,ACCESS_SECRET)

        auth = tweepy.OAuth1UserHandler(API_KEY,API_SECRET,ACCESS_KEY,ACCESS_SECRET)
        api = tweepy.API(auth)
        # self.latlong = pd.read_json('latlong.json')
        # self.latlong['city'] = self.latlong.city.str.lower()
        # self.latlong['nation'] = self.latlong.nation.str.lower()
        # temp = self.latlong[self.latlong.city.str.contains('hyderabad')].iloc[1,2:]
        woeid = api.closest_trends(lat = temp[0], long = temp[1])[0]['woeid']
        print(api.get_place_trends(woeid))
        
        self.search = search
    
        self.stream = MyStream(BEARER)            
        for i in self.search:
            print("rules:",self.stream.get_rules())
            self.stream.add_rules(tweepy.StreamRule(i))
    # stream.disconnect()
    
    def filter(self):
        self.stream.filter()
    
    def disconnect(self):    
        self.stream.disconnect()
        
if __name__ == '__main__':
    stream = Stream(['indvsaus','rohit','gill'])
    stream.filter()        
    stream.disconnect()