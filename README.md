# Ohio Sites
A (WIP) collection of central (and beyond) Ohio sites, feeds, calendars, and blogs.

# Totals
248 sites

703 feeds (rss/atom)

39 calendars (ical/ics)

## Python Tools (`tools/`)
- csv_to_json.py
-- Converts the CSV into a json file (useful to run the website)
- duplicates.py
-- Checks if the CSV contains any duplicate URLs
- opml.py
-- Generates an OPML of all atom/rss feeds from the CSV

## Opening `index.html`
- This is a example website probably won't be a longterm project
- Run the csv_to_json.py
- Run `python3 -m http.server 8000` (needs to be on a server because CORS blocks the request to `data.json` otherwise)

### Useful Resources
https://github.com/benlk/columbus-govdelivery-rss/

https://github.com/benlk/columbus-misc-rss/

https://github.com/benlk/columbus-gov-websites/
