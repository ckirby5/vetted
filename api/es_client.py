import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

ELASTICSEARCH_URL=os.environ["ELASTICSEARCH_URL"]

def get_es_client():
    client = Elasticsearch (
        hosts=[ELASTICSEARCH_URL]
    )
    return client

INDEX_NAME = "eligibility_rules"

MAPPING = {
    "program_id": "keyword",
    "program_name": "text",
    "jurisdiction": "keyword",
    "state": "keyword",
    "category": "keyword",
    "rule_type": "keyword",
    "raw_text": "text",
    "source_url": "keyword",
    "last_scraped_at": "date"
}

map_props = {"properties": {}}

for field_name, field_type in MAPPING.items():
    map_props["properties"][field_name] = {"type": field_type}

def create_index_if_not_exists(es_client):
    if not es_client.indices.exists(index=INDEX_NAME):
        es_client.indices.create(index=INDEX_NAME, mappings=map_props)
        print(f"Index {INDEX_NAME} created successfully with mappings")
    else:
        print("Index already exists, skipping")

def index_program_rules(es_client, program): 
    es_client.delete_by_query(
        index=INDEX_NAME,
        query={"term": {"program_id": str(program.id)}}
    )

    for rule in program.eligibility_rules:
        
        doc = {
            "program_id": str(program.id),
            "program_name": program.name,
            "jurisdiction": program.jurisdiction,
            "state": program.state,
            "category": program.category,
            "rule_type": rule.rule_type,
            "raw_text": rule.raw_text,
            "source_url": program.source_url,
            "last_scraped_at": program.last_scraped_at.isoformat()
        }

        es_client.index(index=INDEX_NAME, id=str(rule.id), document=doc)

def search_eligibility(es_client, query_text, category=None, state=None):
    filters = []
    if category:
        filters.append({"term": {"category": category}})
    if state:
        filters.append({"term": {"state": state}})

    result = es_client.search(index=INDEX_NAME, query={
        "bool": {
            "must": [
                {"match": {"raw_text": query_text}}
            ],
            "filter": filters
        }
    })
    return result["hits"]["hits"]
