"""All the Flask routes are here."""
from flask import Response
from . import app, generate_feed, construct_reddit_instance


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
    if app:
        return 'App is running?', 200

    return 'Reddit instance not created', 500

@app.route('/rss/<key_id>/<subreddit>')
def gen_custom_sub(key_id, subreddit):
    """
    Get the 25 hottest posts from a subreddit.

    :param subreddit: The name of the subreddit to fetch posts from.
    :return: An XML response containing the RSS feed.
    """
    target_sub = construct_reddit_instance(key_id, subreddit)

    hot_posts = target_sub.get_hot_posts()
    if hot_posts is None:
        return Response(f"Error fetching posts for {subreddit}", status=500)

    return generate_feed(subreddit, hot_posts, target_sub)

@app.route('/rss/<key_id>/sfw/<subreddit>')
def gen_sfw_sub(key_id, subreddit):
    """
    Get the 25 hottest posts from a SFW subreddit.
    If it's NSFW, 403.

    :param subreddit: The name of the subreddit to fetch posts from.
    :return: An XML response containing the RSS feed, 403 if NSFW.
    """
    target_sub = construct_reddit_instance(key_id, subreddit)

    if not target_sub.is_sfw:
        return Response(f"Subreddit {subreddit} is NSFW", status=403)

    hot_posts = target_sub.get_hot_sfw_posts()
    if hot_posts is None:
        return Response(f"Error fetching posts for {subreddit}", status=500)

    return generate_feed(subreddit, hot_posts, target_sub)

@app.route('/rss/<key_id>/noself/<subreddit>')
def gen_custom_sub_no_self(key_id, subreddit):
    """
    Get the 25 hottest posts from a subreddit, no self posts.
    If there are more than 76 self posts, we'll end up with less than 25 posts.

    :param subreddit: The name of the subreddit to fetch posts from.
    :return: An XML response containing the RSS feed.
    """
    target_sub = construct_reddit_instance(key_id, subreddit)

    hot_posts = target_sub.get_hot_no_self_posts()
    if hot_posts is None:
        return Response(f"Error fetching posts for {subreddit}", status=500)

    return generate_feed(subreddit, hot_posts, target_sub)
