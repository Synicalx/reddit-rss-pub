"""All the core functionality of the app is here."""
import os
import hashlib
import hmac
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

def generate_hash(api_key_id: str, secret_key: str) -> str:
    """Generate SHA-256 hash of the API key ID using the user-provided secret key."""
    return hmac.new(secret_key.encode(), api_key_id.encode(), hashlib.sha256).hexdigest()

def insert_reddit_key(hashed_id: str, reddit_id: str, reddit_key: str):
    response = (
        supabase
        .table('user_data')
        .insert({
            'sha_of_key_id': hashed_id,
            'reddit_id': reddit_id,
            'reddit_key': reddit_key
        })
        .execute()
    )
    return response.status_code

def get_reddit_key(input_hash: str):
    """
    Retrieve the Reddit key and its associated Reddit ID using the hash of the Reddit ID.

    :param reddit_id: The Reddit ID to look up.
    :return: A tuple (reddit_id, reddit_key) if found, otherwise None.
    """
    try:
        response = (
            supabase
            .table('user_data')
            .select('reddit_id, reddit_key')
            .eq('sha_of_key_id', input_hash)
            .execute()
        )
        if response.data and len(response.data) > 0:
            return response.data[0]['reddit_id'], response.data[0]['reddit_key']
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def construct_reddit_instance(input_hash, subreddit):
    """
    Create a SubredditFetch object.

    :param client_id: The Reddit client ID.
    :param subreddit: The name of the subreddit.
    :retrun: A SubredditFetch object.
    """
    reddit_api_key_id, reddit_api_key = get_reddit_key(input_hash)

    if reddit_api_key or reddit_api_key_id is None:
        return Response(f"Reddit API key not found for {input_hash}", status=404)

    target_sub = SubredditFetch(subreddit, reddit_api_key_id, reddit_api_key)

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