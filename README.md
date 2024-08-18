# reddit-rss-pub
DIY Reddit RSS feed using BYO API keys. 

Disclaimer: I have no idea what I'm doing when it comes to building feeds so consider this still under development.

## What

Barebones flask app, it works by generating a feed of the 25 'hot' posts from a subreddit your request at `<yourdomain.tld>/rss/<your subreddit>`. It will return an XML payload suitable for most feed readers with a minimal level of detail (post title, URL).

What it does do:

- Connects to the reddit API to GET posts and subreddits
- Returns a mostly well structured RSS XML blob
- Ignores NSFW/SFW status of subreddits, there is no filtering

What it does not do;

- Consider any previous feeds, de-duplication needs to be handled by your reader based on the URL/GUID (some readers do this, such as Inoreader!).
- Rank or re-arrange posts. We use reddits ‘hot’ sorting method for this, which is generally the default view of most subreddits anyway.

## How

In theory, you can run this from wherever you like (in my case, DigitalOcean) and just set a few env vars;

| Var | |
|-----|-|
| APP_DOMAIN | the domain (including subdomain if applicable) you wish to run this from |
| REDDIT_CLIENT_ID | the client ID from your personal reddit key pair |
| REDDIT_CLIENT_SECRET | the secret from your personal reddit key pair |

For setting up your API keys, start -> [here](https://old.reddit.com/wiki/api)


IMO the easiest way to run this, and the way I do, is to use [DigitalOcean's App Platform](https://www.digitalocean.com/products/app-platform). You can hook up your repo from in your DO dashboard, point to the internal port (5000), set the env vars noted above, and then set a domain. 

Something similar should be possible elsewhere, such as Heroku, but is untested.