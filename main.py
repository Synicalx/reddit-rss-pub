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
def gen_rss():
    return construct_feed()

def construct_feed():
    fg = FeedGenerator()
    fg.title('Reddit Feed')
    fg.link(href=f'{app_domain}/rss', rel='self')
    fg.description('Reddit feed for various subreddits')

    for sub in subreddits:
        fg = add_sub_to_feed(sub, fg)

    return fg.rss_str(pretty=True)

def add_sub_to_feed(sub, fg):
    content = get_posts(sub)
    for title, url in content.items():
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=url)
    return fg

def get_posts(target):
    posts = {}

    for submission in reddit.subreddit(target).hot(limit=5):
        posts[submission.title] = submission.url
    return posts

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
