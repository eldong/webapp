"""
Document Intelligence
"""
import streamlit as st
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient
import base64
import os


# Azure Storage Account details 
DOCUMENT_STORAGE_CONNECTIONSTRING = os.getenv("DOCUMENT_STORAGE_CONNECTIONSTRING")
TEMPLATE_DOCUMENT_CONTAINER = os.getenv("STORAGE_ACCOUNT_CONTAINER")
TEMPLATE_DOCUMENT_QUEUE = os.getenv("TEMPLATE_DOCUMENT_QUEUE")

# Function to upload file to Azure Storage
def upload_to_azure_storage(files):
    
    total_files = len(files)
    progress_bar = st.progress(0)

    for i, file in enumerate(files):
        blob_service_client = BlobServiceClient.from_connection_string(f"{DOCUMENT_STORAGE_CONNECTIONSTRING}")
        blob_client = blob_service_client.get_blob_client(container=TEMPLATE_DOCUMENT_CONTAINER, blob=file.name)
        blob_client.upload_blob(file, overwrite=True)
        
        # Update the progress bar
        percent_complete = (i + 1) / total_files
        progress_bar.progress(percent_complete)
        
        st.markdown(f"**{file.name}** ✅ uploaded successfully")
        
def update_status_in_queue():
    message = base64_encode("done")
       
    queue_service_client = QueueServiceClient.from_connection_string(f"{DOCUMENT_STORAGE_CONNECTIONSTRING}")
    queue_client = queue_service_client.get_queue_client(TEMPLATE_DOCUMENT_QUEUE)
    queue_client.send_message( message)


def base64_encode(plain_text):
    plain_text_bytes = plain_text.encode('utf-8')
    return base64.b64encode(plain_text_bytes).decode('utf-8')

st.title("Document Intelligence")

uploaded_files = st.file_uploader("Choose a file(s)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_files:
    upload_to_azure_storage(uploaded_files)
    
    #Upload status to queue
    update_status_in_queue()      
    
    st.success("File uploaded to Azure Storage!")    # Add your file processing code here
