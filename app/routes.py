"""All the Flask routes are here."""
from feedgen.feed import FeedGenerator
from flask import Response
from . import app, reddit, subreddit_exists
from .subreddit_fetch import SubredditFetch

@app.errorhandler(404)
def page_not_found(error):
    """
    Handle all other routes.

    :param error: The error we are handling.
    """
    print(error)
    return 'Use /rss/_subreddit_ to get an RSS feed for a subreddit.', 404

@app.route('/healthcheck')
def healthcheck():
    """
    A healthcheck route to ensure the app is running.

    :return: A string response.
    """
    if reddit:
        testsub = reddit.subreddit("redditdev")
        return testsub.title, 200

    return 'Reddit instance not created', 500

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

    found_sub = SubredditFetch(subreddit, reddit)
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
