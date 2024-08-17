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

@app.route('/')
def home():
    """
    The homepage of the app.

    :return: Some instructions.
    """
    return 'Use /rss/_subreddit_ to get an RSS feed for a subreddit.'

@app.errorhandler(404)
def page_not_found(e):
    # You can return a custom template or message here
    return "Sorry, this page does not exist.", 404

@app.route('/rss/<subreddit>')
def gen_custom_sub(subreddit):
    """
    Get the 25 hottest posts from a subreddit.

    :param subreddit: The name of the subreddit to fetch posts from.
    :return: An XML response containing the RSS feed.
    """
    found_sub = subreddit_fetch.subreddit_fetch(subreddit, reddit)
    if found_sub.exists:
        found_sub.posts = found_sub.get_hot_posts(subreddit, reddit)
    else:
        return "Sorry, this sub does not exist."

    # Create a FeedGenerator object
    fg = FeedGenerator()
    fg.title(f"Reddit - r/ {subreddit}")
    fg.link(href=f"https://www.reddit.com/r/{subreddit}/", rel='alternate')
    fg.description(f"RSS feed generated from the {subreddit} subreddit.")

    for title, url in found_sub.posts.items():
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=url)

    rss_feed = fg.rss_str(pretty=True)

    # Clear the posts we found
    found_sub.clear_posts()

    # Return the RSS feed as an XML response
    return Response(rss_feed, mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
