from os import environ
from time import sleep

import bs4
import requests
import pandas as pd
import telegram

## Settings
wait_timer = 120  # wait 2 minutes to check stocks again
stocks = pd.read_csv('app/stocks.txt')

## Get Environment variables
token = environ.get('TELEGRAMSTOCKBOT_TOKEN')
telegram_user_id = environ.get('TELEGRAMSTOCKBOT_CHATID')

## Helper functions
def send(msg, chat_id, token):
    """
    Send a mensage to a telegram user
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)

def scrape_stock_price(url):
    """
    Scrape stock price from iex.nl.
    Example:
    scrape_stock_price('https://www.iex.nl/Aandeel-Koers/11754/Aegon.aspx')
    """
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, features="lxml")
    tagline = soup.find(name='span', attrs={'id': lambda x: x and 'LastPrice' in x and not 'Label' in x})
    price = float(tagline.contents[0].replace(',','.'))
    return price


## Main loop
send('Stock Alarm started...', telegram_user_id, token)
while True:
    for ix, row in stocks.iterrows():
        try:
            stock_price = scrape_stock_price(row.url)
            message = f"{row['index']} - {row['name']} -=> €{stock_price:.3f} (alarm: €{row['alarm']:.3f})"
            print(message)  # for the log
            if stock_price >= row['alarm']:
                send(message, telegram_user_id, token)
        except:
            send('Error getting stock price...', telegram_user_id, token)
    sleep(wait_timer)
