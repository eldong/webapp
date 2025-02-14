# utils.py

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.web.server.server import Server
import base64
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient
from azure.storage.blob import generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta, timezone
import os
import requests
import urllib.parse
import hmac
import hashlib


# Azure Storage Account details 
DOCUMENT_STORAGE_CONNECTIONSTRING = os.getenv("DOCUMENT_STORAGE_CONNECTIONSTRING")
TEMPLATE_DOCUMENT_CONTAINER = os.getenv("STORAGE_ACCOUNT_CONTAINER")
TEMPLATE_DOCUMENT_QUEUE = os.getenv("TEMPLATE_DOCUMENT_QUEUE")
STORAGE_ACCOUNT_OUTPUT_CONTAINER = os.getenv("STORAGE_ACCOUNT_OUTPUT_CONTAINER")


def generate_document_url(foldername, file_name, expiry_minutes=60):
    """
    Generates a URL with a SAS token for the specified blob.
    
    Parameters:
        foldername (str): The folder (or virtual directory) in the container.
        file_name (str): The name of the uploaded file.
        expiry_minutes (int): How many minutes until the SAS token expires.
    
    Returns:
        str: A URL that provides access to the blob.
    """

    # Make sure these variables are imported or defined in your module.
    
    account_info = extract_account_info(DOCUMENT_STORAGE_CONNECTIONSTRING)
    DOCUMENT_STORAGE_ACCOUNT = account_info.get("AccountName")
    DOCUMENT_STORAGE_ACCOUNT_KEY = account_info.get("AccountKey")

    # Replace the file extension with ".md"
    base_name, _ = os.path.splitext(file_name)
    out_file_name = base_name + "-final-insights" + ".md"

    encoded_out_file_name = urllib.parse.quote(out_file_name)
    sas_token = generate_blob_sas(
        account_name=DOCUMENT_STORAGE_ACCOUNT,
        container_name=STORAGE_ACCOUNT_OUTPUT_CONTAINER,
        blob_name=f"{foldername}/{encoded_out_file_name}",
        account_key=DOCUMENT_STORAGE_ACCOUNT_KEY,
        permission=BlobSasPermissions(read=True),
        start=datetime.now(timezone.utc) - timedelta(minutes=5),
        expiry=datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    )
    
    # Construct the full URL including the SAS token.
    blob_url = (
        f"https://{DOCUMENT_STORAGE_ACCOUNT}.blob.core.windows.net/"
        f"{STORAGE_ACCOUNT_OUTPUT_CONTAINER}/document_insights/{foldername}/{encoded_out_file_name}?{sas_token}"
    )
    return blob_url


def extract_account_info(connection_string):
    info = {}
    for part in connection_string.split(';'):
        if '=' in part:
            key, value = part.split('=', 1)
            info[key] = value
    return info


# Function to upload file to Azure Storage
def upload_to_azure_storage(files, foldername):
    
    total_files = len(files)
    progress_bar = st.progress(0)

    for i, file in enumerate(files):
        # Update the progress bar
        percent_complete = (i + 1) / total_files
        progress_bar.progress(percent_complete)
        upload_file_to_azure_storage(file, foldername)

def upload_file_to_azure_storage(file, foldername):

    blob_service_client = BlobServiceClient.from_connection_string(f"{DOCUMENT_STORAGE_CONNECTIONSTRING}")
    blob_client = blob_service_client.get_blob_client(container=TEMPLATE_DOCUMENT_CONTAINER, blob=foldername + "/" + file.name)
    
    if not st.session_state.file_processed:
        blob_client.upload_blob(file, overwrite=True)
        apiurl = "https://occ-notebook-test.azurewebsites.net/api/generate_insights"
        params = {"folder_name": foldername} 
        response = requests.get(apiurl, params=params)
        st.markdown(f"**{file.name}** ✅ uploaded successfully")

    # url = generate_document_url(foldername, file.name)
    # st.markdown(f"[Download/View File]({url})")
    # Use an if-statement to check if the button is clicked.
    # if st.button(f"Fetch {file.name}"):
    #     file_data = download_file_from_blob(foldername, file.name)
    #     st.success(f"File '{file.name}' has been fetched from Azure!")

        # Provide a download button for the user to save the file locally
        # label_text = f"Download {file.name}"
        # st.download_button(
        #     label=label_text,
        #     data=file_data,
        #     file_name=file.name,
        #     mime="text/markdown"  # Adjust MIME type if needed

        # Create two columns of equal width
    #fetch_buttton(file, foldername)

def clear_session_data():
    # Clear or update the session state variable
    del st.session_state['file_processed']
    del st.session_state['foldername']
    del st.session_state['uploaded_file']
    del st.session_state['uploaded_files']


def fetch_buttton(file, foldername):

    col1, col2 = st.columns(2)
    # Place the fetch button in the first column
    with col1:
        fetch_clicked = st.button(f"Fetch {file.name}", key=f"fetch_{file.name}")

    # Create an empty placeholder in the second column for the download button
    with col2:
        download_placeholder = st.empty()

    # When the fetch button is clicked, download the file from Azure and render the download button in col2
    if fetch_clicked:
        file_data = download_file_from_blob(foldername, file.name)
        # st.success(f"File '{file.name}' has been fetched from Azure!")
        label_text = f"Download {file.name}"
        download_placeholder.download_button(
            label=label_text,
            data=file_data,
            file_name=file.name,
            key=f"download_{file.name}",
            on_click=clear_session_data,
            mime="text/markdown"  # Adjust MIME type if needed
        )  # Adjust MIME type if needed

def update_status_in_queue():
    message = base64_encode("done")
       
    queue_service_client = QueueServiceClient.from_connection_string(f"{DOCUMENT_STORAGE_CONNECTIONSTRING}")
    queue_client = queue_service_client.get_queue_client(TEMPLATE_DOCUMENT_QUEUE)
    queue_client.send_message( message)


def base64_encode(plain_text):
    plain_text_bytes = plain_text.encode('utf-8')
    return base64.b64encode(plain_text_bytes).decode('utf-8')

# Function to convert a binary file to a base64 string
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def download_file(file):
    with open(file, "rb") as f:
        data = f.read()
    return data

def download_file_from_blob(folder_name, file_name):
    # Get Azure connection details from st.secrets
    connection_string = DOCUMENT_STORAGE_CONNECTIONSTRING 
    container_name = STORAGE_ACCOUNT_OUTPUT_CONTAINER

    # Replace the file extension with ".md"
    base_name, _ = os.path.splitext(file_name)
    out_file_name = base_name + "-final-insights" + ".md"

    encoded_out_file_name = "document_insights/" + folder_name + "/" + urllib.parse.quote(out_file_name)

    # Create a BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=encoded_out_file_name )

    # Download the blob's content
    download_stream = blob_client.download_blob()
    file_data = download_stream.readall()
    return file_data