"""All the Flask routes are here."""
import supabase
from flask import request, render_template, Response
from . import app, generate_feed, construct_reddit_instance, insert_reddit_key, generate_hash


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

@app.route('/add_reddit_key', methods=['GET', 'POST'])
def add_reddit_key():
    """
    Show a form to input Reddit key ID and Reddit key, and handle form submissions.

    :return: A rendered template with a message.
    """
    if request.method == 'POST':
        reddit_id = request.form.get('reddit_id')
        reddit_key = request.form.get('reddit_key')
        if not reddit_id or not reddit_key:
            return render_template('add_reddit_key.html',
                                   message="Please provide both Reddit Key ID and Reddit Key.")

        try:
            hashed_id = generate_hash(reddit_id, reddit_key)
            response_code = insert_reddit_key(hashed_id, reddit_id, reddit_key)

            if response_code == 201:
                return render_template('add_reddit_key.html', 
                                       message="Reddit key added successfully!")
            return render_template('add_reddit_key.html', 
                                   message="Failed to add Reddit key.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return render_template('add_reddit_key.html',
                                   message="An error occurred while processing the request.")
    return render_template('add_reddit_key.html', message=None)

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
