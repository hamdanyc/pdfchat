import gdown
import os
from googleapiclient.discovery import build

# Replace with your OAuth 2.0 client ID and secret
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

# Function to download Google Doc by ID and convert to PDF
def download_and_convert(file_id, output_filename):
    try:
        # Download Google Doc
        gdown.download(f'https://drive.google.com/uc?id={file_id}', output_filename)

        # Convert downloaded file to PDF (assuming .docx format)
        from docx import Document
        doc = Document(output_filename)
        doc.save(output_filename + '.pdf')

        print(f'Successfully downloaded and converted "{file_id}" to "{output_filename}.pdf"')
    except Exception as e:
        print(f'Error downloading/converting "{file_id}": {e}')

# Function to recursively convert and download Google Docs from folders
def convert_folder(folder_id):
    service = build('drive', 'v3', credentials=authorize(CLIENT_ID, CLIENT_SECRET))
    files = service.files().list(q=f"'{folder_id}' in parents").execute().get('files', [])

    for file in files:
        file_id = file['id']
        filename = file['name']

        if file['mimeType'] == 'application/vnd.google-apps.document':
            output_filename = 'out/' + filename + '.docx'  # Assuming Google Doc format
            download_and_convert(file_id, output_filename)
        elif file['mimeType'] == 'application/vnd.google-apps.folder':
            convert_folder(file_id)  # Recursively process subfolders

# Authorization function (replace with your preferred method)
def authorize(client_id, client_secret):
    # Use your preferred method to get an access token (e.g., flow_from_client_secrets)
    from google.oauth2 import service_account
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = service_account.Credentials.from_service_account_file(
        '/home/abi/nfs/Oaut_json', scopes=scope)
    return credentials

# Folder ID(s) to process (replace with your folder IDs)
folder_ids = ['FOLDER_ID_1', 'FOLDER_ID_2', ...]

for folder_id in folder_ids:
    convert_folder(folder_id)
