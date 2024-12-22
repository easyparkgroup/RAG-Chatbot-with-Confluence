# https://atlassian-python-api.readthedocs.io/confluence.html
# https://developer.atlassian.com/server/confluence/expansions-in-the-rest-api/
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from threading import Semaphore

import pandas as pd
from atlassian import Confluence
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
username = os.getenv("CONFLUENCE_USERNAME")
api_token = os.getenv("CONFLUENCE_API_KEY")
base_url = os.getenv("CONFLUENCE_BASE_URL").rstrip("/")
datadir = Path(__file__).parent.parent / "data"
datafile = Path(datadir / "confluence_spaces.csv")

# Initialize the Confluence client
ep_confluence = Confluence(url=base_url, username=username, password=api_token)


def get_last_modified(space_key):
    # Retrieve all pages that belong to the space
    start = 0
    space_pages = []
    while True:
        pages = ep_confluence.get_all_pages_from_space(
            space=space_key, start=start, limit=100, expand="history.lastUpdated"
        )
        # Break the loop if no more pages are turned
        if not pages:
            break

        space_pages.extend(pages)

        # Increment the start index for the next batch
        start += 100

    mod_dates = sorted([p["history"].get("lastUpdated").get("when") for p in space_pages], reverse=True)
    last_modified = datetime.strptime(mod_dates[0], "%Y-%m-%dT%H:%M:%S.%fZ") if mod_dates else None
    return space_key, len(space_pages), last_modified


def get_all_spaces():
    """Fetch all non-archived spaces from Confluence."""
    start = 0

    while True:
        spaces = ep_confluence.get_all_spaces(start=start, limit=100, expand="description.plain")
        for space in spaces["results"]:
            if not space.get("archived", False):
                space_key = space["key"]
                result = {
                    "space_key": space_key,
                    "space_name": space["name"],
                    "space_link": f"{base_url}/spaces/{space_key}/pages",
                    "space_type": space["type"],
                }
                yield result

        # Break the loop if no more pages are returned
        if not spaces["results"]:
            break

        # Increment the start index for the next batch
        start += 100


def get_spaces_data(csv_file):
    # Load from pickle if it exists, otherwise write to it
    if not csv_file.exists():
        spaces_df = pd.DataFrame(list(get_all_spaces()))
        space_keys = spaces_df["space_key"].tolist()
        rate_limit = 5

        def rate_limited_get_most_recently_modified_page(space_key):
            with Semaphore(rate_limit):
                result = get_last_modified(space_key)
                time.sleep(1 / rate_limit)
                return result

        # get last modified date for all spaces
        with ThreadPoolExecutor() as executor:
            last_modified_dates = list(executor.map(rate_limited_get_most_recently_modified_page, space_keys))

        # create a DataFrame from the results
        lmd = pd.DataFrame(last_modified_dates, columns=["space_key", "page_count", "last_modified"])
        # join the last modified dates with the space data
        df = spaces_df.merge(lmd, on="space_key")
        # save the data to a csv file
        df.to_csv(csv_file, index=False)
        print("Data written to csv file.")
    else:
        df = pd.read_csv(csv_file)
        print("Data loaded from csv file.")
    return df


if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    pd.set_option("display.max_colwidth", 1000)

    all_spaces = get_spaces_data(datafile)
    print(all_spaces.head(25))
