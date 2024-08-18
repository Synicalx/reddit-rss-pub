import os
import praw
from prawcore.exceptions import NotFound, Forbidden
from feedgen.feed import FeedGenerator
from flask import Flask, Response
import subreddit_fetch

app = Flask(__name__)

# We're going to reuse the Reddit instance in a lot of places
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    # To avoid getting blocked (in theory)
    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
)

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

@app.route('/rss/<subreddit>')
def gen_custom_sub(subreddit):
    """
    Get the 25 hottest posts from a subreddit.

    :param subreddit: The name of the subreddit to fetch posts from.
    :return: An XML response containing the RSS feed, or a non-200 if theres an issue
    """
    sub_exists = subreddit_exists(subreddit, reddit)
    if not sub_exists:
        return Response(f"Subreddit {subreddit} does not exist", status=404)

    found_sub = subreddit_fetch.subreddit_fetch(subreddit, reddit)
    hot_posts = found_sub.get_hot_posts()

    # Create a FeedGenerator object
    fg = FeedGenerator()
    fg.title(f"Reddit - r/ {subreddit}")
    fg.link(href=f"https://www.reddit.com/r/{subreddit}/", rel='alternate')
    fg.description(f"RSS feed generated from the {subreddit} subreddit.")

    for title, url in hot_posts.items():
        fe = fg.add_entry()
        fe.title(title)
        fe.link(href=url)
        fe.guid(url, permalink=True)

    rss_feed = fg.rss_str(pretty=True)

    # Clear the posts we found
    found_sub.clear_posts()

    # Return the RSS feed as an XML response
    return Response(rss_feed, mimetype='application/rss+xml')

@app.errorhandler(404)
def page_not_found():
    """
    Handle all other routes.
    """
    return 'Use /rss/_subreddit_ to get an RSS feed for a subreddit.', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
