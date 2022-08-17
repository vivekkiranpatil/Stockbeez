from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import os
import pandas as pd

def Finviz():

    url = 'https://finviz.com'

    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)
    main_link = 'https://finviz.com/'
    # Find id 'news-table'
    signal_table = html.find(id='signals_1')
    # Add the table to our dictionary
    signals_table = signal_table

    signals = []
    tickers = []
    links = []
    lasts = []
    changes = []
    volumes = []
    for i, table_row in enumerate(signals_table.findAll('tr')[1:]):
        table_data = table_row.findAll('td')
        ticker = table_data[0].text
        link = main_link+table_data[0].a['href']
        last = table_data[1].text
        change = table_data[2].text
        volume = table_data[3].text
        signal = table_data[-1].text
        # print(ticker)
        # print(signal)
        signals.append(signal)
        tickers.append(ticker)
        links.append(link)
        lasts.append(last)
        changes.append(change)
        volumes.append(volume)

    df = pd.DataFrame()

    signal_table = html.find(id='signals_2')
    # Add the table to our dictionary
    signals_table = signal_table
    for i, table_row in enumerate(signals_table.findAll('tr')[1:]):
        table_data = table_row.findAll('td')
        ticker = table_data[0].text
        link = main_link+table_data[0].a['href']
        last = table_data[1].text
        change = table_data[2].text
        volume = table_data[3].text
        signal = table_data[-1].text
        # print(ticker)
        # print(signal)
        signals.append(signal)
        tickers.append(ticker)
        links.append(link)
        lasts.append(last)
        changes.append(change)
        volumes.append(volume)

    df['Ticker'] = tickers
    df['Last Price'] = lasts
    df['Change'] = changes
    df['Volume'] = volumes
    df['Signal'] = signals
    df['Link'] = links

    major_news = html.find(id='major-news')
    major_news_body = major_news.parent

    major_news_tickers = []
    major_news_changes = []
    for i, table_row in enumerate(major_news_body.findAll('tr')[1:]):
        table_data = table_row.findAll('td')
        ticker = table_data[0].text
        change = table_data[1].text
        # print(ticker)
        # print(p)
        major_news_tickers.append(ticker)
        major_news_changes.append(change)
    
    df.to_csv('finviz.csv', mode='w')

def MoneyControlStock():
    url = 'https://www.moneycontrol.com/stocks/marketstats/nsegainer/index.php'
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)
    table = html.find_all('table')
    tbody = table[1].find('tbody')
    parent_node = tbody
    trs = parent_node.findChildren("tr", recursive=False)
    tds = trs[0].find_all("td")

    companies = {}

    signal = 'Top Gainers'

    for company in trs:
        tds = company.find_all("td")
        last = tds[3].text
        change = tds[6].text
        link = company.td.a['href']
        companies[company.td.a.text] = [last, change, [signal], link]
    # print(company.td.a['href'], end=" ")
    # print(company.td.a.text, end=" ")
    # print(tds[6].text, end=" ")
    # print(tds[4].text, end=" ")
    # print(tds[3].text)

    url = 'https://www.moneycontrol.com/stocks/marketstats/nseloser/index.php'
    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)
    table = html.find_all('table')
    tbody = table[1].find('tbody')
    parent_node = tbody
    trs = parent_node.findChildren("tr", recursive=False)

    signal = 'Top Losers'

    for company in trs:
        tds = company.find_all("td")
        name = company.td.a.text
        if (name in companies.keys()):
            signal_c = companies[name][2]
            signal_c.append(signal)
            companies[company.td.a.text][2] = signal_c
        else:
            last = tds[3].text
            change = tds[6].text
            link = company.td.a['href']
            signal_c = [signal]
            companies[company.td.a.text] = [last, change, signal_c, link]

    url = 'https://www.moneycontrol.com/stocks/marketstats/nsemact1/index.php'

    req = Request(url=url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0'}) 
    response = urlopen(req)
    html = BeautifulSoup(response)

    table = html.find_all('table')

    tbody = table[1].find('tbody')

    parent_node = tbody

    trs = parent_node.findChildren("tr", recursive=False)

    signal = 'Most Active'

    for company in trs:
        tds = company.find_all("td")
        name = company.td.a.text
        if (name in companies.keys()):
            signal_c = companies[name][2]
            signal_c.append(signal)
            companies[name][2] = signal_c
        else:
            last = tds[3].tex
            change = tds[4].text
            link = company.td.a['href']
            signal_c = [signal]
            companies[name] = [last, change, signal_c, link]

    names = []
    lasts = []
    changes = []
    links = []
    signals = []

    for name, info in companies.items():
        names.append(name)
        lasts.append(info[0])
        changes.append(info[1])
        signals.append(info[2])
        links.append(info[3])

    df = pd.DataFrame()

    df['Name'] = names
    df['Signal'] = signals
    df['Last Price'] = lasts
    df['Gain %'] = changes
    df['Link'] = links

    df.to_csv('moneycontrol.csv', mode='w')

def get_stock_data():
    Finviz()
    MoneyControlStock()
