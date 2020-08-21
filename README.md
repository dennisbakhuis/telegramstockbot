# Telegram Stock Alarm
A simple Python server to check specific stocks from the Dutch iex stock website.
Stocks to be checked are in the stocks.txt file. All is run from a Docker Container.

### Stocks.txt file
Currently only iex.nl pages are parsed but this can easily be extended. The stocks.txt
 has the following format:\
index, name, url, alarm\
2, aegon, https://www.iex.nl/Aandeel-Koers/11754/Aegon.aspx, 3.00

### Telegram token and chat-id:
The host environment should have the following environment variables or be set during
the creation of the docker instance (docker run -e TELEGRAMSTOCKBOT_...)\
- TELEGRAMSTOCKBOT_TOKEN
- TELEGRAMSTOCKBOT_CHATID

You can get a token from the @botfather bot in Telegram. Using the @userinfobot
you can get your own chatid. Before receiving messages, you need to open the chat
to your own bot.

### Docker build:
docker build -t stockbot .

### Docker run:
```
    docker run -d --rm \
    -e TELEGRAMSTOCKBOT_TOKEN \
    -e TELEGRAMSTOCKBOT_CHATID \
    stockbot
```
