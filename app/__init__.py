"""All the core functionality of the app is here."""
import os
import praw
from feedgen.feed import FeedGenerator
from flask import Flask, Response
from prawcore.exceptions import NotFound, Forbidden
from supabase import create_client, Client
from .subreddit_fetch import SubredditFetch

app = Flask(__name__)
app_domain = os.getenv('APP_DOMAIN')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_reddit_key(reddit_id):
    """
    Setup the Reddit instance.

    :return: A Reddit instance, or None.
    """
    try:
        response = (
            supabase
            .table('user_data')
            .select('reddit_key')
            .eq('reddit_id', reddit_id)
            .execute()
        )
        if response.data and len(response.data) > 0:
            return response.data[0]['reddit_key']
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def construct_reddit_instance(client_id, subreddit):
    """
    Create a SubredditFetch object.

    :param client_id: The Reddit client ID.
    :param subreddit: The name of the subreddit.
    :retrun: A SubredditFetch object.
    """
    reddit_api_key = get_reddit_key(client_id)
    if reddit_api_key is None:
        return Response(f"Reddit API key not found for {client_id}", status=404)

    target_sub = SubredditFetch(subreddit, client_id, reddit_api_key)

    if not target_sub.exists:
        return Response(f"Subreddit {subreddit} does not exist", status=404)

    return target_sub

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
