import streamlit as st
import time
import requests
import uuid  # to create a unique session_id

# Page config
st.set_page_config(page_title="Simple Chatbot", page_icon="💬", layout="centered")

# Title
st.markdown("<h1 style='text-align: center;'>Mohamed Mahmoud Chatbot</h1>", unsafe_allow_html=True)

# Store session_id (so the backend can keep history)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Store messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("What is on your mind?"):
    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Bot thinking animation
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")

        try:
            # Send to FastAPI
            response = requests.post(
                "http://127.0.0.1:8000/match",
                json={"job_description": prompt, "n_results": 5}
            )

            if response.status_code == 200:
                answer = response.json()["answer"]
            else:
                answer = "❌ Error from API"

        except Exception as e:
            answer = f"⚠️ Could not connect to API: {e}"

        time.sleep(1)  # Just for animation
        message_placeholder.markdown(answer)

    # Save bot response
    st.session_state.messages.append({"role": "assistant", "content": answer})
