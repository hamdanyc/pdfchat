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
    available_questions = ["What is the article about?",
        "what are the key applications of machine learning which mentioned in the article?",
        "What are the important findings from the literature review of the article. Briefly explain the finding.",
        "What are the challenges and benefits of implementing machine learning, as discussed in the article?",
        "Provide an overview of the technologies and algorithms used for machine learning, as described in the article.",
        "Discuss the impact of machine learning according to the article.",
        "Explain the ethical considerations and data privacy issues associated with machine learning, based on the article.",
        "Can you extract statistics or figures related to the success rates of machine learning models from the article?",
        "Summarize any case studies or real-world examples of machine learning applications that are discussed in the article.",
        "What trends or future developments in machine learning does the article highlight?",
        "Provide information on any regulatory or compliance requirements for machine learning in healthcare mentioned in the article.",
        "Summarize the conclusions and recommendations made in the article regarding the use of machine learning.",
        "Suggest a related readings on the subject mentioned in the article",
        "Other"]
    selected_question = st.selectbox("Select a question:", available_questions)

    if selected_question == "Other":
        user_input = st.text_input("Ask me a question:")
    else:
        user_input = selected_question

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
