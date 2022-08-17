from myflask import main_app
from flask import render_template
from .utils import get_news
from .headlines import *
from .stock_data import get_stock_data
import pandas as pd

app = main_app

@app.route('/')
def hello():
    user = {'name': "Vladimir"}
    return render_template("index.html", user=user)

@app.route('/headlines')
def headlines_route():
    headlines = []
    get_all_headlines(headlines)
    make_headlines_data(headlines)
    df = pd.read_csv('headlines.csv')
    headlines = df['Headline']
    links = df['Link']
    scores = df['Score']
    length = len(headlines)
    colors = []
    for i in range(length):
        if (scores[i]>0):
            colors.append('green')
        elif (scores[i]<0):
            colors.append('red')
        else:
            colors.append('yellow')
    return render_template("headlines.html", length=length, headlines=headlines, links=links, colors=colors)

@app.route('/stock_data')
def stock_data_route():
    get_stock_data()
    return "Successful"

@app.route('/news')
def news_headlines():
    fetched_news = get_news()
    news_articles  =fetched_news[0]
    formatted = fetched_news[1]
    length = len(news_articles)
    return render_template('news.html', news_articles=news_articles, formatted=formatted, length=length)

