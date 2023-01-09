"""
Module Name: st_util.py

Purpose: Define functions that help with using Streamlit.
"""

# Third-party imports
import streamlit as st

# Python imports
import base64

def hide_streamlit_labels():
    """
    Purpose: Hide unnecessary Streamlit labels.
    """
    # If needed, can add
    # - "#MainMenu {visibility: hidden;}" to hide the hamburger menu in the top left
    # - "header {visibility: hidden;}" to hide the header
    hide_st_style = """
                    <style>
                    footer {visibility: hidden;}
                    </style>
                    """

    st.markdown(hide_st_style, unsafe_allow_html=True)



def generate_table_download_link(df) -> None:
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    # remove line breaks and quotes from the dataframe
    df = df.replace(r'\n', ' ', regex=True)
    df = df.replace(r'\"', '', regex=True)

    # https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806/2
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="table.csv">Download Table as CSV</a>'
    st.markdown(href, unsafe_allow_html=True)