# Username Finder

Checks which public sites have a given username and streams the results live.

## Run

```
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000

## Files

- `main.py`: FastAPI backend (parallel checks, live streaming, rate limit)
- `sites.json`: the sites to check and how to detect a profile on each
- `index.html`: the search page
- `requirements.txt`: Python dependencies

## Add a site

Add one line to `sites.json`:

```
{"name": "Site", "url": "https://site.com/{}"}
```

`{}` is replaced with the username. Optional fields:

- `profile_url`: the link shown to the user, if different from `url`
- `mode`: `present_text` (found if `text` is in the page) or `absent_text` (not found if `text` is in the page)
- `text`: the text to look for

Default rule: HTTP 200 means found, 404 means not found, anything else means the site could not be checked.

## Notes

- Sites change and block bots. Re-test the rules now and then. A blocked site shows as "could not be checked", never as a match.
- A match is a lead, not proof of identity.
- Before going public, add Terms, a Privacy Policy and an opt-out page.
- Deploy on Render or Railway with the start command `uvicorn main:app --host 0.0.0.0 --port $PORT`.
