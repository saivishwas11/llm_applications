from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
from google.api_core import exceptions
# Import GenerationConfig
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

# --- Define the System Instruction for Mental Health Focus and Brevity ---
SYSTEM_INSTRUCTION = """
You are a supportive, empathetic, and informative mental health awareness and information assistant.
Your primary goal is to provide general knowledge about mental health topics, discuss coping strategies, promote well-being, and offer encouragement.

**Keep your responses concise, brief, and to the point, ideally within 5 to 8 lines.** Avoid overly long paragraphs or detailed explanations unless specifically requested.

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
# Estimate: A line is roughly 10-25 tokens. 8 lines * 25 tokens/line = 200 tokens.
# Let's set max_output_tokens to a reasonable limit for brief responses.
BRIEF_GENERATION_CONFIG = GenerationConfig(
    max_output_tokens=200, # Adjust this value as needed (e.g., 150, 250)
    # You could also adjust temperature or top_p here if desired, but max_output_tokens is key for length
    temperature=0.7, # Example: slightly lower temp can sometimes lead to more direct answers
)


# --- Streamlit UI setup ---
st.set_page_config(page_title="Mental Health Awareness Assistant", page_icon=":brain:")
st.title("Mental Health Awareness Assistant")
st.markdown("### Your guide to understanding mental well-being.")

# --- Important Disclaimers ---
st.warning("""
**Please Read:**
I am an AI assistant focused on providing general information and awareness about mental health topics.
*   **I am NOT a substitute for professional medical advice, diagnosis, or treatment.**
*   **I CANNOT help in a crisis or emergency.** If you are in distress, having thoughts of harming yourself or others, please contact a crisis hotline or seek immediate professional help (call emergency services like 911 or your local equivalent).
*   The information I provide is general and should not be taken as personalized medical advice.
*   Always consult with a qualified mental health professional for any health concerns or before making decisions related to your health.
""", icon="⚠️")

# Initialize chat history in Streamlit's session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    # Optional: Add an initial greeting message from the bot
    st.session_state.chat_history.append({"role": "bot", "text": "Hello! I'm here to provide general information and support regarding mental health topics. How can I help you today?", "is_intro": True})


# --- Initialize the Gemini model and the chat session ---
# The system_instruction is passed when creating the model instance
try:
    model = genai.GenerativeModel(model_name=MODEL_NAME, system_instruction=SYSTEM_INSTRUCTION)

    # Convert our session_state history format to the API's expected format
    api_history = []
    for msg in st.session_state.chat_history:
        # Skip the very first "bot" message if it's just an intro and not meant for API history
        if msg.get("is_intro", False):
             continue

        # The API expects 'user' and 'model' roles, and 'parts' instead of 'text'
        role = "user" if msg["role"] == "user" else "model"
        api_history.append({"role": role, "parts": [msg["text"]]})

    # Start the chat with the history
    # The system_instruction is already applied to the 'model' object itself
    chat = model.start_chat(history=api_history)


except Exception as e:
    st.error(f"Error initializing model or chat: {e}")
    st.stop()

# --- Chat History Display Area ---
# Display the entire history from session_state first
st.subheader("Conversation History")

# Optional: Add a button to clear the history
def clear_chat_history():
     st.session_state.chat_history = []
     # Optional: Re-add the initial greeting after clearing
     st.session_state.chat_history.append({"role": "bot", "text": "Hello! I'm here to provide general information and support regarding mental health topics. How can I help you today?", "is_intro": True})
     st.rerun()

st.button("Clear Conversation", on_click=clear_chat_history)

# Display the messages using st.chat_message
for message in st.session_state.chat_history:
    # Map our stored roles ('user', 'bot') to st.chat_message roles ('user', 'assistant')
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["text"])


# --- Chat Input Area ---
user_input = st.chat_input("Ask about mental health topics...")

# --- Handle New Input and Response ---
if user_input:
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message to history
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Get response from Gemini using the chat object
    with st.spinner("Thinking..."):
        try:
            # Use chat.send_message and pass the generation_config
            response = chat.send_message(user_input, generation_config=BRIEF_GENERATION_CONFIG) # <-- Pass the config here!
            bot_response_text = response.text

        except exceptions.GoogleAPIError as e:
             bot_response_text = f"An API error occurred: {e}"
             st.error(bot_response_text)
        except Exception as e:
             bot_response_text = f"An unexpected error occurred: {e}"
             st.error(bot_response_text)

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_response_text)

    # Save bot response to history
    st.session_state.chat_history.append({"role": "bot", "text": bot_response_text})

    # --- Rerun the app to update the history display ---
    st.rerun()