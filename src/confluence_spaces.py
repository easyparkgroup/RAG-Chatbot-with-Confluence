import os
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from src.get_confluence_spaces import get_spaces_data

load_dotenv()

# Load environment variables
username = os.getenv("CONFLUENCE_USERNAME")
api_token = os.getenv("CONFLUENCE_API_KEY")
base_url = os.getenv("CONFLUENCE_BASE_URL").rstrip("/")
datadir = Path(__file__).parent.parent / "data"
pickle_file = Path(datadir / "spaces.pkl")


df = get_spaces_data(pickle_file)
display_df = df.copy()


col1, col2 = st.columns(2)

# create toggle to hide personal spaces
if st.checkbox("Hide personal spaces", value=True):
    display_df = display_df[~display_df["space_type"].str.contains("personal", case=False)]

with col1:
    # create an altair bar chart to show the distribution of space last modified dates
    st.write("Distribution of last modified dates")
    display_df["last_modified"] = pd.to_datetime(display_df["last_modified"])
    date_counts = display_df["last_modified"].dt.date.value_counts().reset_index()
    date_counts.columns = ["date", "count"]
    date_counts = date_counts.sort_values("date")
    bar_chart = (
        alt.Chart(date_counts)
        .mark_bar()
        .encode(
            x=alt.X(field="date", type="temporal"),
            y=alt.Y(field="count", type="quantitative"),
            tooltip=["date", "count"],
        )
    )
    st.altair_chart(bar_chart, use_container_width=True)
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
        "page_count": st.column_config.NumberColumn("Page Count", width="small"),
        "last_modified": st.column_config.DateColumn("Last Modified", width="medium"),
    },
)
