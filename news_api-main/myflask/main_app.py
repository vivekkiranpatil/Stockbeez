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
    mean_score = scores.mean()
    avg_sentiment = ""
    progress_color = ""
    if (mean_score>=-0.15 and mean_score<=0.15):
        avg_sentiment = "Neutral"
        progress_color = "bg-warning"
    elif (mean_score<=-0.15):
        avg_sentiment = "Negative"
        progress_color = "bg-danger"
    elif (mean_score>=0.15):
        avg_sentiment = "Positive"
        progress_color = "bg-success"
    percent_score = (mean_score+1)/2*100
    return render_template("headlines.html", length=length, headlines=headlines, links=links, percent_score=percent_score, progress_color=progress_color, avg_sentiment=avg_sentiment, colors=colors, truth=False)

@app.route('/stock_data')
def stock_data_route():
    get_stock_data()
    return redirect('glance.html')

@app.route('/analytic-tools')
def get_tools_page():
    return render_template('tools.html', ticker=None, name_co=None)

@app.route('/analytic-tools', methods=["POST"])
def get_tools():
    name_co = request.form['company_name']
    ticker = request.form['company_ticker']
    return render_template('tools.html', name_co=name_co, ticker=ticker, truth=False)

# fetched_news = get_news(ticker.lower())
    # news_articles = fetched_news[0]
    # formatted = fetched_news[1]
    # length = len(news_articles)

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
    mean_score = scores.mean()
    avg_sentiment = ""
    progress_color = ""
    if (mean_score>=-0.15 and mean_score<=0.15):
        avg_sentiment = "Neutral"
        progress_color = "bg-warning"
    elif (mean_score<=-0.15):
        avg_sentiment = "Negative"
        progress_color = "bg-danger"
    elif (mean_score>=0.15):
        avg_sentiment = "Positive"
        progress_color = "bg-success"
    percent_score = (mean_score+1)/2*100
    return render_template("headlines.html", length=length, headlines=headlines, links=links, percent_score=percent_score, progress_color=progress_color, avg_sentiment=avg_sentiment, colors=colors, truth=True)

@app.route('/glance', methods=['GET'])
def get_glance_data():
    df = pd.read_csv('/content/gdrive/My Drive/PPL Project/news_api-main/finviz.csv')
    length = len(df)
    Fticks = df['Ticker'].tolist()
    Flastp = df['Last Price'].tolist()
    Fchange = df['Change'].tolist()
    Fvolume = df['Volume'].tolist()
    Fsignal = df['Signal'].tolist()
    return render_template("glance.html", Fticks=Fticks, Flastp=Flastp, Fchange=Fchange, Fvolume=Fvolume,Fsignal=Fsignal, length=length)

@app.route('/glance', methods=['POST'])
def go_to_glance():
    get_stock_data()
    df = pd.read_csv('/content/gdrive/My Drive/PPL Project/news_api-main/finviz.csv')
    length = len(df)
    Fticks = df['Ticker'].tolist()
    Flastp = df['Last Price'].tolist()
    Fchange = df['Change'].tolist()
    Fvolume = df['Volume'].tolist()
    Fsignal = df['Signal'].tolist()
    return render_template("glance.html", Fticks=Fticks, Flastp=Flastp, Fchange=Fchange, Fvolume=Fvolume,Fsignal=Fsignal, length=length)

@app.route('/wordcloud')
def wordcloud_route():
    return render_template('wordcloud.html', truth=False)

@app.route('/wordcloud', methods=['POST'])
def wordcloud_sub():
    generate_wordcloud()
    return render_template('wordcloud.html', truth=True)

# # Active Change
# @app.route('/sentiment', methods=['GET', 'POST'])
# def get_sentiment_page():
#     if request.method=='GET':
#         return render_template('sentiment.html', truth=False)
#     elif request.method=='POST':
#         ticker = request.form['ticker']
#         generate_image(ticker)
#         url = f"images/{ticker}.png"
#         # Tweet Analysis
#         df = pd.DataFrame()
#         df = query(BEARER_TOKEN, ticker, df)
#         df = refine_df(tzone, df, ticker)
#         make_data(ticker, df)
#         url_tweet = f"images/{ticker}_tweet.png"
#         return render_template('sentiment.html', truth=True, url=url, url_tweet = url_tweet)
