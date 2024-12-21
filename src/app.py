import streamlit as st

pg = st.navigation(
    [
        st.Page("confluence_chat.py", title="Chat with EP Confluence", icon=":material/chat:"),
        st.Page("list_spaces.py", title="List EP Confluence Spaces", icon=":material/list:"),
    ]
)

pg.run()
