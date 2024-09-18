import streamlit as st
from pymongo import MongoClient
from chatbot_model import get_response, pred_class, words, classes, intents_json
from streamlit_chat import message

# MongoDB Atlas connection
client = MongoClient("mongodb+srv://mail4shavi:oZIBh7PlnSnY6OZ7@cluster0.6ccx5.mongodb.net/SIH?retryWrites=true&w=majority")
db = client["SIH"]
files_collection = db["uploaded_files"]

# Set the title of the app
st.title("RailResolve Management Chatbot")

# Initialize the chat history if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
if "collecting_details" not in st.session_state:
    st.session_state.collecting_details = False
if "complaint_details" not in st.session_state:
    st.session_state.complaint_details = {}

# Display the chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.write(f"**You:** {msg['content']}")
    else:
        st.write(f"**Bot:** {msg['content']}")

# Sidebar for file upload
st.sidebar.title("Upload Complaint Details")
uploaded_file = st.sidebar.file_uploader("Upload a file (optional)", type=["txt", "pdf", "docx","png","jpg","jpeg"])

# Handling file upload
if uploaded_file is not None:
    # Read the file as bytes
    file_bytes = uploaded_file.read()
    
    # Store the file in MongoDB
    files_collection.insert_one({
        "filename": uploaded_file.name,
        "file": file_bytes,
        "content_type": uploaded_file.type
    })
    st.sidebar.success("File uploaded successfully!")

# User input
user_input = st.chat_input("You:")

# Handling user input and file upload
if user_input:
    # Append the user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Check if we are collecting details
    if st.session_state.collecting_details:
        # Collecting the user's complaint details step by step
        if "name" not in st.session_state.complaint_details:
            st.session_state.complaint_details["name"] = user_input
            bot_response = "Thank you. Please provide your contact information."
        elif "contact" not in st.session_state.complaint_details:
            st.session_state.complaint_details["contact"] = user_input
            bot_response = "Thank you. Please provide your train number."
        elif "train_no" not in st.session_state.complaint_details:
            st.session_state.complaint_details["train_no"] = user_input
            bot_response = "Thank you. Please provide your seat number."
        elif "seat_no" not in st.session_state.complaint_details:
            st.session_state.complaint_details["seat_no"] = user_input
            bot_response = "Thank you. Please provide your coach number."
        elif "coach" not in st.session_state.complaint_details:
            st.session_state.complaint_details["coach"] = user_input
            bot_response = f"Thank you for providing the details:\n{st.session_state.complaint_details}"
            st.session_state.collecting_details = False  # Stop collecting details
        else:
            bot_response = "I'm sorry, I didn't quite get that. Can you please provide the information again?"

        # Append the bot response
        st.session_state.messages.append({"role": "bot", "content": bot_response})
    else:
        # Get the bot response based on user input
        intents_list = pred_class(user_input, words, classes)
        bot_response = get_response(intents_list, intents_json)

        if "file_complaint" in intents_list:
            bot_response = "Please provide your name, contact information, train number, seat number, and coach."
            st.session_state.collecting_details = True  # Start collecting details

        # Append the bot response
        st.session_state.messages.append({"role": "bot", "content": bot_response})

# Button to redirect to complaint form

st.sidebar.title("Register Complaint")
if st.sidebar.button("Click Here"):
    st.query_params(action="redirect")
    st.sidebar.markdown('<a href="https://complain-bot-1.onrender.com/" target="_self">Redirecting...</a>', unsafe_allow_html=True)


# Clear the text input for the next message
st.session_state.text_input = ""
