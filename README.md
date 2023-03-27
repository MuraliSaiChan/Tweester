# Tweester - A real time tweet analyzer

This one is a little and simple sentiment analyzer of tweets. 

It generates real-time sentiment reports for a particular trend or group of trends. The report is a graph contains two subplots in it.
- one is a weighted sentiment ( positive or negative ). We used weighted to bring balance between no of tweets and the intensity of the sentiment.
- another one is a horizantal bar graph, which displays top 2-18 words that are being used in the trend in real time.

The process:

- We collect the twets in real-time using twitter api, Tweepy.
- Then we clean the text by removing unwanted characters, words, emojis etc..
- Then we applied lemmatization using wordnet lemmatizer from nltk.
- After cleaning the text we now generates the sentiment score for all newly added tweets using nltk's polarity_score method.
- Then we take only tweets that are non-neutral. We calculate the magnitude of score.
- Finally we plot the avg sentiments multiplied by their number, and top 2-18 words stored in collections.COunter.

For handling the speed of the data, we used two dataframes:
- master, in this we do less operations and to store all the data.
- df, this is a temporary data frame. When the new data comes in we take it into this df, we do all the nlp steps on it, at last
we concat it with the master. This will hep us handle the speed of streaming.

Working on further updates....!
[tweester1](https://user-images.githubusercontent.com/29299439/227946149-8d8c507c-c970-4692-bd2a-9b28c5fc389f.PNG)
