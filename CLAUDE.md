# eBay Product Hunter

A personal, **non-API** eBay product research tool. It uses Playwright to drive a
**visible Chrome window** and reads **sold listings** to help find products worth
reselling. Data is saved to SQLite and can be exported to Excel.

The owner is a complete beginner: explain steps simply and keep code easy to read.

## Tech stack
- Python 3.13, virtual environment in `.venv/`
- Playwright (uses the installed Google Chrome, `channel="chrome"`, `headless=False`)
- SQLite (built-in `sqlite3`) for storage
- openpyxl for Excel export

## Setup / running
- Activate venv: `.\.venv\Scripts\Activate.ps1`
- Install deps: `pip install -r requirements.txt`
- Run scripts with the venv Python: `.\.venv\Scripts\python.exe <script>.py`

## Rules (must always be followed)
1. **No eBay API.** Browse the website only.
2. **No login, ever.** Never sign in to eBay or any account; never ask for or store credentials.
3. **Visible Chrome only.** Never run headless.
4. **Sold listings only**, on these sites only:
   - ebay.co.uk
   - ebay.com
   - ebay.com.au
   Do not visit any other eBay site or domain.
5. **Polite pacing:** wait a random 3-8 seconds between page loads. There is no
   daily page limit.
6. **Captcha / block pages:** if a captcha, "verify you are human", or block/robot-check
   page appears, **stop immediately and tell the user.** Never try to solve, bypass,
   or work around it (no proxies, no stealth plugins, no retry loops).
7. **Storage:** save all data to SQLite (`ebay_data.db`) and export to Excel (`exports/`).
   Database and exports are git-ignored.

## Project layout (planned)
- `CLAUDE.md` - this file
- `requirements.txt` - pinned dependencies
- `.gitignore` - files git should skip
- (future) `scraper.py`, `db.py`, `export.py`
