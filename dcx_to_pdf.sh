#!/bin/bash

# Iterate through each folder (feb, mar, apr, etc.)
for folder in feb mar apr ; do
    # Create pdf sub-folder if it doesn't exist
    mkdir -p $folder/pdf
    
    # Iterate through each docx file in the current folder
    for file in $folder/*.docx ; do
        # Get the filename without extension
        filename=$(basename $file .docx)
        
        # Convert docx to pdf using unoconv cli
        unoconv -f pdf -o $folder/pdf $file
    done
done