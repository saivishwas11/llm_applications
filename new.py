from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions
from google.generativeai.types import GenerationConfig

# Load API key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Configuration ---
if not GOOGLE_API_KEY:
    st.error("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-1.5-flash"

# --- Initialize chat history in Streamlit's session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    st.session_state.chat_history.append({"role": "bot", "text": "Hello! I'm here to provide general information and support regarding mental health topics. How can I help you today?", "is_intro": True})

# --- Define the System Instruction for Mental Health Focus and Brevity ---
SYSTEM_INSTRUCTION = """
You are a supportive, empathetic, and informative mental health awareness and information assistant.
Your primary goal is to provide general knowledge about mental health topics, discuss coping strategies, promote well-being, and offer encouragement.

Keep your responses concise, brief, and to the point, ideally within 5 to 8 lines. Avoid overly long paragraphs or detailed explanations unless specifically requested.

Strictly adhere to the following guidelines:
1.  **Focus Solely on Mental Health:** Only discuss topics related to mental health. If a user asks about something else, politely state that you can only provide information on mental health.
2.  **No Medical Advice or Diagnosis:** You are NOT a substitute for a licensed mental health professional, therapist, counselor, or doctor. You CANNOT diagnose any mental health condition, provide medical advice, or recommend specific treatments.
3.  **No Crisis or Emergency Handling:** You are NOT a crisis hotline or emergency service. If a user expresses suicidal thoughts, intent to harm themselves or others, or is in any form of immediate crisis, you MUST provide contact information for crisis resources (like a national suicide prevention hotline) or advise them to contact emergency services (e.g., 911 or their local equivalent) or a trusted adult/professional IMMEDIATELY. State clearly that you are not equipped to handle emergencies. Do NOT attempt to provide therapy or crisis intervention yourself.
4.  **General Information Only:** Provide general information based on common knowledge about mental health. Avoid discussing specific personal situations or providing tailored advice that would require a professional assessment.
5.  **Supportive and Non-Judgmental Tone:** Maintain a compassionate, understanding, and non-judgmental demeanor.
6.  **Refer to Professionals:** Encourage users to consult with qualified mental health professionals for personalized support, diagnosis, and treatment.
7.  **Safety First:** Your responses must prioritize the safety and well-being of the user.
"""

# --- Define Generation Configuration for Brevity ---
BRIEF_GENERATION_CONFIG = GenerationConfig(
    max_output_tokens=200, # Adjust this value as needed
    temperature=0.7,
)


# --- Streamlit Sidebar (Top Left) ---
with st.sidebar:
    # === Add Logo ===
    logo_path = "C:\\Users\\saivi\\Downloads\\download.png" # <-- CHANGE THIS LINE! (e.g., "logo.png" if in same dir)
    # Recommended width for sidebar logos is usually 150-250px
    desired_logo_width = 100 # Pixels

    if os.path.exists(logo_path):
         st.image(logo_path, width=desired_logo_width) # Using width parameter
    else:
         st.warning(f"Logo not found at {logo_path}. Please update the path or use a URL.")
         st.markdown("## Your Logo Here") # Placeholder text


    # --- Chat History Dashboard Section (Moved to Sidebar) ---
    st.subheader("Conversation History")

    # Optional: Add a button to clear the history
    def clear_chat_history():
         st.session_state.chat_history = []
         st.session_state.chat_history.append({"role": "bot", "text": "Hello! I'm here to provide general information and support regarding mental health topics. How can I help you today?", "is_intro": True})
         st.rerun()

    st.button("Clear Conversation", on_click=clear_chat_history)

    # Display the messages from session_state in the sidebar (formatted text)
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**User:** {message['text']}")
        else: # role == "bot"
            st.markdown(f"**Assistant:** {message['text']}")
        st.markdown("---") # Add a separator between messages


# --- Main Content Area ---
st.title("Mental Health Awareness Assistant")
st.markdown("### Your guide to understanding mental well-being.")

# --- Initialize the Gemini model and the chat session ---
try:
    model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_INSTRUCTION)

    api_history = []
    for msg in st.session_state.chat_history:
        if msg.get("is_intro", False):
             continue
        if msg["role"] in ["user", "bot"]:
             role = "user" if msg["role"] == "user" else "model"
             api_history.append({"role": role, "parts": [msg["text"]]})

    chat = model.start_chat(history=api_history)

except Exception as e:
    st.error(f"Error initializing model or chat: {e}")
    st.stop()

# --- Display immediate/latest chats in the main view ---
st.subheader("Current Conversation")
# Define how many latest messages to display in the main area
num_latest_messages = 2 # Last user input + last bot response

# Iterate through the last 'num_latest_messages' from chat_history
# Use max(0, ...) to avoid negative indexing if history is smaller than num_latest_messages
for message in st.session_state.chat_history[max(0, len(st.session_state.chat_history) - num_latest_messages):]:
    # Map our stored roles ('user', 'bot') to st.chat_message roles ('user', 'assistant')
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["text"])


# --- Chat Input Area (Main Area) ---
user_input = st.chat_input("Ask about mental health topics...")

# --- Handle New Input and Response ---
if user_input:
    # Save user message to history
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Get response from Gemini
    with st.spinner("Thinking..."):
        try:
            response = chat.send_message(user_input, generation_config=BRIEF_GENERATION_CONFIG)
            bot_response_text = response.text

        except exceptions.GoogleAPIError as e:
             bot_response_text = f"An API error occurred: {e}"
             st.error(bot_response_text)
        except Exception as e:
             bot_response_text = f"An unexpected error occurred: {e}"
             st.error(bot_response_text)

    # Save bot response to history
    st.session_state.chat_history.append({"role": "bot", "text": bot_response_text})

    # --- Rerun the app to update both sidebar and main view history ---
    st.rerun()