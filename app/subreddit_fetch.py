"""A class representing a subreddit and its posts."""
import praw
from prawcore.exceptions import NotFound

class SubredditFetch:
    """
    A class to represent a subreddit and its posts.

    :param name: The name of the subreddit.
    :param reddit: The Reddit instance to use.
    """

    def __init__(self, name, client_id, client_secret) -> None:
        self.name = name
        self.hot_posts = {}
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        )
        self._exists = None
        self._is_sfw = None

    @property
    def exists(self):
        """
        Check if the subreddit exists.

        :return: True if the subreddit exists, False otherwise.
        """
        if self._exists is None:
            self._exists = self.subreddit_exists()
        return self._exists

    @property
    def is_sfw(self):
        """
        Check if the subreddit is safe for work.

        return: True if the subreddit is safe for work, False otherwise.
        """
        if self._is_sfw is None:
            self._is_sfw = self.is_sub_sfw()
        return self._is_sfw

    def subreddit_exists(self) -> bool:
        """
        Check if the subreddit exists.

        :return: True if the subreddit exists, False otherwise.
        """
        try:
            sub_id = self.reddit.subreddit(self.name).id
            if sub_id:
                return True
            return False
        except NotFound:
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

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

    def get_hot_sfw_posts(self):
        """
        Get the 25 hottest posts from a subreddit, excluding NSFW posts.

        :return: A dictionary with post titles as keys and URLs as values.
        """
        hot_posts = {}
        try:
            for submission in self.reddit.subreddit(self.name).hot(limit=100):
                if not submission.is_over_18:
                    hot_posts[submission.title] = submission.url
                if len(hot_posts) >= 25:
                    break
            return hot_posts
        except Exception as e:
            print("Error fetching posts:", e)
            return {}

    def is_sub_sfw(self):
        """
        True or False if the subreddit is safe for work.

        :return: True if the subreddit is safe for work, False otherwise.
        """
        if self.reddit.subreddit(self.name).over18:
            return False
        return True

    def clear_posts(self):
        """
        Clear the posts we found.
        """
        self.hot_posts = None
