import streamlit as st
import uuid

from langchain_core.messages import HumanMessage
from agent.graph import graph

st.title("SQL Agent Chatbot")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])


user_input = st.chat_input("Ask something...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    result = graph.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )

    response = result["messages"][-1].content

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

    with st.chat_message("assistant"):
        st.write(response)