# reddit-rss-pub
DIY Reddit RSS feed using BYO API keys. 

Disclaimer: I have no idea what I'm doing when it comes to building feeds so consider this still under development.

## What

Barebones flask app, it works by generating a feed of the 25 'hot' posts from a subreddit your request at `<yourdomain.tld>/rss/<your subreddit>`. It will return an XML payload suitable for most feed readers with a minimal level of detail (post title, URL).

In theory, you can run this from wherever you like (in my case, DigitalOcean) and just set a few env vars;

```
APP_DOMAIN - the domain (including subdomain if applicable) you wish to run this from
REDDIT_CLIENT_ID - the client ID from your personal reddit key pair
REDDIT_CLIENT_SECRET - the secret from your personal reddit key pair
```

For setting up your API keys, start -> [here](https://old.reddit.com/wiki/api)

## How

IMO the easiest way to run this, and the way I do, is to use [DigitalOcean's App Platform](https://www.digitalocean.com/products/app-platform). You can hook up your repo from in your DO dashboard, set the env vars noted above, and then set a domain. 

Something similar should be possible elsewhere, such as Heroku, but is untested.