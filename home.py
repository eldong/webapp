import streamlit as st
import requests

st.set_page_config(
    page_title="Gen AI Portal",
    page_icon="👋",
)

#st.sidebar.title("Navigation")
#st.sidebar.success("Select an action to run.")

# Replace this URL with the actual URL of your Flask API endpoint
api_url = "https://occaiportalpoc.azurewebsites.net/user-name"

try:
    # Make a GET request to the Flask API.
    # IMPORTANT: For the header to be present, the request must pass through Easy Auth.
    response = requests.get(api_url)
    response.raise_for_status()  # Raise an error for non-2xx responses.
    data = response.json()
    
    if "principal_name" in data:
        st.write(f"Hello, {data['principal_name']}!")
    else:
        st.error("User principal name not found in response.")
except Exception as e:
    st.error(f"Error fetching user info: {e}")


st.markdown(
    """
    ### OCC Gen AI Portal
 """
)
st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown(
    """
    For using Generative Artificial Intelligence (AI) Service, you are accountable for ensuring the accuracy and integrity of all AI generated products from this service that you integrate or introduce into your OCC tasks and work products, in alignment with applicable agency-wide or organizational unit standards.
"""
)