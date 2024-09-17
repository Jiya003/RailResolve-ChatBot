import streamlit as st
from chatbot_model import ChatbotModel

st.title("Indian Railway General Query and Complaint Management Chatbot")

# Load the chatbot model
chatbot = ChatbotModel(intents_file="intents.json")
chatbot.train_model()

# Function to handle user input
def get_response(user_input):
    prediction = chatbot.classify(user_input)
    return prediction

# User input box
user_input = st.text_input("Ask your railway query here:")

if st.button("Send"):
    response = get_response(user_input)
    st.write(response)
