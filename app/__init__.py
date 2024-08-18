"""All the core functionality of the app is here."""
import os
import praw
from feedgen.feed import FeedGenerator
from flask import Flask, Response
from prawcore.exceptions import NotFound, Forbidden

# We're going to reuse the Reddit instance in a lot of places
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    # To avoid getting blocked (in theory)
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
)

app = Flask(__name__)

app_domain = os.getenv('APP_DOMAIN')

def subreddit_exists(subreddit, praw_instance):
    """
    Check if a subreddit exists.

    :param subreddit: The name of the subreddit to check.
    :param reddit: The Reddit instance to use.
    :return: True if the subreddit exists and we can access it, False otherwise.
    """
    try:
        praw_instance.subreddits.search_by_name(subreddit, exact=True)
        return True
    except NotFound:
        return False
    except Forbidden:
        return False

def generate_feed(subreddit, posts, source_subreddit):
    """
    Generate an RSS feed from a dictionary of posts.

    :param subreddit: The name of the subreddit.
    :param posts: A dictionary of post titles and URLs.
    :param source_subreddit: The SubredditFetch object.

    :return: An XML response containing the RSS feed.
    """
    # Create a FeedGenerator object
    fg = FeedGenerator()
    fg.title(f"Reddit - r/ {subreddit}")
    fg.link(href=f"https://www.reddit.com/r/{subreddit}/", rel='alternate')
    fg.description(f"RSS feed generated from the {subreddit} subreddit.")

    for title, url in posts.items():
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=url)
        fe.guid(url, permalink=True)

    rss_feed = fg.rss_str(pretty=True)

    # Clear the posts we found
    source_subreddit.clear_posts()

    # Return the RSS feed as an XML response
    return Response(rss_feed, mimetype='application/rss+xml')

from . import routes
