import os
from docx import Document

def convert_files_in_folder(input_folder, output_folder):
    """
    Convert all .docx files in the input_folder to .pdf files in the output_folder.
    
    Args:
        input_folder (str): The path to the input folder containing .docx files.
        output_folder (str): The path to the output folder where the .pdf files will be saved.
    
    Returns:
        None
    """
    for filename in os.listdir(input_folder):
        if filename.endswith(".docx"):
            input_file_path = os.path.join(input_folder, filename)
            output_filename = os.path.join(output_folder, filename.split(".docx")[0] + ".pdf")
            try:
                doc = Document(input_file_path)
                doc.save(output_filename)
                print(f'Successfully converted "{input_file_path}" to "{output_filename}"')
            except Exception as e:
                print(f'Error converting "{input_file_path}" to PDF: {e}')

# Convert files in the input folders to the output folders
input_folders = ['feb', 'mac', '.../dec']  # Replace with actual folder paths
output_folders = ['out-feb', 'out-mac', '.../out-dec']  # Replace with actual output folder paths

for i in range(len(input_folders)):
    convert_files_in_folder(input_folders[i], output_folders[i])
