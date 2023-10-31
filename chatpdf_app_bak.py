# chatpdf_app.py
# streamlit run chatpdf_app.py

import streamlit as st
import os
import requests

# Set the chatPDF API key
chatpdf_api_key = os.environ.get("CHATPDF_API_KEY")
conversation = []
headers = {
    "x-api-key": chatpdf_api_key,
    "Content-Type": "application/json"
}
st.title("chatPDF App")

def chatpdf_request(query):
    # headers = {"x-api-key": "{chatpdf_api_key}","Content-Type": "application/json",}
    conversation.append({"role": "user", "content": query})
    data = {"referenceSources": True,"sourceId": "cha_pc39qI9E01JoNDKXn6rgv","messages": conversation}
    response = requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"chatPDF API error: {response.status_code}")

# Define a function to render the chat interface
def render_chat_interface():
    # Get the user input
    user_input = st.text_input("Ask me a question:")

    # Try to send a request to the chatPDF API
    try:
        response = chatpdf_request(user_input)
        # Display the response from the chatPDF API response.json()['content']
        messages = response.get("content")
        st.write(f"{messages}")
    except Exception as e:
        st.write(f"chatPDF API error: {e}")

if __name__ == "__main__":
    # Render the chat interface
    render_chat_interface()
