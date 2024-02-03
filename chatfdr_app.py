import streamlit as st
import requests
import os

# Set the chatPDF API key
secretkey = os.environ.get("DCM_API_KEY")

# Function to make the API request with a custom question
def make_api_request(question):
    url = 'http://documind.onrender.com/api-ask-from-collection'
    files = {
        'secretkey': (None, secretkey),
        'question': (None, question),
        'folder_id': (None, 'a62cadb4-5b79-4090-8097-06d546a0f0d5'),
        'enable_gpt4': (None, 'false')
    }

    response = requests.post(url, files=files)
    return response.text

# Streamlit app code
st.title('Chat with RAFOC documents')

# Add a text input for the user to enter the question
user_question = st.text_input('Enter your query')

# Add a button to trigger the API request
if st.button('Ask Question'):
    if user_question:
        response_text = make_api_request(user_question)
        st.write('API Response:')
        st.code(response_text)
    else:
        st.write('Please enter a question')
