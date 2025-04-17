import sqlite3
from tabulate import tabulate

# Connect to the SQLite DB
conn = sqlite3.connect("news_sentiment.db")
cursor = conn.cursor()

# Run the query
cursor.execute("""
    SELECT
        published_at,
        symbol,
        company_name,
        vader_sentiment,
        vader_label,
        marketaux_sentiment,
        article_title,
        article_source
    FROM ArticleEntitySentiment
    ORDER BY published_at DESC
    LIMIT 20
""")

rows = cursor.fetchall()
conn.close()

# Display results
headers = [
    "Date", "Symbol", "Company",
    "VADER Score", "VADER Label",
    "Marketaux Score", "Title", "Source"
]

if not rows:
    print("⚠️ No records found in the ArticleEntitySentiment table.")
else:
    print(tabulate(rows, headers=headers, tablefmt="fancy_grid", maxcolwidths=[None, None, 20, None, None, None, 40, 15]))
