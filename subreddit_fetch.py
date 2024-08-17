class subreddit_fetch:
    """
    A class to represent a subreddit and its posts.
    """

    def __init__(self, name, reddit) -> None:
        self.name = name
        self.reddit = reddit
        self.posts = self.get_hot_posts(self.name, self.reddit)

    def get_hot_posts(self, subreddit_name, reddit):
        """
        Get the 25 hottest posts from a subreddit. 

        :param subreddit_name: The name of the subreddit to fetch posts from.
        :param reddit: The Reddit instance to use.
        :return: A dictionary of post titles keys and URLs.
        """
        hot_posts = {}

        for submission in self.reddit.subreddit(subreddit_name).hot(limit=25):
            hot_posts[submission.title] = submission.url
        return hot_posts
