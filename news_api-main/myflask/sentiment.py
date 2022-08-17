import plotly.express as px
import yfinance as yf
import os
import json
import pandas as pd

# import requests
# from decouple import config
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# vader = SentimentIntensityAnalyzer()

def get_yf_data(ticker):
    DATA_PATH = f"/content/gdrive/My Drive/PPL Project/news_api-main/myflask/static/data/{ticker}.json"

    if os.path.isfile(DATA_PATH):
        # Read from file if we've already downloaded the data.
        with open(DATA_PATH) as f:
            hist = pd.read_json(DATA_PATH)
    else:
        tick = yf.Ticker(f"{ticker.upper()}")
        hist = tick.history(period="10y")
        hist.reset_index(inplace=True)

        # Save file to json in case we need it later.  This prevents us from having to re-download it every time.
        hist.to_json(DATA_PATH)
    return hist

def generate_image(ticker):
    # os path exists?
    hist = get_yf_data(ticker)
    STATIC = '/content/gdrive/My Drive/PPL Project/news_api-main/myflask/static/images'
    fig = px.line(hist, x="Date", y="Close", title=f'{ticker.upper()} Stock Prices')
    path = f"{STATIC}/{ticker}.png"
    fig.write_image(path)
