import streamlit as st
import json
import streamlit.components.v1 as components
import msal
from utils import  get_token
from threading import Thread
from streamlit.web.server.websocket_headers import _get_websocket_headers





st.set_page_config(
    page_title="Gen AI Portal",
    page_icon="👋",
)

#st.sidebar.title("Navigation")
#st.sidebar.success("Select an action to run.")

if "token_response" not in st.session_state:
    st.session_state.token_response = None

if st.session_state.token_response is None:
    st.info("You are not logged in. Please sign in:")
    
    # Display a login link using the helper function.
    #auth_url = get_auth_url()
    #st.markdown(f"[Click here to sign in with Azure AD]({auth_url})", unsafe_allow_html=True)
    # Automatically redirect the user using an HTML meta refresh.
    # redirect_html = f"""
    # <html>
    #   <head>
    #     <meta http-equiv="refresh" content="0; url={auth_url}">
    #   </head>
    #   <body>
    #     If you are not redirected automatically, <a href="{auth_url}">click here</a>.
    #   </body>
    # </html>
    # """
    # st.components.v1.html(redirect_html, height=100)    


    # user_info = get_user_info()
    # st.write(user_info)
    # if user_info:
    #     user_name = user_info['user_claims']['val']
    #     st.write(f"Logged in user: {user_name}")
    # else:
    #     st.write("Failed to fetch user information")


headers = _get_websocket_headers()
header_token = headers.get("X-MS-CLIENT-PRINCIPAL-NAME")
st.write("Header Token:")
st.write(header_token)

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