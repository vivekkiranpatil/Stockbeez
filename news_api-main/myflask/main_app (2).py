from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
# from config import Config
from flask import render_template

from myflask.wordcloud import generate_wordcloud
from .utils import get_news
from .headlines import *
from .stock_data import get_stock_data
from .sentiment import generate_image
import pandas as pd

app = Flask(__name__)
# app.config.from_object(Config)

@app.route('/')
def hello():
    return render_template("home.html")

@app.route('/headlines')
def headlines_route():
    headlines = []
    links = []
    get_all_headlines(headlines, links)
    make_headlines_data(headlines, links)
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
    return render_template("headlines.html", length=length, headlines=headlines, links=links, colors=colors, truth=False)

@app.route('/stock_data')
def stock_data_route():
    get_stock_data()
    return "Successful"

@app.route('/news')
def news_headlines():
    return render_template('news.html', news_articles=None, formatted=None, length=None, name=None)

@app.route('/headlines', methods=['POST'])
def news_wordcloud():
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
    generate_wordcloud()
    return render_template("headlines.html", length=length, headlines=headlines, links=links, colors=colors, truth=True)

@app.route('/news', methods=["POST"])
def get_news_query():
    name = request.form['company_name']
    fetched_news = get_news(name)
    news_articles = fetched_news[0]
    formatted = fetched_news[1]
    length = len(news_articles)
    return render_template('news.html', news_articles=news_articles, formatted=formatted, length=length, name=name, truth=False)

@app.route('/wordcloud')
def wordcloud_route():
    return render_template('wordcloud.html', truth=False)

@app.route('/wordcloud', methods=['POST'])
def wordcloud_sub():
    generate_wordcloud()
    return render_template('wordcloud.html', truth=True)
