import os
import re
from pathlib import Path

import pandas as pd
from atlassian import Confluence
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
username = os.getenv("CONFLUENCE_USERNAME")
api_token = os.getenv("CONFLUENCE_API_KEY")
base_url = os.getenv("CONFLUENCE_BASE_URL").rstrip("/")
datadir = Path(__file__).parent.parent / "data"

# Initialize the Confluence client
confluence = Confluence(url=base_url, username=username, password=api_token)


def get_all_spaces():
    """Fetch all non-archived spaces from Confluence."""
    start = 0
    page_size = 100

    while True:
        spaces = confluence.get_all_spaces(start=start, limit=page_size, expand="description.plain")
        for space in spaces["results"]:
            if not space.get("archived", False):
                space_key = space["key"]
                yield {
                    "space_key": space_key,
                    "space_name": space["name"],
                    "space_link": f"{base_url}/spaces/{space_key}",
                }

        if len(spaces["results"]) < page_size:
            print(spaces["results"])
            break
        start += page_size


if __name__ == "__main__":
    # Load from pickle if it exists, otherwise write to it
    pickle_file = Path(datadir / "spaces.pkl")
    if not pickle_file.exists():
        all_spaces = list(get_all_spaces())
        df = pd.DataFrame(all_spaces)
        # add boolean column "is_personal" to indicate if the space is personal or not
        # regexp match space_key to see whether it starts with '~' or '-'
        df["is_personal"] = df["space_key"].apply(lambda x: re.match(r"^[~|-]", x) is not None)
        df.to_pickle(pickle_file)
        print("Data written to pickle file.")
    else:
        df = pd.read_pickle(pickle_file)
        print("Data loaded from pickle file.")

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.max_rows", None)

    # display all spaces that are not personal
    print(df[~df["is_personal"]])
