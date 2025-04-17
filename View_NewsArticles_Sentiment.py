import sqlite3
from tabulate import tabulate

# Connect to the SQLite DB
conn = sqlite3.connect("news_sentiment.db")
cursor = conn.cursor()

# Run a basic query to get the 20 most recent articles
cursor.execute("""
    SELECT title, sentiment_label, sentiment_score, published_at, tickers, companies, source
    FROM NewsArticles
    ORDER BY published_at DESC
    LIMIT 20
""")

rows = cursor.fetchall()
conn.close()

# Print as a table
headers = ["Title", "Sentiment", "Score", "Published", "Tickers", "Companies", "Source"]
print(tabulate(rows, headers=headers, tablefmt="fancy_grid", maxcolwidths=[40, None, None, None, 20, 30, 10]))
