import tweepy
from constants import *


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
        
class Stream:
    
    def __init__(self, search):        
        client = tweepy.Client(BEARER,API_KEY,API_SECRET,ACCESS_KEY,ACCESS_SECRET)

        auth = tweepy.OAuth1UserHandler(API_KEY,API_SECRET,ACCESS_KEY,ACCESS_SECRET)
        api = tweepy.API(auth)

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
    stream = Stream(['Indvsaus','indvaus'])
    stream.filter()        
    stream.disconnect()