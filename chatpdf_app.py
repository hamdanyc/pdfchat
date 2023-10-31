import streamlit as st
import os
import requests

# Set the chatPDF API key
chatpdf_api_key = os.environ.get("CHATPDF_API_KEY")

def chatpdf_upload_file():
    # upload pdf File
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.write("Uploaded file:", uploaded_file.name)
        source_id = upload_pdf(uploaded_file, chatpdf_api_key)
        if source_id:
            render_chat_interface(source_id)

def upload_pdf(uploaded_file, api_key):
    headers = {"x-api-key": api_key}
    files = {"file": uploaded_file}
    response = requests.post('https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
    if response.status_code == 200:
        st.success("PDF file uploaded successfully.")
        return response.json().get("sourceId")
    else:
        st.error(f"Failed to upload PDF file. Status code: {response.status_code}")
        st.write("Error Details:", response.text)
        return None

def chatpdf_request(source_id, user_input, api_key):
    headers = {"x-api-key": api_key}
    conversation = [{"role": "user", "content": user_input}]
    data = {"referenceSources": True, "sourceId": source_id, "messages": conversation}
    response = requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"chatPDF API error: {response.status_code}")

def render_chat_interface(source_id):
    user_input = st.text_input("Ask me a question:")
    if st.button("Send"):
        try:
            response = chatpdf_request(source_id, user_input, chatpdf_api_key)
            messages = response.get("content")
            st.write(f"{messages}")
        except Exception as e:
            st.write(f"API error: {e}")

if __name__ == "__main__":
    st.title("chatPDF App")
    chatpdf_upload_file()
