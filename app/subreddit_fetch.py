class SubredditFetch:
    """
    A class to represent a subreddit and its posts.

    :param name: The name of the subreddit.
    :param reddit: The Reddit instance to use.
    """

    def __init__(self, name, reddit) -> None:
        self.name = name
        self.reddit = reddit

    def get_hot_posts(self):
        """
        Get the 25 hottest posts from a subreddit. 

        :param self: The subreddit_fetch object.
        :return: A dictionary of post titles keys and URLs.
        """
        hot_posts = {}

        for submission in self.reddit.subreddit(self.name).hot(limit=25):
            hot_posts[submission.title] = submission.url
        return hot_posts

    def clear_posts(self):
        """
        Clear the posts we found.
        """
        self._posts = None
