import streamlit as st
import json
import streamlit.components.v1 as components
import msal
from utils import get_auth_url, get_token_from_code, get_user_name, build_msal_app, get_user_info

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


    user_info = get_user_info()
    if user_info:
        user_name = user_info['user_claims']['val']
        st.write(f"Logged in user: {user_name}")
    else:
        st.write("Failed to fetch user information")
    
    # Check for the authorization code in the query parameters.
    query_params = st.query_params
    if "code" in query_params:
        auth_code = query_params["code"][0]
        result = get_token_from_code(auth_code)
        if "access_token" in result:
            st.session_state.token_response = result
            st.experimental_set_query_params()  # Clear query parameters after processing.
            st.success("Login successful!")
        else:
            st.error("Login failed. Please try again.")
else:
    # User is authenticated; display their name.
    user_name = get_user_name(st.session_state.token_response)
    if user_name:
        st.write(f"Hello, {user_name}!")
    else:
        st.write("Hello!")





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