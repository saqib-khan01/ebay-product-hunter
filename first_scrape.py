r"""First test script: load ONE sold-listings page on eBay and print a few results.

Usage:
    .\.venv\Scripts\python.exe first_scrape.py "lego star wars"
    .\.venv\Scripts\python.exe first_scrape.py "lego star wars" --site ebay.com

Rules (see CLAUDE.md): visible Chrome, sold listings only on the three allowed
sites, 3-8 second random wait before each page load, and STOP if a captcha or
block page appears (never try to bypass it). If eBay shows a sign-in page, the
script pauses so YOU can log in by hand in the Chrome window.
"""

import argparse
import random
import sys
import time
from urllib.parse import quote_plus

from playwright.sync_api import sync_playwright

# The only sites this tool is allowed to visit.
ALLOWED_SITES = ["ebay.co.uk", "ebay.com", "ebay.com.au"]

# If any of these words show up in the page, we treat it as a captcha / block page.
BLOCK_SIGNS = [
    "captcha",
    "verify you are human",
    "verify yourself",
    "pardon our interruption",
    "are you a robot",
    "access denied",
    "unusual traffic",
    "security measure",
]


# Folder where Chrome keeps your login session (git-ignored, never commit it).
PROFILE_DIR = ".browser_profile"


class BlockedError(Exception):
    """Raised when eBay shows a captcha or block page."""


def build_sold_url(site: str, search: str) -> str:
    """Make a sold-listings search URL. LH_Sold=1 + LH_Complete=1 means sold items only."""
    if site not in ALLOWED_SITES:
        raise ValueError(f"{site} is not allowed. Use one of: {', '.join(ALLOWED_SITES)}")
    return f"https://www.{site}/sch/i.html?_nkw={quote_plus(search)}&LH_Sold=1&LH_Complete=1"


def polite_wait() -> None:
    """Wait a random 3-8 seconds before loading a page."""
    seconds = random.uniform(3, 8)
    print(f"Waiting {seconds:.1f} seconds before loading the page...")
    time.sleep(seconds)


def check_for_block(page) -> None:
    """Stop the program if the page looks like a captcha or block page."""
    url = page.url.lower()
    text = page.inner_text("body").lower()
    if "captcha" in url or "challenge" in url or any(sign in text for sign in BLOCK_SIGNS):
        raise BlockedError(page.url)


def is_sign_in_page(page) -> bool:
    """True if eBay sent us to its sign-in page."""
    return "signin" in page.url.lower() or page.title().lower().startswith("sign in")


def main() -> int:
    parser = argparse.ArgumentParser(description="Load one eBay sold-listings page.")
    parser.add_argument("search", help='what to search for, e.g. "lego star wars"')
    parser.add_argument("--site", default="ebay.co.uk", choices=ALLOWED_SITES)
    args = parser.parse_args()

    url = build_sold_url(args.site, args.search)
    print(f"Page to load: {url}")

    polite_wait()

    with sync_playwright() as p:
        # channel="chrome" = your real Google Chrome; headless=False = visible window.
        # The profile folder remembers your login so you only sign in once.
        browser = p.chromium.launch_persistent_context(
            PROFILE_DIR, channel="chrome", headless=False
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        try:
            page.goto(url, wait_until="domcontentloaded")
            check_for_block(page)

            if is_sign_in_page(page):
                print("\neBay is asking you to sign in.")
                input("Log in by hand in the Chrome window, then press Enter here...")
                polite_wait()
                page.goto(url, wait_until="domcontentloaded")
                check_for_block(page)
                if is_sign_in_page(page):
                    print("Still on the sign-in page, so I am stopping here.")
                    return 1

            items = page.locator("li.s-item, li.s-card")
            count = items.count()
            print(f"\nPage title: {page.title()}")
            print(f"Found {count} listing blocks. First few:\n")
            for i in range(min(count, 5)):
                lines = [l for l in items.nth(i).inner_text().split("\n") if l.strip()]
                print(f"  {i + 1}. " + " | ".join(lines[:4]))

            input("\nPress Enter to close the browser...")
        except BlockedError as err:
            print("\n" + "=" * 60)
            print("STOPPED: eBay showed a captcha or block page.")
            print(f"Page: {err}")
            print("I will NOT try to get around it. Please look at the Chrome window,")
            print("and wait a while before trying again.")
            print("=" * 60)
            input("Press Enter to close the browser...")
            return 1
        finally:
            browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
