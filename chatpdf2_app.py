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
    global source_id  # Declare source_id as a global variable

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
            source_id = response.json().get("sourceId")  # Update the global source_id
            st.write("Source:", source_id)
            render_chat_interface()
        else:
            st.error(f"Failed to upload PDF file. Status code: {response.status_code}")
            st.write("Error Details:", response.text)  # Display the response content for error details

def chatpdf_request(query):
    conversation.append({"role": "user", "content": query})
    data = {"referenceSources": True, "sourceId": source_id, "messages": conversation}
    response = requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"chatPDF API error: {response.status_code}")

# Define a function to render the chat interface
def render_chat_interface():
    global source_id
    # Get the user input
    user_input = st.text_input("Ask me a question:")
    # Try to send a request to the chatPDF API
    if st.button("Send"):
        try:
            response = chatpdf_request(user_input)
            # Display the response from the chatPDF API response.json()['content']
            messages = response.get("content")
            conversation.append({"role": "chatpdf", "content": messages})
        except Exception as e:
            st.write(f"API error: {e}")

    # Display the conversation history
    st.subheader("Chat History")
    for message in conversation:
        if message["role"] == "user":
            st.text_input("You:", message["content"], key=message)
        elif message["role"] == "chatpdf":
            st.text_area("ChatPDF:", message["content"], key=message)

if __name__ == "__main__":
    # upload file
    chatpdf_upload_file()
