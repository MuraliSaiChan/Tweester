import pandas as pd
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet as  wn
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
from collections import  defaultdict
import regex as re
import string

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

from time import sleep

class Analyze:
    
    def __init__(self):
        print("Please don't forget to call exit.")
        self.master = pd.DataFrame({'data':[],'scores':[],'sentiment':[],'scores_updated':[]})
        self.df = None
        self.c = []
        # self.f = open('tweets.txt','r',encoding='UTF-8')
        # self.data = self.f.readlines()
        # self.df = pd.DataFrame({'data':self.data})
        # self.df = self.df.iloc[np.arange(0,self.df.shape[0]-1,2),:]
        self.pointer = 0
        
        self.tag_map = defaultdict(lambda : wn.NOUN)
        self.tag_map['J'] = wn.ADJ
        self.tag_map['V'] = wn.VERB
        self.tag_map['R'] = wn.ADV
        
        self.sia = SentimentIntensityAnalyzer()
        self.emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F" # emoticons
                           u"\U0001F300-\U0001F5FF" # symbols & pictographs
                           u"\U0001F680-\U0001F6FF" # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF" # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
        
        self.x = [1]
        self.y = [1]
        
        sns.set_style('darkgrid')
        # self.fig = plt.figure()
        # self.ax = self.fig.add_subplot(1,1,1)
        
    def read_new_data(self):
        with open('tweets.txt','r',encoding='UTF-8') as f:
            temp_df = pd.DataFrame({'data':f.readlines()[self.pointer:]})
            temp_df = temp_df.iloc[np.arange(0,temp_df.shape[0]-1,2),:]
        return temp_df
     
    # def most_hashtag(self,n = 5):
    #     pat = re.compile('#[\w]*\s')
    #     for i in self.df['data']:
    #         for j in re.findall(pat, i):
    #             self.c[j] += 1

    #     print(self.c.most_common(n))
        
    def remove_stops(self,text):
        stops = nltk.corpus.stopwords.words('english') + list(string.punctuation)
        tokens = [i for i in text.lower().split(" ") if i not in stops]
        return tokens
        
    def clean_words(self, text, retSent = True):
        
        translator = str.maketrans('','',string.punctuation)
        text = text.translate(translator)

        tokens = self.remove_stops(text)
    
        lemma = WordNetLemmatizer()
        tokens = [lemma.lemmatize(i,self.tag_map[j[0]]) for i,j in pos_tag(tokens)]

        return ' '.join(tokens) if retSent else tokens 
    
    
    def visualize_helper(self, r):
        self.df = self.read_new_data()
        # print(self.df.info())
        self.df['data'] = self.df.data.astype('string').str.replace(r'@[\S]+',"",regex=True)
        self.df['data'] = self.df.data.astype('string').str.replace(r'#[\S]+',"",regex=True)
        self.df['data'] = self.df.data.astype('string').str.replace(r'[\s]+'," ",regex=True)
        self.df['data'] = self.df.data.astype('string').str.replace(r'http[s]?:[\S]+',"",regex=True)
        self.df['data'] = self.df.data.astype('string').str.replace(r'[^\s\w]',"",regex=True)
        self.df['data'] = self.df.data.astype('string').map(lambda x:self.emoji_pattern.sub(r'',x))
        
        self.df['data'] = self.df.data.map(self.clean_words)
        self.df['scores'] = self.df['data'].map(lambda x:self.sia.polarity_scores(x)['compound'])
        
        self.df = self.df[self.df.scores != 0]
        self.df['sentiment'] = np.where(self.df.scores >= 0,'positive','negative')
        # self.df['sentiment'] = np.where(self.df.scores == 0,'neutral',self.df['sentiment'])
        self.df['scores'] = abs(self.df.scores)
        self.master = pd.concat([self.master,self.df])
        self.pointer = self.master.shape[0]
        
        b = self.master.sentiment.value_counts()
        
        try:
            self.master['scores_updated'] = (np.where(self.master.sentiment == 'negative',\
                                    self.master.scores*b.loc['negative'],\
                                    self.master.scores*b.loc['positive']))/self.pointer
        except KeyError:
            pass
            
        for i in self.df.data:
            self.c.extend(i.split())
        
        self.c1 = nltk.FreqDist(self.c).most_common(20)[2:-2]
        print(self.c1)
        self.x=[]
        self.y = []
        for i in self.c1:
            self.x.append(i[0])
            self.y.append(i[1])
        # print(x,y)
        # print(self.df.head())
        # plt.subplots(1,1,1)
        
        # plt.bar(x = self.master.sentiment, height = self.master.scores);
        t = self.master.groupby('sentiment').scores_updated.mean().map(lambda x:round(x,2)).reset_index()
        print(self.master.shape,t.values)
        
        try:
            self.ax1.clear()
            self.ax1.set_title('Total tweets processed : '+str(self.pointer))
            # self.ax1.bar(t.index.values, height = t.values,color=['r','g'])
            b = sns.barplot(data = t, x = 'sentiment', y = 'scores_updated', ax = self.ax1, palette = 'Blues_r')
            b.bar_label(b.containers[0])
            self.ax2.clear()
            sns.barplot(y=self.x, x = self.y,ax=self.ax2, palette = 'Blues_r')
        except ValueError:
            sleep(3)
            print("value error occured, please wait until the data is available.")
        
    def visualize(self):
        # while True:
        #     self.visualize_helper()
        #     sleep(2)
        self.fig = plt.figure(figsize=(10,10))
        self.ax1 = self.fig.add_subplot(1,2,1)
        
        self.ax2 = self.fig.add_subplot(1,2,2)
        self.ani = animation.FuncAnimation(self.fig, self.visualize_helper, interval = 3000)
        plt.show()

        
    def exit(self):
        del self.df
        del self.master

if __name__ == '__main__':
    a = Analyze()
    a.visualize()
