import requests
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dataclasses import dataclass
from typing import List
from datetime import datetime

# --- Marketaux API setup ---
API_TOKEN = "null"
url = "https://api.marketaux.com/v1/news/all"

params = {
    "api_token": API_TOKEN,
    "symbols": "AAPL,MSFT,TSLA,GOOG,AMZN,META,NVDA",
    "limit": 3,  # Adjust based on your plan
    "language": "en"
}

# --- Dataclass to hold article-entity relationship ---
@dataclass
class ArticleEntitySentiment:
    article_title: str
    article_description: str
    article_url: str
    article_source: str
    published_at: str
    symbol: str
    company_name: str
    marketaux_sentiment: float
    vader_sentiment: float
    vader_label: str

# --- Sentiment analyzer setup ---
analyzer = SentimentIntensityAnalyzer()

def get_vader_sentiment(text: str) -> tuple[float, str]:
    score = analyzer.polarity_scores(text)['compound']
    label = (
        "Positive" if score >= 0.05 else
        "Negative" if score <= -0.05 else
        "Neutral"
    )
    return score, label

# --- Fetch and process articles ---
response = requests.get(url, params=params)
data = response.json()

print(f"🔢 Articles returned: {len(data.get('data', []))}")
print(f"⚠️ Warnings: {data.get('warnings')}")

entries: List[ArticleEntitySentiment] = []

for article in data.get("data", []):
    title = article.get('title', '')
    desc = article.get('description', '')
    source = article.get('source', '')
    url_ = article.get('url', '')
    published_at = article.get('published_at', '')
    full_text = f"{title} {desc}"
    
    vader_score, vader_label = get_vader_sentiment(full_text)

    for entity in article.get("entities", []):
        symbol = entity.get("symbol")
        name = entity.get("name")
        sentiment_score = entity.get("sentiment_score")

        if not symbol or not name:
            continue  # Skip incomplete entries

        entry = ArticleEntitySentiment(
            article_title=title,
            article_description=desc,
            article_url=url_,
            article_source=source,
            published_at=published_at,
            symbol=symbol,
            company_name=name,
            marketaux_sentiment=sentiment_score,
            vader_sentiment=vader_score,
            vader_label=vader_label
        )

        entries.append(entry)

# --- Create SQLite database and table ---
conn = sqlite3.connect("news_sentiment.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ArticleEntitySentiment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    article_title TEXT,
    article_description TEXT,
    article_url TEXT,
    article_source TEXT,
    published_at TEXT,
    symbol TEXT,
    company_name TEXT,
    marketaux_sentiment REAL,
    vader_sentiment REAL,
    vader_label TEXT
)
""")
conn.commit()

# --- Insert into DB ---
for entry in entries:
    cursor.execute("""
        INSERT INTO ArticleEntitySentiment (
            article_title, article_description, article_url, article_source,
            published_at, symbol, company_name,
            marketaux_sentiment, vader_sentiment, vader_label
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry.article_title,
        entry.article_description,
        entry.article_url,
        entry.article_source,
        entry.published_at,
        entry.symbol,
        entry.company_name,
        entry.marketaux_sentiment,
        entry.vader_sentiment,
        entry.vader_label
    ))

conn.commit()
conn.close()

print(f"✅ Inserted {len(entries)} entity-sentiment records into 'news_sentiment.db'")
