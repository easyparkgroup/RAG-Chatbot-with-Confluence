import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.document_loaders import ConfluenceLoader
from langchain_core.load import dumps, loads

load_dotenv()

datadir = Path(__file__).parent.parent / "data"
username = os.getenv("CONFLUENCE_USERNAME")
api_token = os.getenv("CONFLUENCE_API_KEY")
base_url = os.getenv("CONFLUENCE_BASE_URL")
openai_key = os.getenv("OPENAI_API_KEY")
interesting_spaces = [
    "DEVXP",  # Developers Experience
    "EP",  # The Curb
    "EPA",  # Drivers Experience
    "EPIC",  # Epic platform
    "ERPTP",  # ERP Transformation Program
    "PC",  # People & Culture
    "PE",  # Parking Excellence
    "PET",  # Platform Engineering
    "POPS",  # Parking Operator Support
    "PPACK",  # Product Packages
    "PRO",  # Productivity
    "RND",  # Product & Technology
    "~215070400",  # Frank's personal space
]


def get_docs_for_space(space_key):
    cache_file = datadir / f"{space_key}_docs.json"
    if cache_file.exists():
        with cache_file.open("r") as f:
            string_representation = json.load(f)
            docs = loads(string_representation)
        print(f"{len(docs)} docs loaded from cache: {space_key}")
    else:
        loader = ConfluenceLoader(
            url=base_url,
            username=username,
            api_key=api_token,
            space_key=space_key,
            limit=10,
            # include_attachments=True, # uncomment to include png, jpeg, ..
            max_pages=500,
            keep_markdown_format=True,
        )
        docs = loader.load()
        with cache_file.open("w") as f:
            string_representation = dumps(docs, pretty=True)
            json.dump(string_representation, f)
        print(f"{len(docs)} docs fetched and saved to cache: {space_key}")

    # for d in docs:
    #     print(d.page_content)
    #     print("*" * 50)
    #     print(d.metadata)
    #     print("*" * 50)
    return docs


def split_docs(docs):
    headers_to_split_on = [
        ("#", "Heading 1"),
        ("##", "Heading 2"),
        ("###", "Heading 3"),
    ]
    split_docs = []
    for doc in docs:
        for header, header_type in headers_to_split_on:
            sections = doc.page_content.split(header)
            for section in sections:
                split_docs.append(section)
    return split_docs


def create_embeddings_from_space_content(space_key):
    docs = get_docs_for_space(space_key)
    print(docs)


if __name__ == "__main__":
    all_docs = []
    for space_key in interesting_spaces[:3]:
        d = get_docs_for_space(space_key)
        all_docs.extend(d)
    print(len(all_docs))
