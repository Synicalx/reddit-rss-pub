import os
import praw
import subreddit_fetch
from feedgen.feed import FeedGenerator
from flask import Flask, Response

app = Flask(__name__)

# We're going to reuse the Reddit instance in a lot of places
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    # To avoid getting blocked (in theory)
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
)

app_domain = os.getenv('APP_DOMAIN')

@app.route('/rss/<subreddit>')
def gen_custom_sub(subreddit):
    found_sub = subreddit_fetch.subreddit_fetch(subreddit, reddit)
    return found_sub.posts

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
