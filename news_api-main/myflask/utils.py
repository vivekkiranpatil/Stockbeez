import requests
from decouple import config
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
vader = SentimentIntensityAnalyzer()

NEWS_API_KEY = config('NEWS_API_KEY')

def get_news(topic):
    global vader
    df = pd.DataFrame()
    print("Topic: ", topic)
    news_data = requests.get(f'https://newsapi.org/v2/everything?q={topic}&apiKey={NEWS_API_KEY}&pageSize=20&lang=en').json()
    headlines = []
    print(news_data)
    for article in news_data['articles']:
        headlines.append(article['title'])
    df['Headline'] = headlines
    scores = df['Headline'].apply(vader.polarity_scores)
    scores_df = pd.DataFrame(scores.to_list())
    df = df.join(scores_df, rsuffix='_right')
    headlines_c = pd.DataFrame()
    headlines_c['Headline'] = df.iloc[df['compound'].sort_values(ascending=False).index]['Headline']
    # headlines_c['links'] = df.iloc[df['compound'].sort_values(ascending=False).index]['Links']
    headlines_c['score'] = df.iloc[df['compound'].sort_values(ascending=False).index]['compound']
    headlines_c.reset_index(inplace=True)
    formatted = {}
    for i in range(len(headlines_c)):
        score = headlines_c.loc[i]['score']
        headline = headlines_c.loc[i]['Headline']
        if (score>0):
            formatted[i] = [headline, 'green']
        elif (score==0):
            formatted[i] = [headline, 'yellow']
        else:
            formatted[i] = [headline, 'red']

    # for i in range(len(headlines_c)):
    #     print(headlines_c.loc[i]['Headline'])
    #     print(headlines_c.loc[i]['score'])
    #     print()
    
    return news_data['articles'], formatted
