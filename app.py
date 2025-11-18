"""
Thoughtful AI Support Agent - Streamlit Web Interface

This module provides a web-based chat interface for the Thoughtful AI Support Agent.
Users can ask questions about Thoughtful AI's products and receive intelligent,
context-aware responses with reasoning transparency.

Features:
- Chat interface with message history
- Session-based conversation memory
- Expandable reasoning view showing confidence and thought process
- Clean, user-friendly UI

Author: Kyle M.
"""

import streamlit as st
import uuid
from agent import get_agent

# Page configuration
st.set_page_config(page_title="Thoughtful AI Support", page_icon="🤖")

st.title("Thoughtful AI Support Agent 🤖")
st.markdown("Ask me about Thoughtful AI's agents like EVA, CAM, and PHIL!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    st.session_state.agent = get_agent()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                response = st.session_state.agent.invoke(
                    {"messages": [{"role": "user", "content": prompt}]},
                    config
                )
                
                # Extract the answer from the structured response
                structured_res = response["structured_response"]
                answer = structured_res.answer
                
                # Optional: Display reasoning/confidence in an expander
                with st.expander("Agent Reasoning"):
                    st.write(f"**Confidence:** {structured_res.confidence}")
                    st.write(f"**Reasoning:**")
                    for step in structured_res.reasoning:
                        st.write(f"- {step}")
                
                st.markdown(answer)
                
                # Add assistant response to state
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
