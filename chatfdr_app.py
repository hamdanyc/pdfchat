import streamlit as st
import requests
import os
import json

# Set the chatPDF API key
secretkey = os.environ.get("DCM_API_KEY")

# Function to make the API request with a custom question
def make_api_request(question):
    url = 'http://documind.onrender.com/api-ask-from-collection'
    data = {
        'secretkey': secretkey,
        'question': question,
        'folder_id': 'a62cadb4-5b79-4090-8097-06d546a0f0d5',
        'enable_gpt4': 'false'
    }

    response = requests.post(url, data=data)

    # Check if the response is successful
    if response.status_code == 200:
        return response.json()['data']['answer']
    else:
        raise Exception(f"API error: {response.status_code}")
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
        st.text_area('Response', value=response_text, height=300)
    else:
        st.write('Please enter a question')
