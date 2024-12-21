import streamlit as st

from help_desk import HelpDesk

model = HelpDesk(new_db=True)

# Streamlit
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input("How can I help you?"):
    # Add prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Get answer
    result, sources = model.retrieval_qa_inference(prompt)

    # Add answer and sources
    st.chat_message("assistant").write(result + "  \n  \n" + sources)
    st.session_state.messages.append({"role": "assistant", "content": result + "  \n  \n" + sources})
