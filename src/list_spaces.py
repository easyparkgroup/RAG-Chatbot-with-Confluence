# https://atlassian-python-api.readthedocs.io/confluence.html
import os
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from threading import Semaphore

import altair as alt
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
pickle_file = Path(datadir / "spaces.pkl")

# Initialize the Confluence client
ep_confluence = Confluence(url=base_url, username=username, password=api_token)


def get_most_recently_modified_page(space_key):
    start = 0
    space_pages = []
    while True:
        # Retrieve a batch of pages that belong to the space
        # or https://atlassian-python-api.readthedocs.io/confluence.html#get-spaces-info
        # get_space_content()
        pages = ep_confluence.get_all_pages_from_space(
            space=space_key, start=start, limit=100, expand="history,version"
        )

        # Break the loop if no more pages are turned
        if not pages:
            break

        space_pages.extend(pages)

        # Increment the start index for the next batch
        start += 100

    mod_dates = sorted([p.get("version", {}).get("when") for p in space_pages], reverse=True)
    if mod_dates:
        dt = datetime.strptime(mod_dates[0], "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        dt = None
    return space_key, dt


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


def get_data(pf):
    # Load from pickle if it exists, otherwise write to it
    if not pf.exists():
        spaces_df = pd.DataFrame(list(get_all_spaces()))
        space_keys = spaces_df["space_key"].tolist()
        rate_limit = 5

        def rate_limited_get_most_recently_modified_page(space_key):
            with Semaphore(rate_limit):
                result = get_most_recently_modified_page(space_key)
                time.sleep(1 / rate_limit)
                return result

        # get last modified date for all spaces
        with ThreadPoolExecutor() as executor:
            last_modified_dates = list(executor.map(rate_limited_get_most_recently_modified_page, space_keys))

        # create a DataFrame from the results
        lmd = pd.DataFrame(last_modified_dates, columns=["space_key", "last_modified"])
        # join the last modified dates with the space data
        df = spaces_df.merge(lmd, on="space_key")
        # save the data to a pickle file
        df.to_pickle(pickle_file)
        print("Data written to pickle file.")
    else:
        df = pd.read_pickle(pf)
        print("Data loaded from pickle file.")
    return df


df = get_data(pickle_file)
display_df = df.copy()


col1, col2 = st.columns(2)

with col1:
    # create button to delete the pickle file
    if st.button("Delete pickle file"):
        pickle_file.unlink()
        st.write("Pickle file deleted. Reload the page to get fresh data.")
    # create toggle to hide personal spaces
    if st.checkbox("Hide personal spaces", value=True):
        display_df = display_df[~display_df["space_type"].str.contains("personal", case=False)]

with col2:
    # create an altair pie chart to show the distribution of space types
    st.write("Distribution of space types")
    space_type_counts = display_df["space_type"].value_counts().reset_index()
    space_type_counts.columns = ["space_type", "count"]
    bar_chart = (
        alt.Chart(space_type_counts)
        .mark_bar()
        .encode(
            x=alt.X(field="space_type", type="nominal", sort="-y"),
            y=alt.Y(field="count", type="quantitative"),
            color=alt.Color(field="space_type", type="nominal", legend=None),
            tooltip=["space_type", "count"],
        )
    )
    st.altair_chart(bar_chart, use_container_width=True)

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

if __name__ == "__main__":
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 1000)
    pd.set_option("display.max_colwidth", 1000)

    all_spaces = get_data(pickle_file)
    print(all_spaces.head(25))
