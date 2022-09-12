import requests
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"


## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
API_KEY = "VC24KCG2UMTKB3LH"
NEWS_KEY = "464691d8b11e4960afe4b06bb6c97496"
TWILIO_KEY = "AC6480ebb1b0ee62fd62d3bfe6a4b3a5d1"
TWILI_AUTH = "8835ca97fd8f3d6e1ce361fc297bdd79"
GET_NEWS = False
params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": API_KEY,
}
data = requests.get("https://www.alphavantage.co/query", params=params)
processed_data = data.json()["Time Series (Daily)"]

dataToList = [value for (key, value) in processed_data.items()]
yesterday = dataToList[0]
yesterday_closing_price = yesterday["4. close"]
print(yesterday_closing_price)

two_days_prior = dataToList[1]
two_days_prior_closing_price = two_days_prior["4. close"]
print(two_days_prior_closing_price)

percent_difference = (abs(float(yesterday_closing_price) - float(two_days_prior_closing_price))/ float(two_days_prior_closing_price))*100
print(percent_difference)

if percent_difference > 1:
    GET_NEWS = True

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 


if GET_NEWS == True:
    params_news = {
        "apiKey": "464691d8b11e4960afe4b06bb6c97496",
        "qIntitle": COMPANY_NAME,
    }
    news_data = requests.get("https://newsapi.org/v2/everything", params= params_news)
    first_three_articles = (news_data.json()["articles"][:3])
    print(first_three_articles)


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
    processed_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in first_three_articles]
    client = Client(TWILIO_KEY,TWILI_AUTH)
    for article in processed_articles:
        message = client.messages.create(
            body= article,
            from_="+16802083354",
            to="+15879172757",
        )

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

