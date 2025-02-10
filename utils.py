# utils.py
import msal
import os
import requests
import streamlit as st
import webbrowser
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.web.server.server import Server

# --- Configuration Constants ---
CLIENT_ID = os.getenv("CLIENT_ID")           # Replace with your Azure AD Application (client) ID
CLIENT_SECRET = os.getenv("CLIENT_SECRET")    # Replace with your client secret
TENANT_ID = os.getenv("TENANT_ID")          # Replace with your Directory (tenant) ID
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = os.getenv("REDIRECT_URI")   # Update for production as needed
SCOPE = ["User.Read"]                   # Adjust scopes as needed

def build_msal_app(cache=None):
    """Creates and returns an MSAL ConfidentialClientApplication object."""
    return msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
        token_cache=cache
    )


# Function to get the token
def get_token():
    app = build_msal_app()
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(scopes=['User.Read'], account=accounts)    
    auth_url = app.get_authorization_request_url(scopes=['User.Read'], redirect_uri=REDIRECT_URI)
    st.write(f'Please go to this URL to authenticate: {auth_url}')
    code = st.text_input('Enter the authorization code:')
    if code:
        result = app.acquire_token_by_authorization_code(code, scopes=['User.Read'], redirect_uri=REDIRECT_URI)
        return result

def get_auth_url():
    """Generates the Azure AD authorization URL."""
    msal_app = build_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )
    return auth_url

def get_token_from_code(auth_code):
    """Exchanges the authorization code for an access token."""
    msal_app = build_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        auth_code,
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )
    return result

def get_user_name(token_response):
    """Extracts the user’s name from the token’s id_token claims."""
    id_token_claims = token_response.get("id_token_claims")
    if id_token_claims:
        # Use 'preferred_username' or 'name' based on your preference and availability.
        return id_token_claims.get("preferred_username") or id_token_claims.get("name")
    return None

def get_user_info2():
    # Create an MSAL public client application instance
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

    # Get the authorization URL to redirect the user to sign in
    auth_url = app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    print("Go to the following URL to sign in:")
    print(auth_url)

    # Optionally, open the URL in a web browser
    webbrowser.open(auth_url)

    # After the user signs in, they will be redirected to your redirect URI
    # with a code in the URL. Capture that code.
    auth_code = input("Paste the authorization code here: ")

    # Exchange the authorization code for tokens
    result = app.acquire_token_by_authorization_code(
        auth_code,
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )

    if "id_token_claims" in result:
        id_token_claims = result["id_token_claims"]
        user_name = id_token_claims.get("name")
        print("Logged in as:", user_name)
    else:
        print("Authentication error:", result.get("error"), result.get("error_description"))

def get_user_info():

    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(scopes=["openid", "profile"])
    st.write(result)
    if "access_token" in result:
        token = result['access_token']
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get("https://occaiportalpoc.azurewebsites.net/.auth/me", headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            user_name = user_info['user_claims']['val']
            print(f"Logged in user: {user_name}")
        else:
            print("Failed to fetch user information")
    else:
        print("Failed to acquire token")


    response = requests.get("https://occaiportalpoc.azurewebsites.net/.auth/me")
    if response.status_code == 200:
        user_info = response.json()
        return user_info
    else:
        return response
    

def read_aad_username():
    session_id = get_script_run_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)
    headers = session_info.ws.request.headers

    headers = headers._dict

    if "X-Ms-Client-Principal-Name" in headers:
        username = headers["X-Ms-Client-Principal-Name"]
        st.write(f"Logged in as {username}")
    else:
        st.warning(f"could not directly read username from azure active directory.")
        username = None
    return username