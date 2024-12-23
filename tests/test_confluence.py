import os
from pprint import pprint

import pytest
from atlassian import Confluence

from src.get_confluence_spaces import get_last_modified


@pytest.fixture
def confluence_client():
    username = os.getenv("CONFLUENCE_USERNAME")
    api_token = os.getenv("CONFLUENCE_API_KEY")
    base_url = os.getenv("CONFLUENCE_BASE_URL").rstrip("/")
    return Confluence(url=base_url, username=username, password=api_token)


def test_get_space(confluence_client):
    space_key = "EP"
    ep_confluence = confluence_client
    space = ep_confluence.get_space(space_key, expand="history,version,metadata")
    print()
    pprint(space)


def test_get_all_spaces(confluence_client):
    ep_confluence = confluence_client
    spaces = ep_confluence.get_all_spaces(start=700, limit=100)
    print()
    pprint(spaces["results"][80])


def test_get_space_content(confluence_client):
    space_key = "EP"
    ep_confluence = confluence_client
    sc = ep_confluence.get_space_content(space_key)
    print(sc)


def test_get_last_modified_date():
    space_key = "RND"
    print()
    print(get_last_modified(space_key))


def test_space_pages_count(confluence_client):
    # Define the CQL query
    space_key = "RND"
    ep_confluence = confluence_client

    cql = f"type=page AND space={space_key}"

    # Submit the CQL query
    results = ep_confluence.cql(cql, limit=1000)  # Fetching only metadata for count
    total_results = results.get("size", 0)

    print(f"Total non-archived pages in space '{space_key}': {total_results}")
