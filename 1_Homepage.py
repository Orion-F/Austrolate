"""
Module Name: 1_Homepage.py

Purpose: Define the home page.
"""

# Third-party imports
import streamlit as st

from util import st_util
from util import file_util

# Needs to be called before any other Streamlit commands
st.set_page_config(page_title="Austrolate",
                   page_icon="img/favicon.png")
# Note: add layout="wide" if needed to make the page full width

def generate_page() -> None:
    """
    Call the streamlit functions to generate this page.
    """

    st_util.hide_streamlit_labels()

    # Read README.md and render it as markdown
    st.markdown(file_util.get_file_as_string("README.md"))

if __name__ == "__main__":
    generate_page()