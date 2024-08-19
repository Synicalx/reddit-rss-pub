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
        self.is_sfw = self.is_sub_sfw()

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

    def get_hot_no_self_posts(self):
        """
        Get the 25 hottest posts from a subreddit, excluding self posts.

        :return: A dictionary with post titles as keys and URLs as values.
        """
        hot_posts = {}
        try:
            for submission in self.reddit.subreddit(self.name).hot(limit=100):
                if not submission.is_self:
                    hot_posts[submission.title] = submission.url
                if len(hot_posts) >= 25:
                    break
            return hot_posts
        except Exception as e:
            print("Error fetching posts:", e)
            return {}

    def is_sub_sfw(self):
        if self.reddit.subreddit(self.name).over18:
            return False
        return True

    def clear_posts(self):
        """
        Clear the posts we found.
        """
        self.hot_posts = None
