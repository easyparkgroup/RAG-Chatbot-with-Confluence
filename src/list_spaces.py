# https://atlassian-python-api.readthedocs.io/confluence.html
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
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


def get_most_recently_modified_page(space_key):
    start = 0
    space_pages = []
    while True:
        # Retrieve a batch of pages from the space
        pages = confluence.get_all_pages_from_space(space=space_key, start=start, limit=100, expand="history,version")

        # Break the loop if no more pages are returned
        if not pages:
            break

        space_pages.extend(pages)

        # Increment the start index for the next batch
        start += 100

    mod_dates = sorted([p.get("version", {}).get("when") for p in space_pages], reverse=True)
    dt = datetime.strptime(mod_dates[0], "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt


def get_all_spaces():
    """Fetch all non-archived spaces from Confluence."""
    start = 0
    page_size = 100

    while True:
        spaces = confluence.get_all_spaces(start=start, limit=page_size, expand="description.plain")
        for space in spaces["results"]:
            if not space.get("archived", False):
                space_key = space["key"]
                # last_modified = get_most_recently_modified_page(space_key)

                result = {
                    "space_key": space_key,
                    "space_name": space["name"],
                    "space_link": f"{base_url}/spaces/{space_key}/pages",
                    "space_type": space["type"],
                }
                print(result)
                yield result

        # Break the loop if no more pages are returned
        if not spaces["results"]:
            break

        # Increment the start index for the next batch
        start += page_size


def get_data(pf):
    # Load from pickle if it exists, otherwise write to it
    if not pf.exists():
        all_spaces = list(get_all_spaces())
        df = pd.DataFrame(all_spaces)
        df.to_pickle(pf)
        print("Data written to pickle file.")
    else:
        df = pd.read_pickle(pf)
        print("Data loaded from pickle file.")
    return df


pickle_file = Path(datadir / "spaces.pkl")
df = get_data(pickle_file)
display_df = df.copy()

# create button to delete the pickle file
if st.button("Delete pickle file"):
    pickle_file.unlink()
    st.write("Pickle file deleted. Reload the page to get fresh data.")


# create toggle to hide personal spaces
if st.checkbox("Hide personal spaces", value=True):
    display_df = display_df[~display_df["space_type"].str.contains("personal", case=False)]

st.dataframe(
    display_df,
    height=700,
    hide_index=True,
    use_container_width=True,
    column_config={
        "space_key": st.column_config.TextColumn("Space Key", width="small"),
        "space_name": st.column_config.TextColumn("Space Name", width="medium"),
        "space_link": st.column_config.LinkColumn("Space Link", width="large"),
        "space_type": st.column_config.TextColumn("Space Type", width="small"),
        # "last_modified": st.column_config.DatetimeColumn("Last Modified", width="medium"),
    },
)

# create a pie chart to show the distribution of space types
st.write("Distribution of space types")
space_type_counts = display_df["space_type"].value_counts()
st.write(space_type_counts)
st.bar_chart(space_type_counts)


if __name__ == "__main__":
    get_data(pickle_file)
