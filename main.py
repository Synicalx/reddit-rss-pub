import os
import praw
from feedgen.feed import FeedGenerator
from flask import Flask, Response

app = Flask(__name__)

# Update env vars as needed
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    # To avoid getting blocked (in theory)
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
)

app_domain = os.getenv('APP_DOMAIN')

subreddits = ['python', 'programming']  # etc etc

@app.route('/rss')
def generate_rss():
    fg = FeedGenerator()
    fg.title('Reddit RSS Feed')
    fg.link(href=app_domain, rel='self')
    fg.description('RSS feed of posts from specified subreddits')

    for subreddit in subreddits:
        for post in reddit.subreddit(subreddit).hot(limit=5): 
            fe = fg.add_entry()
            fe.title(post.title)
            fe.link(href=post.url)
            fe.description(post.selftext)

    rss_feed = fg.rss_str(pretty=True)
    return Response(rss_feed, mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
