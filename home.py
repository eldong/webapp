import streamlit as st
import json
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Gen AI Portal",
    page_icon="👋",
)

#st.sidebar.title("Navigation")
#st.sidebar.success("Select an action to run.")


# A simple HTML/JS snippet to call the API endpoint and display the result.

# html_code = """
# <html>
#   <body>
#     <script>
#       fetch('/user-name')  // relative path so that the browser sends the cookies
#         .then(response => response.json())
#         .then(data => {
#           // Display the principal name in the div
#           document.getElementById('output').innerText = "Hello, " + data.principal_name + "!";
#         })
#         .catch(error => {
#           document.getElementById('output').innerText = "Error fetching user info.";
#           console.error("Error:", error);
#         });
#     </script>
#     <div id="output">Loading user info...</div>
#   </body>
# </html>
# """

# components.html(html_code, height=150)



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