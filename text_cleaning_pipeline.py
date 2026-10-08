"""
Customer Input Data Cleaning Pipeline
-------------------------------------

This script:
1. Loads an Excel/CSV file containing a "Comment" column
2. Cleans the text:
   - Removes emojis
   - Removes HTML tags
   - Expands contractions
   - Normalizes repeated characters
   - Removes non-alphabetic characters
   - Lowercases text
   - Tokenizes and removes stopwords
3. Outputs a cleaned CSV/Excel file

Author: (Your Name)
"""

import pandas as pd
import re
import emoji
from bs4 import BeautifulSoup
import contractions
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download stopwords/tokenizers if missing
nltk.download("punkt")
nltk.download("stopwords")

# --------------------------------------------
# Cleaning Functions
# --------------------------------------------

def remove_emojis(text):
    """Remove emojis using emoji library and regex."""
    return emoji.replace_emoji(text, replace='')

def remove_html(text):
    """Strip HTML tags using BeautifulSoup."""
    return BeautifulSoup(text, "lxml").get_text()

def expand_contractions(text):
    """Expand common English contractions."""
    return contractions.fix(text)

def normalize_repeated_characters(text):
    """
    Convert repeated characters (goooood -> good).
    Keeps two characters max.
    """
    return re.sub(r"(.)\1{2,}", r"\1\1", text)

def remove_non_alpha(text):
    """Remove non-alphabetic characters, keep spaces."""
    return re.sub(r"[^a-zA-Z\s]", " ", text)

def to_lowercase(text):
    return text.lower()

def remove_stopwords(text):
    """Tokenize and remove stopwords."""
    stop_words = set(stopwords.words("english"))
    tokens = word_tokenize(text)
    filtered = [word for word in tokens if word not in stop_words]
    return " ".join(filtered)

# --------------------------------------------
# Master Cleaning Pipeline
# --------------------------------------------

def clean_text(text):
    try:
        original = text
        text = remove_emojis(text)
        text = remove_html(text)
        text = expand_contractions(text)
        text = normalize_repeated_characters(text)
        text = remove_non_alpha(text)
        text = to_lowercase(text)
        text = remove_stopwords(text)
        success = True
    except:
        text = ""
        success = False

    return text, success, len(original.split()), len(text.split())

# --------------------------------------------
# Main Function
# --------------------------------------------

def process_file(input_path, output_path):
    """
    Reads input Excel/CSV file,
    cleans the Comment column,
    and saves the cleaned output.
    """

    # Load file
    if input_path.endswith(".csv"):
        df = pd.read_csv(input_path)
    else:
        df = pd.read_excel(input_path)

    if "Comment" not in df.columns:
        raise ValueError("Input file must contain a 'Comment' column.")

    # Apply cleaning
    cleaned = df["Comment"].astype(str).apply(lambda x: clean_text(x))

    df["Cleaned_Comment"] = cleaned.apply(lambda x: x[0])
    df["Cleaning_Success"] = cleaned.apply(lambda x: x[1])
    df["WordCount_Before"] = cleaned.apply(lambda x: x[2])
    df["WordCount_After"] = cleaned.apply(lambda x: x[3])

    # Save file
    if output_path.endswith(".csv"):
        df.to_csv(output_path, index=False)
    else:
        df.to_excel(output_path, index=False)

    print("Cleaning completed successfully!")
    print(f"Output saved to: {output_path}")

# --------------------------------------------
# Run Script (Optional CLI)
# --------------------------------------------

if __name__ == "__main__":
    input_file = input("Enter input file path (.csv or .xlsx): ")
    output_file = input("Enter output file path (.csv or .xlsx): ")
    process_file(input_file, output_file)
