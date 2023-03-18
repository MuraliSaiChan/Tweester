# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 22:56:30 2023

@author: hp
"""

import tweepy
from constants import *
import time

client = tweepy.Client(BEARER,API_KEY,API_SECRET,ACCESS_KEY,ACCESS_SECRET)

auth = tweepy.OAuth1UserHandler(API_KEY,API_SECRET,ACCESS_KEY,ACCESS_SECRET)
api = tweepy.API(auth)

search = ['NTR']

class MyStream(tweepy.StreamingClient):
    def on_connect(self):
        print("Connected")
        self.f = open('tweets.txt','w',encoding='UTF-8')
        
    def on_tweet(self, tweet):
        if tweet.referenced_tweets == None:
            self.f.write(tweet.text)
    
    def on_disconnect(self):
        rules = self.get_rules()
        for i in rules[0]:
            self.delete_rules([i[2]])
        self.f.close()
    
stream = MyStream(BEARER)            
for i in search:
    print("rules:",stream.get_rules())
    stream.add_rules(tweepy.StreamRule(i))
    # stream.disconnect()

stream.filter()
stream.disconnect()