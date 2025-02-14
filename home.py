import streamlit as st
import streamlit.components.v1 as components
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient
import datetime
import random
import requests

from utils import upload_to_azure_storage, upload_file_to_azure_storage, fetch_buttton, update_status_in_queue, get_base64_of_bin_file


st.set_page_config(
    page_title="OCC Doc Assist'",
    page_icon=":anchor:",
)

# Path to your local image file
image_path = "images/bkground.jpg"  # Update this path accordingly

# Convert the image to base64
bin_str = get_base64_of_bin_file(image_path)

# Create the CSS with the base64 image embedded
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("data:image/jpeg;base64,{bin_str}");
    background-color: blue;  /* fallback for old browsers */
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}
</style>
"""

# Inject custom CSS to style the buttons
st.markdown(
    """
    <style>
    /* Change the text color of all Streamlit buttons */
    div.stButton > button {
        background-color: grey !important;
    }
    div.stDownloadButton  > button {
        background-color: grey !important;
    }    </style>
    """,
    unsafe_allow_html=True
)

# Hide the deploy button
st.markdown(
    r"""
    <style>
    .stAppDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)



# Add a CSS style block to make text white
st.markdown(
    """
    <style>
    h1, h2, h3, h4, h5, h6, p, li, a {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Inject the CSS with the background image into your app
st.markdown(page_bg_img, unsafe_allow_html=True)

# Path to your local image file
image_path = "images/occ-sig-blue.png"  # Update this path accordingly
bin_str = get_base64_of_bin_file(image_path)

# Inject the HTML for the image using its base64 encoding
st.markdown(
    f'''
    <div style="text-align: right; margin-top: -50px; margin-right: 5px;">
      <img src="data:image/png;base64,{bin_str}" style="width:410px; height:88px;" />
    </div>
    ''',
    unsafe_allow_html=True
)

st.markdown(
    '<h2 style="color: white;">OCC Doc Assist</h2>',
    unsafe_allow_html=True
)


header =st.context.headers.get("X-MS-CLIENT-PRINCIPAL-NAME")
# Check if name is either empty or only contains whitespace.
if header is None:
    header = "unknown"

st.write("Hello " + header)


# Initialize a flag in session state if it doesn't exist yet.
if "file_processed" not in st.session_state:
    st.session_state.file_processed = False
if "foldername" not in st.session_state:
    st.session_state.foldername = ""
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None


# Use this code if you want to upload single file
uploaded_file = st.file_uploader("Choose a file(s)", type=["pdf", "docx", "txt"], accept_multiple_files=False, key="uploaded_files")
# Check if a file is uploaded and hasn't been processed yet.
if uploaded_file and not st.session_state.file_processed:
    ## Create folder with current date and random number
    date_string = datetime.datetime.now().strftime("%m%d%Y")
    random_number = random.randint(100000, 999999)
    foldername = f"{date_string}_{random_number}"
    upload_file_to_azure_storage(uploaded_file, foldername)
    update_status_in_queue() 
    st.session_state.file_processed = True
    fetch_buttton(uploaded_file, foldername)
    st.session_state.foldername = foldername
    st.session_state.uploaded_file = uploaded_file
elif st.session_state.foldername != "":
    fetch_buttton(st.session_state.uploaded_file, st.session_state.foldername)

# Use this code if you want to upload multiple files
# uploaded_files = st.file_uploader("Choose a file(s)", type=["pdf", "docx", "txt"], accept_multiple_files=True)
# if uploaded_files:
#     upload_to_azure_storage(uploaded_files, foldername)
#     #Upload status to queue
#     update_status_in_queue()      


st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown(
    """
    For using Generative Artificial Intelligence (AI) Service, you are accountable for ensuring the accuracy and integrity of all AI generated products from this service that you integrate or introduce into your OCC tasks and work products, in alignment with applicable agency-wide or organizational unit standards.
"""
)