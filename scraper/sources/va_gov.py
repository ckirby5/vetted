import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from scraper.pipeline import save_program
from api.models.constants import Jurisdiction, Category
from api.db import SessionLocal
from api.es_client import get_es_client, create_index_if_not_exists, index_program_rules
from scraper.http import fetch_page

load_dotenv()

SCRAPER_CONTACT=os.environ["SCRAPER_CONTACT"]
RAW_DIR = "scraper/raw"

def save_raw_html(html, filename):
    os.makedirs(RAW_DIR, exist_ok=True)
    with open(os.path.join(RAW_DIR, filename), "w", encoding="utf-8") as f:
        f.write(html)

def parse_disability_eligibility(html):
    soup = BeautifulSoup(html, "lxml")

    h1 = soup.find('h1')
    if h1 is None:
        raise ValueError("No h1 found - page structure may have changed")
    title = h1.get_text(separator="\n", strip=True)

    intro_div = soup.find('div', class_='va-introtext')
    intro = intro_div.get_text(separator="\n", strip=True) if intro_div else ""

    sections = []

    divs = soup.find_all('div', attrs={'data-template': 'paragraphs/q_a'})

    for div in divs:
        heading = div.find('h2')
        body = div.find('div', attrs={'data-template': 'paragraphs/wysiwyg'})

        if heading is None or body is None:
            continue
        sections.append(heading.get_text(separator="\n", strip=True) + '\n' + body.get_text(separator="\n", strip=True))
    if not sections:
        raise ValueError("No Q&A sections found - selectors may be broken")
    
    return title, intro, sections

URL = "https://www.va.gov/disability/eligibility/"
def run():
    html = fetch_page(URL)
    save_raw_html(html, "va_disability_eligibility.html")
    title, intro, sections = parse_disability_eligibility(html)

    es_client = get_es_client()
    create_index_if_not_exists(es_client)

    with SessionLocal() as session:
        program = save_program(
            session, name=title, description=intro, source_url=URL, jurisdiction=Jurisdiction.FEDERAL.value, state=None,
            category = Category.DISABILITY.value, sections = sections
        )
        index_program_rules(es_client, program)

    print(f"Saved {len(sections)} sections, indexed to Elasticsearch")

if __name__ == "__main__":
    run()
    