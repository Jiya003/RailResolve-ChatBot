import streamlit as st
from chatbot_model import classify_intent, respond_to_intent

# Initialize user state
user_state = {}

# Function to handle chatbot conversation
def handle_chat(user_message, user_id):
    # Initialize user state if not exists
    if user_id not in user_state:
        user_state[user_id] = {}
    
    # Determine the intent of the user message
    intent = classify_intent(user_message)

    if intent == 'complaint_submission':
        user_state[user_id]['state'] = 'awaiting_complaint_details'
        return "To file a complaint, I'll need some details from you. Please provide the following information:\n1. What is the train number?\n2. On which date did the incident occur?\n3. Can you briefly describe the issue or incident?\n4. Is there any additional information you'd like to provide (e.g., location, staff involved)?"
    
    elif user_state[user_id].get('state') == 'awaiting_complaint_details':
        # Collecting information based on context
        if 'complaint_details' not in user_state[user_id]:
            user_state[user_id]['complaint_details'] = {}
        
        details = user_state[user_id]['complaint_details']
        
        if 'train_number' not in details:
            details['train_number'] = user_message
            return "On which date did the incident occur?"
        
        elif 'date' not in details:
            details['date'] = user_message
            return "Can you briefly describe the issue or incident?"
        
        elif 'description' not in details:
            details['description'] = user_message
            return "Is there any additional information you'd like to provide (e.g., location, staff involved)?"
        
        elif 'additional_info' not in details:
            details['additional_info'] = user_message
            user_state[user_id]['state'] = 'awaiting_confirmation'
            return f"Thank you for providing the details. Here is a summary of your complaint:\n- Train Number: {details['train_number']}\n- Date of Incident: {details['date']}\n- Description of the Issue: {details['description']}\n- Additional Details: {details['additional_info']}\nIs this information correct?"
    
    elif user_state[user_id].get('state') == 'awaiting_confirmation':
        if 'yes' in user_message.lower():
            user_state[user_id]['state'] = 'complaint_submitted'
            return "Your complaint has been successfully submitted. You will receive a reference number shortly. Thank you for bringing this to our attention."
        else:
            return "Please provide the correct details or let me know if you want to start over."

    else:
        return respond_to_intent(user_message)

# Streamlit UI setup
st.title("Indian Railway Complaint Management Chatbot")

# Initialize session state for user_id
if 'user_id' not in st.session_state:
    st.session_state.user_id = 'user_' + str(hash(st.session_state))

# Chat interface
user_message = st.text_input("You:", "")
if st.button("Send"):
    if user_message:
        response = handle_chat(user_message, st.session_state.user_id)
        st.write(f"Bot: {response}")

# Optional: Display chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if user_message:
    st.session_state.chat_history.append(("You", user_message))
    st.session_state.chat_history.append(("Bot", response))

for role, message in st.session_state.chat_history:
    st.write(f"{role}: {message}")

