# Ohio Sites
A (WIP) collection of central (and beyond) Ohio sites, feeds, calendars, and blogs.

# Totals

247 sites

704 feeds (rss/atom)

39 calendars (ical/ics)

13 ActivityPub accounts

8 AtProto accounts

---
1011 Total

## Add new site
Manually add a new site by editing the csv, then re-run `csv_to_json.py`, `duplicates.py`, `opml.py`, and both alphabetical python scripts.

*or* Create a new issue, select 'Submit a new site'. Fill out the required fields and the Github action *should* create a PR for your new site automatically.

### Suggestions
When looking for RSS feeds on a site, install an add-on like [Feed Indicator for Firefox](https://addons.mozilla.org/en-US/firefox/addon/feed-indicator/) or [RSS Feed Finder for Chrome](https://chromewebstore.google.com/detail/rss-feed-finder/gneplfjjnfmbgimbgonejfoaiphdfkcp) to detect if there are hidden feeds on a page. You can also just try adding `/feed`, `/rss`, `/blog.xml`, or `/blog-feed.xml` to the end of the URL and see if there's a hidden feed there. Empty feeds (feeds that have no content, possibly because of a misconfiguration or any number of reasons) are accepted.

## Python Tools (`tools/`)

- csv_to_json.py
  - Converts the CSV into a json file (useful to run the website)
- duplicates.py
  - Checks if the CSV contains any duplicate URLs
- opml.py
  - Generates an OPML of all atom/rss feeds from the CSV
- rss_cleanup.py
  - Fetches rss/atom feeds (w/o titles) to fill in title/description columns. Use with `--full` to rescrape all rss/atom feeds.
- url_cleanup.py
  - Fetches URLs (w/o titles) to fill in title/description columns. Use with `--full` to refetch all existing urls
- totals.py
  - Counts up number of urls, rss+atom feeds, activitypub accounts, and atproto accounts to add to README
- alphabetical_csv.py
  - Sorts the entire CSV on the url column, alphabetically.
- alphabetical_tags.py
  - Sorts the Category field for each row, alphabetically.

## Opening `index.html`
- This is a example website probably won't be a longterm project
- Run the csv_to_json.py
- Run `python3 -m http.server 8000` (needs to be on a server because CORS blocks the request to `data.json` otherwise)

Web View:
<img width="1857" height="601" alt="image" src="https://github.com/user-attachments/assets/4ed67880-7ac6-4b37-bec5-6087425990a7" />

### Useful Resources
https://github.com/benlk/columbus-govdelivery-rss/

https://github.com/benlk/columbus-misc-rss/

https://github.com/benlk/columbus-gov-websites/
