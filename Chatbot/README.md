# Streamlit Mental Health Support Assistant

This is a Streamlit web application that acts as an AI assistant providing **general** information and support related to mental health awareness and well-being. It uses the Google Gemini API to generate responses.

**Please Note:** This application is for informational purposes only and is **NOT** a substitute for professional medical advice, diagnosis, or treatment. It is **NOT** equipped to handle crises or emergencies.

## Features

*   Provides general information on mental health topics and well-being strategies.
*   Maintains a conversation history displayed in the sidebar.
*   Allows clearing the conversation history.
*   Utilizes the Google Gemini API (`gemini-1.5-flash` by default).
*   Configured to provide concise and brief responses (5-8 lines ideally).
*   Strictly adheres to safety guidelines: no medical advice, no diagnosis, no crisis handling.

## Prerequisites

Before running this application, you need:

1.  **Python 3.7+**: Install Python from [python.org](https://www.python.org/).
2.  **pip**: Python's package installer (usually comes with Python).
3.  **Google Cloud/Gemini API Key**: Obtain an API key from the Google AI Studio or Google Cloud Platform. You can get started at [https://aistudio.google.com/](https://aistudio.google.com/) or the Google Cloud Console.
4.  **Internet Connection**: Required to interact with the Google Gemini API.

## Installation

1.  **Save the code**: Save the provided Python code as a file, for example, `app.py`.
2.  **Create a requirements file**: Create a file named `requirements.txt` in the same directory as `app.py` with the following content:

    ```
    streamlit
    google-generativeai
    python-dotenv
    ```

3.  **Install dependencies**: Open your terminal or command prompt, navigate to the directory where you saved the files, and run:

    ```bash
    pip install -r requirements.txt
    ```

## Setup

1.  **Get your Google API Key**: If you haven't already, get your `GOOGLE_API_KEY` from Google AI Studio or GCP.
2.  **Create a `.env` file**: In the same directory as `app.py` and `requirements.txt`, create a file named `.env`.
3.  **Add your API key to `.env`**: Open the `.env` file and add the following line, replacing `YOUR_GOOGLE_API_KEY` with your actual key:

    ```dotenv
    GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
    ```
    **Important:** Do not share your `.env` file or commit it to version control like Git.

4.  **Update Logo Path (Optional but recommended):**
    In the `app.py` file, find the line:
    ```python
    logo_path = "used my local image path" # <-- CHANGE THIS LINE!
    ```
    Change the path `"C:\\Users\\saivi\\Downloads\\download.png"` to the actual path of your logo image file on your system, or place a logo image (e.g., `logo.png`) in the same directory as `app.py` and change the line to:
    ```python
    logo_path = "logo.png" # Example: If logo.png is in the same directory
    ```
    If you don't update the path or the file isn't found, the app will display a warning and placeholder text instead of the logo.

## How to Run

1.  Open your terminal or command prompt.
2.  Navigate to the directory where you saved `app.py`.
3.  Run the Streamlit application using the command:

    ```bash
    streamlit run app.py
    ```

4.  Your web browser should open automatically to the application (usually at `http://localhost:8501`).

## Usage

1.  The application will load in your web browser.
2.  An introductory message from the assistant will appear.
3.  Type your general questions about mental health topics, coping strategies, or well-being into the chat input box at the bottom of the main area.
4.  Press Enter or click the send button.
5.  The assistant's brief response will appear above your message.
6.  The full conversation history will be visible in the sidebar on the left.
7.  Use the "Clear Conversation" button in the sidebar to start a new chat session.

## Important Limitations and Safety Information

*   **NOT a Medical Professional:** This AI cannot provide medical advice, diagnose conditions, or replace consultation with a licensed therapist, counselor, or doctor. Always seek the advice of a qualified professional for any health concerns.
*   **NO Crisis Support:** This application is **NOT** a crisis hotline or emergency service. If you are in danger, having thoughts of harming yourself or others, or experiencing a mental health emergency:
    *   **Call emergency services immediately (e.g., 911 in the US, or your local equivalent).**
    *   **Contact a crisis hotline or suicide prevention line.** Examples include:
        *   National Suicide Prevention Lifeline (US): Call or text 988
        *   Crisis Text Line (US): Text HOME to 741741
        *   *(Find local crisis resources specific to your region)*
    *   **Go to the nearest emergency room.**
    *   **Reach out to a trusted friend, family member, or professional.**
    **DO NOT rely on this application in a crisis.**
*   **General Information Only:** Responses are based on general knowledge and are not tailored to your specific personal situation.
*   **Brevity:** Responses are intentionally kept brief.
