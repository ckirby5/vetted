import os
import httpx
from dotenv import load_dotenv

load_dotenv()

SCRAPER_CONTACT=os.environ["SCRAPER_CONTACT"]
RAW_DIR="scraper/raw"

def fetch_page(url):
    custom_headers = {"User-Agent": f"Vetted/0.1 (open-source; {SCRAPER_CONTACT})"}
    response = httpx.get(
        url,
        headers=custom_headers,
        follow_redirects=True,
        timeout=10.0
    )

    response.raise_for_status()

    return response.text

def save_raw_html(html, filename):
    os.makedirs(RAW_DIR, exist_ok=True)
    with open(os.path.join(RAW_DIR, filename), "w", encoding="utf-8") as f:
        f.write(html)