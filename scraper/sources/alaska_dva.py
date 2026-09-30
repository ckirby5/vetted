from bs4 import BeautifulSoup

from scraper.http import save_raw_html
from scraper.browser_http import fetch_page_rendered
from api.es_client import get_es_client, create_index_if_not_exists, index_program_rules
from scraper.pipeline import save_program
from api.models.constants import Jurisdiction, Category
from api.db import SessionLocal


URL = "https://veterans.alaska.gov/benefits"

def parse_alaska_benefits(html):
    soup = BeautifulSoup(html, "lxml")

    main_content = soup.select_one("div.col-md-12.column")
    if main_content is None:
        raise ValueError("Main content container not found - page structure may have changed")

    raw_text = main_content.get_text(separator="\n", strip=True)

    if raw_text is None or len(raw_text) < 50:
        raise ValueError("Extracted content is empty or suspiciously short")

    title = "Alaskan Veteran Benefits Eligibility"

    return title, raw_text

def run():
    html = fetch_page_rendered(URL)
    save_raw_html(html, "alaska_benefits_eligibility.html")
    title, raw_text = parse_alaska_benefits(html)

    es_client = get_es_client()
    create_index_if_not_exists(es_client)

    with SessionLocal() as session:
        program = save_program(
            session, name=title, description="", source_url=URL,
            jurisdiction=Jurisdiction.STATE.value, state="Alaska",
            category=Category.HEALTHCARE.value,
            sections=[raw_text]
        )

        index_program_rules(es_client, program)

    print(f"Saved 1 section, indexed to Elasticsearch")

if __name__ == "__main__":
    run()