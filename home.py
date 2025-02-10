import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Gen AI Portal",
    page_icon="👋",
)

#st.sidebar.title("Navigation")
#st.sidebar.success("Select an action to run.")
    
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


st.markdown(
    """
    ### OCC Gen AI Portal
 """
)

header =st.context.headers["X-MS-CLIENT-PRINCIPAL-NAME"]
# Check if name is either empty or only contains whitespace.
if not header or not header.strip():
    header = "unknown"
foldername = header.lower().replace(" ", "_")
st.write("Hello " + header)

st.markdown("<br><br><br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown(
    """
    For using Generative Artificial Intelligence (AI) Service, you are accountable for ensuring the accuracy and integrity of all AI generated products from this service that you integrate or introduce into your OCC tasks and work products, in alignment with applicable agency-wide or organizational unit standards.
"""
)