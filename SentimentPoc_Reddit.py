import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

client_id = "null"
client_secret = "null"
user_agent = "SentimentPoc/0.1 by burritonite"

# Set up Reddit API client
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Fetch top 10 hot posts from r/investing
subreddit = reddit.subreddit("investing")
print("🔎 Fetching top 10 hot posts from r/investing...\n")

# simply poc print out the title, author, and message from the post
# for post in subreddit.hot(limit=10):    
#     print(f"Title: {post.title}")
#     print(f"Author: {post.author}")
#     print(f"Message: {post.selftext}\n")

for post in subreddit.hot(limit=10):
    title = post.title
    sentiment = analyzer.polarity_scores(title)
    score = sentiment['compound']

    # Classify sentiment
    if score >= 0.05:
        sentiment_label = "Positive"
    elif score <= -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    print(f"📝 Title: {title}")
    print(f"📊 Sentiment Score: {score:.3f} ({sentiment_label})\n")

