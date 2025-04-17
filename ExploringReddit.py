import praw

client_id = "null"
client_secret = "null"
user_agent = "SentimentPoc/0.1 by burritonite"

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Choose your subreddit
subreddit_name = "investing"
subreddit = reddit.subreddit(subreddit_name)

# Helper to print posts from a category
def print_posts(posts, category_name):
    print(f"\n🔹 {category_name.upper()} posts from r/{subreddit_name}:\n")
    for i, post in enumerate(posts, 1):
        print(f"{i}. {post.title} (Score: {post.score}, Comments: {post.num_comments})")
    print("-" * 50)

# Fetch and print each category
print_posts(subreddit.hot(limit=10), "hot")
print_posts(subreddit.new(limit=10), "new")
print_posts(subreddit.top(limit=10), "top")
print_posts(subreddit.rising(limit=10), "rising")


# # Fetching top 10 popular subreddits
# print("🔍 Fetching popular subreddits...\n")
# for subreddit in reddit.subreddits.popular(limit=10):
#     print(f"{subreddit.display_name}: {subreddit.title}")