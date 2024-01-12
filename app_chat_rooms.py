import streamlit as st
from streamlit_server_state import server_state, server_state_lock
from streamlit_recorder import st_recorder

# Set up initial state
with server_state_lock["chat_messages"]:
    if "chat_messages" not in server_state:
        server_state["chat_messages"] = []

# Sidebar for user nickname input
st.sidebar.header("User Settings")
nickname = st.sidebar.text_input("Nickname", key="nickname")
if not nickname:
    st.stop()

# Function to handle message input
def on_message_input():
    new_message_text = st.session_state["message_input"]
    if not new_message_text:
        return

    new_message_packet = {
        "nickname": nickname,
        "text": new_message_text,
    }
    with server_state_lock["chat_messages"]:
        server_state["chat_messages"] = server_state["chat_messages"] + [
            new_message_packet
        ]

# Main chat interface
st.title("Chat Room")

# Display chat messages
with st.beta_expander("Chat Messages"):
    for message in server_state["chat_messages"]:
        st.text(f"{message['nickname']}: {message['text']}")

# Message input with recording functionality
message_input = st.text_input("Message", key="message_input", on_change=on_message_input)

# Audio recording button
recording_state = st_recorder(message_input, start_recording=False, key="recorder")
if recording_state.is_recording:
    st.info("Recording...")

# Display recorded audio
if recording_state.audio_data:
    st.audio(recording_state.audio_data, format="audio/wav")

# Reset recording when a new message is submitted
if recording_state.is_recording and message_input:
    recording_state.clear()

# Submit button
if st.button("Send Message"):
    on_message_input()
    st.session_state.message_input = ""

# Display current chat messages
st.write("Current Chat Messages:", server_state["chat_messages"])
