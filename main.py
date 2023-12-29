import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "YOUR OWN API KEY"
NEWS_API_KEY = "YOUR OWN API KEY"

account_sid = "AC6309db348a2684b3871aa244dec988e2"
auth_token = "YOUR OWN API KEY"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,

}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

yesterday_close = data_list[0]["4. close"]
before_yesterday_close = data_list[1]["4. close"]

differance = float(yesterday_close) - float(before_yesterday_close)
up_down = None
if differance > 0:
    up_down = "🔼"
else:
    up_down = "🔽"

differance = abs(differance)
diff_percentage = round((differance / float(yesterday_close)) * 100)
print(diff_percentage)
if diff_percentage > 5:
    # print("Get News")

    news_parameters = {
        "q": COMPANY_NAME,
        "apiKey": NEWS_API_KEY,

    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_data = news_response.json()
    articles = news_data["articles"][:3]
    # print(articles[0]["title"])

    headlines = [f"{STOCK_NAME}: {up_down}{diff_percentage}%\nHeadline:  {article['title']}. \nBrief: {article['description']}"for article in articles]

    for headline in headlines:
        client = Client(account_sid, auth_token)
        client.messages.create(
            body=headline,
            from_="+18304606243",
            to="+966561388722"
        )

