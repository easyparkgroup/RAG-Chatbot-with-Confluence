import streamlit as st

pg = st.navigation(
    [
        st.Page("confluence_chat.py", title="Chat with EP Confluence", icon=":material/chat:"),
    ]
)

pg.run()
