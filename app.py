import streamlit as st
from chatbot_model import get_response, pred_class, words, classes, intents_json

# My Streamlit app
st.title("RailResolve Management Chatbot")

# For Initializing the chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying the chat history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"**You:** {message['content']}")
    else:
        st.write(f"**Bot:** {message['content']}")

# User input
user_input = st.text_input("You:", "")

# Handling the user input
if st.button("Send"):
    if user_input:
        # Appending the user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Getting the bot response
        intents_list = pred_class(user_input, words, classes)  # Ensure this returns a list
        bot_response = get_response(intents_list, intents_json)  # Pass intents_list and intents_json
        
        # Appending the bot response
        st.session_state.messages.append({"role": "bot", "content": bot_response})
    st.session_state.text_input = ""

       
