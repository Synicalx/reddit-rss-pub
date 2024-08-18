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

    :return: A string response and status code.
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
    :return: An XML response containing the RSS feed.
    """
    sub_exists = subreddit_exists(subreddit, reddit)
    if not sub_exists:
        return Response(f"Subreddit {subreddit} does not exist", status=404)

    found_sub = SubredditFetch(subreddit, reddit)
    hot_posts = found_sub.get_hot_posts()
    if hot_posts is None:
        return Response(f"Error fetching posts for {subreddit}", status=500)

    return generate_feed(subreddit, hot_posts, found_sub)


@app.route('/rss/noself/<subreddit>')
def gen_custom_sub_no_self(subreddit):
    """
    Get the 25 hottest posts from a subreddit, no self posts.

    :param subreddit: The name of the subreddit to fetch posts from.
    :return: An XML response containing the RSS feed.
    """
    sub_exists = subreddit_exists(subreddit, reddit)
    if not sub_exists:
        return Response(f"Subreddit {subreddit} does not exist", status=404)

    found_sub = SubredditFetch(subreddit, reddit)
    hot_posts = found_sub.get_hot_no_self_posts()
    if hot_posts is None:
        return Response(f"Error fetching posts for {subreddit}", status=500)

    return generate_feed(subreddit, hot_posts, found_sub)

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
