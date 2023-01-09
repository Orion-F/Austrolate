"""
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

    de_deAT_dict = get_de_deAT_dict()
    deAT_de_dict = invert_dict(de_deAT_dict)
    print(deAT_de_dict)

    # Create a form that contains:
    # - a text area input for Deutsch
    # - a button "Translate to Wienerisch"
    # - if the button is clicked, then a uneditable text area output for Wienerisch using the dictionary
    with st.form("Translate to Wienerisch"):
        st.markdown("### Standard German")
        de_text = st.text_area("Write text below:")
        submit_button = st.form_submit_button("Translate to Vienna German")
        if submit_button:
            deAT_text = translate_using_dict(de_text, de_deAT_dict)
            st.markdown("### Vienna German")
            st.code(deAT_text, language="markdown")
    
    # Create a form that contains:
    # - a text area input for Wienerisch
    # - a button "Translate to Deutsch"
    # - if the button is clicked, then a uneditable text area output for Deutsch using the dictionary
    with st.form("Translate to Deutsch"):
        st.markdown("### Vienna German")
        deAT_text = st.text_area("Write text below:")
        submit_button = st.form_submit_button("Translate to Standard German")
        if submit_button:
            de_text = translate_using_dict(deAT_text, deAT_de_dict)
            st.markdown("### Standard German")
            st.code(de_text, language="markdown")


def translate_using_dict(text: str, dictionary: dict) -> str:
    """
    Translate text using a dictionary.
    """
    # Split the text into words
    words = text.split(" ")

    # Translate each word
    translated_words = []
    for word in words:
        if word in dictionary:
            translated_words.append(dictionary[word])
        else:
            translated_words.append(word)

    # Join the translated words into a sentence
    return " ".join(translated_words)


@st.experimental_singleton
def get_de_deAT_dict() -> dict:
    file_path = "de_deAT.csv"

    # Read the file
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Remove first element of lines, since it

    # Create a dictionary
    de_deAT_dict = {}
    for line in lines:
        de, deAT = line.split(",")
        # remove "\n" from deAT
        deAT = deAT[:-1]

        de_options = de.split(";")
        for option in de_options:
            de_deAT_dict[option] = deAT

    return de_deAT_dict


def invert_dict(dictionary: dict) -> dict:
    return {v: k for k, v in dictionary.items()}


if __name__ == "__main__":
    generate_page()
