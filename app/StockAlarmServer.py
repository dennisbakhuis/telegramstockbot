from os import environ
from time import time, sleep

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
error_msg_send = False
while True:
    errors = 0
    for ix, row in stocks.iterrows():
        try:
            stock_price = scrape_stock_price(row.url)
            message = f"{row['index']} - {row['name']} -=> €{stock_price:.3f} (alarm: €{row['alarm']:.3f})"
            print(message)  # for the log
            if stock_price >= row['above']:
                send(message, telegram_user_id, token)
            if stock_price <= row['below']:
                send(message, telegram_user_id, token)
        except:
            send('Error getting stock price...', telegram_user_id, token)
            errors += 1

    if errors >= 1 and not error_msg_send:
        send('Connection error...', telegram_user_id, token)
        error_msg_send = True
    if errors == 1 and error_msg_send:
        send('Connection restored...', telegram_user_id, token)
        error_msg_send = False

    sleep(wait_timer)


