import os
import praw
from flask import Flask
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

def subreddit_exists(subreddit, reddit):
    """
    Check if a subreddit exists.

    :param subreddit: The name of the subreddit to check.
    :param reddit: The Reddit instance to use.
    :return: True if the subreddit exists and we can access it, False otherwise.
    """
    try:
        reddit.subreddits.search_by_name(subreddit, exact=True)
        return True
    except NotFound:
        return False
    except Forbidden:
        return False
    except Exception:
        return False
    
from . import routes  # Import routes to register them with the app