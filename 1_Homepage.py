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
    st.write(
        "Austrolate is a tool for translating between Austrian German and Standard German.")

    dict_de_deAT, dict_deAT_de = get_dicts()

    if dict_de_deAT is None or dict_deAT_de is None:
        st.error("Could not load translation files. Please try again later.")
        return

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

    # Add elements for showing/hiding the dictionaries
    st.markdown("### Dictionaries")
    with st.expander("Click to Show Dictionaries"):
        tab1, tab2 = st.tabs(["Standard to Austrian German", "Austrian to Standard German"])

        with tab1:
            st.write("Number of Items: " + str(len(dict_de_deAT)))
            st.json(dict_de_deAT)
        
        with tab2:
            st.write("Number of Items: " + str(len(dict_deAT_de)))
            st.json(dict_deAT_de)


MAX_PHRASE_LENGTH = 5
DO_NOT_CAPITALIZE_TRANSLATION = ["I"]
MAX_ITERATIONS = 1000 # Backup cutoff for the translator to prevent infinite loops

def translate_using_dict(text: str, dictionary: dict) -> str:
    """
    Translate text using a dictionary. If a word is not in the dictionary, then it is not translated.
    """

    # Split the text into words, accounting for punctuation
    words = re.split(r"(\W)", text)

    # If the last word is "", we need to remove it because it meshes up the algorithm
    if words[-1] == "":
        words = words[:-1]

    # CODE: for translating one word at a time
    # translated_words = []
    # for word in words:
    #     if not word:
    #         continue
    #     is_first_letter_upper = word[0].isupper()
    #     if word in dictionary or word.lower() in dictionary:
    #         translated_word = dictionary[word if word in dictionary else word.lower()]
    #         if is_first_letter_upper:
    #             translated_word = translated_word.capitalize()
    #         translated_words.append(translated_word)
    #     else:
    #         translated_words.append(word)

    # CODE: for translating multiple words (phrases) at a time.
    translated_words = []
    # if a word or a set of words up to MAX_PHRASE_LENGTH is in the dictionary, then translate it
    i = 0
    backup_i = 0
    print("words:", words)
    print("len(words):", len(words))
    while i < len(words) and backup_i < MAX_ITERATIONS:
        backup_i += 1
        print(f"words[{i}]= " + words[i])
        # Check if the word is empty
        if not words[i]:
            continue
        # Check if the first letter of the word is uppercase
        is_first_letter_upper = words[i][0].isupper()
        # Iterate through the words
        was_translated = False
        for j in range(MAX_PHRASE_LENGTH):
            # Check if the word is out of range
            if i + j > len(words) + 1:
                break
            # Join the words
            phrase = "".join(words[i:i + j + 1])
            # print("Checking phrase:", phrase)
            # Check if the phrase is in the dictionary
            if phrase.lower() in dictionary:
                translated_word = dictionary[phrase.lower()]
                # Check if the first letter of the word is uppercase
                if is_first_letter_upper and (phrase not in DO_NOT_CAPITALIZE_TRANSLATION):
                    translated_word = cap_first(translated_word)
                translated_words.append(translated_word)
                print("translated_words:", translated_words)
                was_translated = True
                i += j + 1
                break
        if not was_translated:
            translated_words.append(words[i])
            i += 1

    return "".join(translated_words)


@st.experimental_singleton
def get_dicts() -> tuple[dict, dict]:
    """Load dictionaries from json files.

    Returns:
        tuple[dict, dict]: (de_deAT, deAT_de)
    """

    # Load German to Austrian dictionary
    try:
        with open("data/de_deAT.json", "r", encoding="utf-8") as file:
            dict_de_deAT = json.load(file)
    except FileNotFoundError:
        print("Could not load dictionary de_deAT.json.")
        return None

    # Load Austrian to German dictionary
    try:
        with open("data/deAT_de.json", "r", encoding="utf-8") as file:
            dict_deAT_de = json.load(file)
    except FileNotFoundError:
        print("Could not load dictionary deAT_de.json.")
        return None

    # Make the keys lowercase
    dict_de_deAT = make_keys_lowercase(dict_de_deAT)
    dict_deAT_de = make_keys_lowercase(dict_deAT_de)

    # Return both dictionaries
    return dict_de_deAT, dict_deAT_de

def make_keys_lowercase(dictionary: dict) -> dict:
    """Make the keys of a dictionary lowercase.

    Args:
        dictionary (dict): The dictionary to make the keys lowercase.

    Returns:
        dict: The dictionary with the keys lowercase.
    """
    return {key.lower(): value for key, value in dictionary.items()}

def invert_dict(dictionary: dict) -> dict:
    # Create a new, empty dictionary
    inverted = {}
    # iterate over the key-value pairs in the dictionary
    for key, value in dictionary.items():
        # only add it if it is not already in the dictionary
        if not value in inverted:
            inverted[value] = key
    # return the dictionary
    return inverted

def cap_first(s):
    # Capitalize the first letter in a string, while keeping the rest of the string intact
    return s[:1].upper() + s[1:]


if __name__ == "__main__":
    generate_page()
