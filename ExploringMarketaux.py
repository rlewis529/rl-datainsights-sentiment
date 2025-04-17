import requests

API_TOKEN = "null"

# API endpoint
url = "https://api.marketaux.com/v1/news/all"

# Query parameters
params = {
    "api_token": API_TOKEN,
    "symbols": "AAPL,MSFT,TSLA",   # comma-separated tickers
    "limit": 5,                    # number of articles to return
    "language": "en",
}

# Make the request
response = requests.get(url, params=params)
data = response.json()

# Print results
print("\n🔎 Latest Financial News:\n")
for article in data.get("data", []):
    print(f"📰 Title: {article['title']}")
    print(f"📅 Published: {article['published_at']}")
    print(f"🔗 Source: {article['source']}")
    print(f"📝 Summary: {article['description'][:200]}...\n")
