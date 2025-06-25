import pandas as pd
import re
from nltk import download
from nltk.tokenize import word_tokenize
# Download tokenizer if not already done
download('punkt')


def tokenize_amharic_text(text, method='nltk'):
    if pd.isna(text) or not str(text).strip():
        return []

    text = str(text)

    # ✅ Keep: Amharic characters, Western numbers (0–9), Amharic punctuation,
    # and spaces
    text = re.sub(r'[^\u1200-\u137F0-9፡።፣፤፥፦፧፨\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    if method == 'nltk':
        return word_tokenize(text)

    elif method == 'regex':
        # ✅ Tokenize Amharic words, Western numbers, and Amharic punctuation
        return re.findall(r'[\u1200-\u137F]+|\d+|[፡።፣፤፥፦፧፨]', text)

    elif method == 'combined':
        tokens = []
        for token in word_tokenize(text):
            tokens.extend(re.findall(r'[\u1200-\u137F]+|\d+', token))
        return tokens

    else:
        raise ValueError(
            "Invalid method. Choose 'nltk', 'regex', or 'combined'")
# normalization


def normalize_amharic_text(text):
    """
    Normalizes Amharic text by removing non-Amharic characters and
    handling case sensitivity.
    """
    text = text.lower()
    # Replace special punctuation marks with a space
    text = re.sub(r'[፡።፣፤፥፦]', ' ', text)
    # Remove any extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# Define entity lists for rule-based labeling (extend as needed)
product_keywords = {
    'ስማርትፎን', 'ጫማ', 'ቦርሳ', 'ላፕቶፕ', 'ቲሸርት', 'ቀሚስ', 'ሰዓት', 'ካሜራ',
    'ማዳመጫ', 'ብስክሌት', 'ልብስ', 'ማቀዝቀዣ', 'ቡታ', 'ልብስ', 'ጫማ', 'ጥፍር',
    'መጠጥ', 'ልጅ', 'መቀቀል', 'መገጣጠሚያ', 'ተብሌት', 'መጫወቻ', 'ምድጃ',
    'ሶፋ', 'መጽሐፍ', 'ሞባይል', 'ጠረጴዛ', 'ጃኬት', 'ሰንሰለት', 'ባትሪ'
}
location_keywords = {'አዲስ_አበባ', 'ቦሌ', 'ፒያሳ', 'መገናኛ', 'ሜክሲኮ',
                     'አራት_ኪሎ', 'ጎፋ', 'ለገሃር', 'ቦታ', 'ቢሮ', 'አድራሻ'}
price_keywords = {'በ', 'ዋጋ', 'ብር'}


def label_tokens(tokens):
    labels = []
    inside_price = False
    inside_loc = False
    inside_prod = False
    for token in tokens:
        if token in product_keywords and inside_prod:
            labels.append('I-Product')
        elif token in product_keywords:
            labels.append('B-Product')
            inside_prod = True
        elif token in location_keywords and inside_loc:
            labels.append('I-LOC')
        elif token in location_keywords:
            labels.append('B-LOC')
            inside_loc = True
        elif token in price_keywords:
            labels.append("B-PRICE")
            inside_price = True
        elif token.isdigit() and inside_price:
            labels.append("I-PRICE")
        elif token.isdigit():
            labels.append("O")
            inside_price = False
        else:
            labels.append("O")
            inside_price = False

    return labels
