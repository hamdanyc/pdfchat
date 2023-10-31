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
source_id = None

def chatpdf_upload_file():
    global source_id
    # upload pdf File
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # Display the uploaded file
        st.write("Uploaded file:", uploaded_file.name)
        # Define the headers with your API key
        headers = {"x-api-key": chatpdf_api_key}
        # Prepare the PDF file to be sent
        files = {"file": uploaded_file}
        response = requests.post(
        'https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)

        # Check the response
        if response.status_code == 200:
            st.success("PDF file uploaded successfully.")
            # You can access the response content if needed
            # st.write("Response:", response.json())
            source_id = response.json().get("sourceId")
            st.write("Source:", source_id)
            render_chat_interface()
        else:
            st.error(f"Failed to upload PDF file. Status code: {response.status_code}")
            st.write("Error Details:", response.text)  # Display the response content for error details

def chatpdf_request(query):
    conversation.append({"role": "user", "content": query})
    st.write("Source:", source_id)
    data = {"referenceSources": True,"sourceId": source_id,"messages": conversation}
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
        st.write(f"API error: {e}")

if __name__ == "__main__":
    # upload file
    chatpdf_upload_file()
