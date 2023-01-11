"""
Purpose: Define the home page.
"""

# Third-party imports
import streamlit as st

# Python imports
import json
import re

# Local imports
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
    st.markdown("# Austrolate")
    st.write("Austrolate is a tool for translating between Austrian German and Standard German.")

    dict_de_deAT, dict_deAT_de = get_dicts()

    # Create a form that contains:
    # - a text area input for Deutsch
    # - a button "Translate to Wienerisch"
    # - if the button is clicked, then a uneditable text area output for Wienerisch using the dictionary
    with st.form("Translate to Austrian German"):
        st.markdown("### Standard German")
        de_text = st.text_area("Write text below:")
        submit_button = st.form_submit_button("Translate to Austrian German")
        if submit_button:
            deAT_text = translate_using_dict(de_text, dict_de_deAT)
            st.markdown("### Austrian German")
            st.code(deAT_text, language="markdown")
    
    # Create a form that contains:
    # - a text area input for Wienerisch
    # - a button "Translate to Deutsch"
    # - if the button is clicked, then a uneditable text area output for Deutsch using the dictionary
    with st.form("Translate to Standard German"):
        st.markdown("### Austrian German")
        deAT_text = st.text_area("Write text below:")
        submit_button = st.form_submit_button("Translate to Standard German")
        if submit_button:
            de_text = translate_using_dict(deAT_text, dict_deAT_de)
            st.markdown("### Standard German")
            st.code(de_text, language="markdown")


def translate_using_dict(text: str, dictionary: dict) -> str:
    """
    Translate text using a dictionary. If a word is not in the dictionary, then it is not translated.
    """
    # Split the text into words, accounting for punctuation
    words = re.split(r"(\W)", text)
    
    translated_words = []
    for word in words:
        if not word:
            continue
        is_first_letter_upper = word[0].isupper()
        if word in dictionary or word.lower() in dictionary:
            translated_word = dictionary[word if word in dictionary else word.lower()]
            if is_first_letter_upper:
                translated_word = translated_word.capitalize()
            translated_words.append(translated_word)
        else:
            translated_words.append(word)
    
    return "".join(translated_words)




@st.experimental_singleton
def get_dicts() -> tuple[dict, dict]:
    path_de_deAT = "data/de_deAT.json"
    path_deAT_de = "data/deAT_de.json"

    with open(path_de_deAT, "r", encoding="utf-8") as file:
        dict_de_deAT = json.load(file)
    
    with open(path_deAT_de, "r", encoding="utf-8") as file:
        dict_deAT_de = json.load(file)

    return dict_de_deAT, dict_deAT_de


def invert_dict(dictionary: dict) -> dict:
    inverted = {}
    for key, value in dictionary.items():
        if not value in inverted:
            # only add it if it is not already in the dictionary
            inverted[value] = key
    return inverted


if __name__ == "__main__":
    generate_page()
