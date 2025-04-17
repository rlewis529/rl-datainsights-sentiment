import requests
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dataclasses import dataclass
from typing import List

# --- Marketaux API setup ---
API_TOKEN = "null"
url = "https://api.marketaux.com/v1/news/all"

params = {
    "api_token": API_TOKEN,
    "categories": "stocks",   # <-- use category instead of symbols
    "limit": 50,
    "language": "en"
}

# --- Dataclass to hold result ---
@dataclass
class ArticleSentiment:
    title: str
    description: str
    source: str
    published_at: str
    url: str
    tickers: List[str]
    companies: List[str]
    sentiment_score: float
    sentiment_label: str

# --- Sentiment analyzer setup ---
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text: str) -> tuple[float, str]:
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
articles: List[ArticleSentiment] = []

for article in data.get("data", []):
    title = article['title']
    desc = article.get('description', '')
    full_text = f"{title} {desc}"
    score, label = get_sentiment(full_text)

    # Try to get tickers/companies if they exist (optional fallback)
    tickers = article.get("tickers", [])
    companies = [s.get("name", "") for s in article.get("symbols", [])]

    article_obj = ArticleSentiment(
        title=title,
        description=desc,
        source=article.get("source", ""),
        published_at=article.get("published_at", ""),
        url=article.get("url", ""),
        tickers=tickers,
        companies=companies,
        sentiment_score=score,
        sentiment_label=label
    )

    articles.append(article_obj)

# --- Create SQLite database and table ---
conn = sqlite3.connect("news_sentiment.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS NewsArticles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    source TEXT,
    published_at TEXT,
    url TEXT,
    tickers TEXT,
    companies TEXT,
    sentiment_score REAL,
    sentiment_label TEXT
)
""")
conn.commit()

# --- Insert articles into DB ---
for article in articles:
    cursor.execute("""
        INSERT INTO NewsArticles (
            title, description, source, published_at, url,
            tickers, companies, sentiment_score, sentiment_label
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        article.title,
        article.description,
        article.source,
        article.published_at,
        article.url,
        ",".join(article.tickers),
        ",".join(article.companies),
        article.sentiment_score,
        article.sentiment_label
    ))

conn.commit()
conn.close()
print(f"✅ {len(articles)} articles written to 'news_sentiment.db'")
