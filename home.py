import streamlit as st
import streamlit.components.v1 as components
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient
import datetime
import random
import requests

from utils import upload_to_azure_storage, update_status_in_queue


st.set_page_config(
    page_title="Gen AI Portal",
    page_icon="👋",
)


st.markdown(
    """
    ### OCC Gen AI Portal
 """
)

header =st.context.headers.get("X-MS-CLIENT-PRINCIPAL-NAME")
# Check if name is either empty or only contains whitespace.
if header is None:
    header = "unknown"

st.write("Hello " + header)

## Create folder with current date and random number
date_string = datetime.datetime.now().strftime("%m%d%Y")
random_number = random.randint(100000, 999999)
foldername = f"{date_string}_{random_number}"


uploaded_files = st.file_uploader("Choose a file(s)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_files:
    upload_to_azure_storage(uploaded_files, foldername)
    
    #Upload status to queue
    update_status_in_queue()      
    
    st.success("File uploaded to Azure Storage - Now processing!")    # Add your file processing code here
    url = "https://occ-notebook-test.azurewebsites.net/api/generate_insights"
    params = {"folder_name": foldername}  # This sets the 'folder' parameter to 'name'

    response = requests.get(url, params=params)

    # Check the status code and response data
    if response.ok:
        data = response.json()  # or response.text depending on the API response format
        print("Response data:", data)
    else:
        print("Request failed with status:", response.status_code)    

st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown(
    """
    For using Generative Artificial Intelligence (AI) Service, you are accountable for ensuring the accuracy and integrity of all AI generated products from this service that you integrate or introduce into your OCC tasks and work products, in alignment with applicable agency-wide or organizational unit standards.
"""
)