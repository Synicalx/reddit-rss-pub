"""A class representing a subreddit and its posts."""
class SubredditFetch:
    """
    A class to represent a subreddit and its posts.

    :param name: The name of the subreddit.
    :param reddit: The Reddit instance to use.
    """

    def __init__(self, name, reddit) -> None:
        self.name = name
        self.reddit = reddit
        self.hot_posts = {}

    def get_hot_posts(self):
        """
        Get the 25 hottest posts from a subreddit. 

        :param self: The subreddit_fetch object.
        :return: A dictionary of post titles keys and URLs.
        """
        try:
            for submission in self.reddit.subreddit(self.name).hot(limit=25):
                self.hot_posts[submission.title] = submission.url
            return self.hot_posts
        except Exception as e:
            print("Error fetching posts: ", e)
            return None

    def clear_posts(self):
        """
        Clear the posts we found.
        """
        self.hot_posts = None
