from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions

# Load API key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Configuration ---
if not GOOGLE_API_KEY:
    st.error("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop() # Stop execution if key is missing

genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-1.5-flash" # Or "gemini-pro" or "gemini-1.0-pro"

# --- Streamlit UI setup ---
st.set_page_config(page_title="Q&A Chatbot", page_icon=":robot_face:")
st.title("Q&A Chatbot")
st.header("Ask me anything!")

# Initialize chat history in Streamlit's session state
# This history is used for displaying and for initializing the model's chat object
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize the Gemini model and the chat session
# This happens on every rerun, but we initialize the chat history from session_state
try:
    model = genai.GenerativeModel(model_name=MODEL_NAME)

    # Convert our session_state history format to the API's expected format
    api_history = []
    for msg in st.session_state.chat_history:
        # The API expects 'user' and 'model' roles
        role = "user" if msg["role"] == "user" else "model"
        api_history.append({"role": role, "parts": [msg["text"]]})

    chat = model.start_chat(history=api_history) # Pass the history to the chat object

except Exception as e:
    st.error(f"Error initializing model or chat: {e}")
    st.stop()

# --- Chat Input Area ---
# Use st.chat_input for a nicer mobile-friendly input at the bottom
# This input appears below the history dashboard
user_input = st.chat_input("Type your question here:")

# --- Handle New Input and Response ---
# st.chat_input returns the value directly when Enter is pressed
if user_input:
    # Display user message immediately in the chat messages area below
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message to history
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Get response from Gemini using the chat object
    with st.spinner("Thinking..."): # Show a spinner while waiting for the response
        try:
            # Use chat.send_message to maintain conversation context
            response = chat.send_message(user_input)
            bot_response_text = response.text

        except exceptions.GoogleAPIError as e:
             bot_response_text = f"An API error occurred: {e}"
             st.error(bot_response_text) # Show error in UI
        except Exception as e:
             bot_response_text = f"An unexpected error occurred: {e}"
             st.error(bot_response_text) # Show error in UI

    # Display bot response in the chat messages area
    with st.chat_message("assistant"): # Use 'assistant' role for the bot message style
        st.markdown(bot_response_text)

    # Save bot response to history
    st.session_state.chat_history.append({"role": "bot", "text": bot_response_text})

    # --- Important: Rerun the app to update the history display ---
    # When using st.chat_input and manually adding messages,
    # rerunning after handling a new message ensures the full history
    # (including the new messages) is re-rendered by the display loop below.
    st.rerun()


# --- Chat History Dashboard Section ---
st.subheader("Chat History Dashboard")

# Optional: Add a button to clear the history
if st.button("Clear History"):
    st.session_state.chat_history = [] # Clear the session state history
    st.rerun() # Rerun the app to apply the change and clear the displayed history

# Display the entire history from session_state
# This loop runs on every rerun and renders all messages stored in session_state
for message in st.session_state.chat_history:
    # Map our stored roles ('user', 'bot') to st.chat_message roles ('user', 'assistant')
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["text"]) # Use markdown to render potential formatting