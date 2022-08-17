from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
# import os
import pandas as pd
# import matplotlib.pyplot as plt
# NLTK VADER for sentiment analysis
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
# nltk.download('vader_lexicon')
vader = SentimentIntensityAnalyzer()

# Lemmatization Library
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()
# Lemmatization with POS tagging
from nltk.tokenize import word_tokenize

headlines = []
times = []
links = []

def MarketWatch(headlines, links):
    url = 'https://www.marketwatch.com/markets?mod=top_nav'
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)

    stories = html.findAll(class_="article__headline")
    count = 0
    for story in stories:
        anchors = story.find('a')
        headline = anchors.text
        link = anchors['href']
        headline = word_tokenize(headline)
        f_headline = ""
        if headline==[] or count==19 or count==20:
            pass
        else:
            for i in range(len(headline)):
                word = headline[i]
                if (i+1<len(headline)):
                    next = headline[i+1]
                if (next==',' or next=='.' or next=='!' or next=='?' or next==';' or next==':'):
                    f_headline+=f"{word}"
                else:
                    f_headline+=f"{word} "
                # print(count, f_headline)
            if (f_headline not in headlines):
                headlines.append(f_headline)
                links.append(link)
    count+=1

def MoneyControl(headlines, links):
    url = 'https://www.moneycontrol.com/news/business/stocks/'
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)

    stories = html.find(id="cagetory").findAll('li')
    count = 0
    ads = [4, 9, 14, 19, 24, 29, 34]
    for story in stories:
        if (count not in ads):
            anchors = story.find('a')
            if anchors:
                headline = anchors['title']
                link = anchors['href']
                headline = word_tokenize(headline)
                f_headline = ""
                for i in range(len(headline)):
                    word = headline[i]
                    if (i+1<len(headline)):
                        next = headline[i+1]
                    if (next==',' or next=='.' or next=='!' or next=='?' or next==';' or next==':'):
                        f_headline+=f"{word}"
                    else:
                        f_headline+=f"{word} "
                if (f_headline not in headlines):
                    headlines.append(f_headline)
                    links.append(link)
    count+=1

def Yahoo(headlines, links):
    url = 'https://finance.yahoo.com/'
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)

    stories = html.findAll(class_="js-content-viewer")

    headlines.append(stories[0].img['alt'])
    links.append(stories[0]['href'])

    headlines.append(stories[1].h2.text)
    links.append(stories[1]['href'])

    for i in range(2, 10):
        headline = stories[i].h3.text
        link = stories[i]['href']
        if (headline not in headlines):
            headlines.append(headline)
            links.append(link)
    # print(stories[i].h3.text)

    for i in range(10, len(stories)):
        headline = stories[i].text
        link = stories[i]['href']
        if (headline not in headlines):
            headlines.append(headline)
            links.append(link)
    # print(stories[i].text)

# len(headlines)

# RiverHeadline-headline, FeaturedCard-contentText, SecondaryCard-headline

def CNBC(headlines, links):
    url = 'https://www.cnbc.com/world/?region=world'
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)

    main = html.find(class_="FeaturedCard-contentText")
    sec = html.findAll(class_="SecondaryCard-headline")
    pri = html.findAll(class_="RiverHeadline-headline")

    if (main.a.text not in headlines):
        headlines.append(main.a.text)
        links.append(main.a['href'])

    for articles in sec:
        headline = articles.a.text
        link = articles.a['href']
        if (headline not in headlines):
            headlines.append(headline)
            links.append(link)

    for articles in pri:
        headline = articles.a.text
        link = articles.a['href']
        if (headline not in headlines):
            headlines.append(headline)
            links.append(link)

def LiveMint(headlines, links):
    url = 'https://www.livemint.com/market/stock-market-news'
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)
    main_link = 'https://www.livemint.com'

    stories = html.findAll(class_="headline")
    for story in stories:
        anchors = story.find('a')
        headline = anchors.text
        link = anchors['href']
        headline = word_tokenize(headline)
        f_headline = ""
        for i in range(len(headline)):
            word = headline[i]
            if (i+1<len(headline)):
                next = headline[i+1]
            if (next==',' or next=='.' or next=='!' or next=='?' or next==';' or next==':'):
                f_headline+=f"{word}"
            else:
                f_headline+=f"{word} "
        if (f_headline not in headlines):
            headlines.append(f_headline)
            links.append(link)

# len(headlines)

def EconomicTimes(headlines, links):
    url = 'https://economictimes.indiatimes.com/markets/stocks/news'
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)
    main_link = 'https://economictimes.indiatimes.com'

    stories = html.findAll(class_="eachStory")

    for story in stories:
        anchors = story.findAll('a')
        headline = anchors[1].text
        link = main_link+anchors[1]['href']
        if (headline not in headlines):
            headlines.append(headline)
            links.append(link)

# len(headlines)

def get_all_headlines(headlines, links):
    # MarketWatch(headlines, links)
    # MoneyControl(headlines, links)
    Yahoo(headlines, links)
    # CNBC(headlines, links)
    # LiveMint(headlines, links)
    # EconomicTimes(headlines, links)

def make_headlines_data(headlines, links):
    df = pd.DataFrame()
    # times = pd.Series(times)
    # df['Date and Time'] = times
    # print("---------------------Headlines---------------------")
    # print(headlines)
    df['Headline'] = headlines
    df['Links'] = links
    scores = df['Headline'].apply(vader.polarity_scores)
    scores_df = pd.DataFrame(scores.to_list())
    df = df.join(scores_df, rsuffix='_right')

    headlines_c = pd.DataFrame()

    headlines_c['Headline'] = df.iloc[df['compound'].sort_values(ascending=False).index]['Headline']
    headlines_c['Link'] = df.iloc[df['compound'].sort_values(ascending=False).index]['Links']
    headlines_c['Score'] = df.iloc[df['compound'].sort_values(ascending=False).index]['compound']
    headlines_c.reset_index(inplace=True)
    headlines_c.to_csv('headlines.csv', mode='w')
    # print(len(headlines_c))
    # print(len(headlines))

# for i in range(len(headlines_c)):
#   print(headlines_c.loc[i]['Headline'])
#   print(headlines_c.loc[i]['score'])
#   print()