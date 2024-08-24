# reddit-rss-pub
Reddit RSS feed using BYO API keys. This turns subreddits into RSS feeds.

Disclaimer: I have no idea what I'm doing when it comes to building feeds so consider this still under development.

## What

Barebones flask app, it works by generating a feed of the 25 'hot' posts from a subreddit your request at `<yourdomain.tld>/rss/$your_api_key_id/<your subreddit>`. It will return an XML payload suitable for most feed readers with a minimal level of detail (post title, URL). Yes you read that right, BYO API keys so use a throwaway account because you shouldn't be giving random people on the internet your real API keys. There is also a non-zero chance reddit may ban or restrict accounts using services like this.

What it does do:

- Connects to the reddit API to GET posts and subreddits
- Returns a mostly well structured RSS XML blob
- Ignores NSFW/SFW status of subreddits, there is no filtering

What it does not do;

- Consider any previous feeds, de-duplication needs to be handled by your reader based on the URL/GUID (some readers do this, such as Inoreader!).
- Rank or re-arrange posts. We use reddits ‘hot’ sorting method for this, which is generally the default view of most subreddits anyway.

## Why

Reddit has [it's own RSS implementation](https://old.reddit.com/wiki/rss), but it returns links to reddit along with a bunch of other useless data that makes your feed ugly. It also can break the in-line reading that readers like Inoreader use because the subreddit itself can't be "unrolled" inside your reader. 

[Reddit also seems to not like people using this feature too much](https://www.buzl.uk/2024/08/24/reddit.html), so by using disposable and easy-to-make API keys that everyone can get in infinite quantities for free we potentially sidestep these issues.  

## Endpoints

As it stands now, this exposes these useful endpoints;

| Endpoint | Purpose |
|----------|---------|
| $domain/rss/$your_api_key_id/$subreddit | Returns 25 'hot' posts from $subreddit |
| $domain/rss/$your_api_key_id/sfw/$subreddit * | Returns 25 'hot' posts from $subreddit ONLY if the subreddit is SFW |
| $domain/rss/$your_api_key_id/noself/$subreddit *  | Returns 25 'hot' posts, but no self posts from $subreddit |

\* _In some cases, might be less than 25 posts_

## How

In theory, you can run this from wherever you like (in my case, DigitalOcean) and just set a few env vars;

| Var | |
|-----|-|
| APP_DOMAIN | the domain (including subdomain if applicable) you wish to run this from |
| SUPABASE_URL | URL for your supa project |
| SUPABASE_KEY | the key for your supa project

You will also need to add your Reddit keys to your supabase project, the schema could quite literally not be any more simple but

For setting up your API keys, start -> [here](https://old.reddit.com/wiki/api)

IMO the easiest way to run this, and the way I do, is to use [DigitalOcean's App Platform](https://www.digitalocean.com/products/app-platform). You can hook up your repo from in your DO dashboard, point to the internal port (5000), set the env vars noted above, and then set a domain. 

Something similar should be possible elsewhere, such as Heroku, but is untested.

## Will it / can it do XYZ

Yes, no, I don't know, maybe. If you can think of a feature that is missing, but that also might be useful (and there's a lot of those) please create an issue or open a PR.

## License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
