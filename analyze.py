import pandas as pd
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet as  wn
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
from collections import Counter, defaultdict
import regex as re
import string

import matplotlib.pyplot as plt
import seaborn as sns

from time import sleep
class Analyze:
    
    def __init__(self):
        print("Please don't forget to call exit.")
        self.c = Counter()
        self.f = open('tweets.txt','r',encoding='UTF-8')
        self.data = self.f.readlines()
        self.df = pd.DataFrame({'data':self.data})
        self.df = self.df.iloc[np.arange(0,self.df.shape[0]-1,2),:]
        
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
     
    def most_hashtag(self,n = 5):
        pat = re.compile('#[\w]*\s')
        for i in self.df['data']:
            for j in re.findall(pat, i):
                self.c[j] += 1

        print(self.c.most_common(n))
        
    def remove_stops(self,text):
        stops = nltk.corpus.stopwords.words('english') + list(string.punctuation)
        tokens = [i for i in text.split(" ") if i not in stops]
        return tokens
        
    def clean_words(self, text, retSent = True):
        
        translator = str.maketrans('','',string.punctuation)
        text = text.translate(translator)

        tokens = self.remove_stops(text)
    
        lemma = WordNetLemmatizer()
        tokens = [lemma.lemmatize(i,self.tag_map[j[0]]) for i,j in pos_tag(tokens)]

        return ' '.join(tokens) if retSent else tokens 
        
    def visualize(self):
        self.df['data'] = self.df.data.str.replace(r'@[\S]+',"",regex=True)
        self.df['data'] = self.df.data.str.replace(r'#[\S]+',"",regex=True)
        self.df['data'] = self.df.data.str.replace(r'[\s]+'," ",regex=True)
        self.df['data'] = self.df.data.str.replace(r'http[s]?:[\S]+',"",regex=True)
        self.df['data'] = self.df.data.map(lambda x:self.emoji_pattern.sub(r'',x))
        
        self.df['data'] = self.df.data.map(lambda x:self.clean_words(x))
        self.df['scores'] = self.df['data'].map(lambda x:self.sia.polarity_scores(x)['compound'])
        
        self.df['sentiment'] = np.where(self.df.scores >= 0,'positive','negative')
        self.df['sentiment'] = np.where(self.df.scores == 0,'neutral',self.df['sentiment'])
        self.df['scores'] = abs(self.df.scores)
        # print(self.df.head())
        sns.barplot(data = self.df,y='scores',x='sentiment',ci=None);
        plt.show()
     
        
    def exit(self):
        self.f.close()
