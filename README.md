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
