class subreddit_fetch:

    def __init__(self, name, reddit) -> None:
        self.name = name
        self.reddit = reddit
        self.posts = self.get_hot_posts(self.name, self.reddit)

    def get_hot_posts(self, subreddit_name, reddit):
        hot_posts = {}

        for submission in self.reddit.subreddit(subreddit_name).hot(limit=25):
            hot_posts[submission.title] = submission.url
        return hot_posts
