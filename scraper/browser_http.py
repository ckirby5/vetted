from playwright_stealth import Stealth
from playwright.sync_api import sync_playwright

def fetch_page_rendered(url):
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page()
        response = page.goto(url, wait_until="networkidle", timeout=30000)

        if response is None or response.status != 200:
            raise ValueError(f"Failed to fetch page: status {response.status if response else 'no response'}")

        html = page.content()
        browser.close()
        return html
