import streamlit as st

pg = st.navigation(
    [
        st.Page("confluence_chat.py", title="Chat with EP Confluence", icon=":material/chat:"),
        st.Page("confluence_spaces.py", title="All EP Confluence Spaces", icon=":material/list:"),
    ]
)

pg.run()
