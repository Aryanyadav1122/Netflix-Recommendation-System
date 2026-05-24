import re


# ============================================
# Module 5: Missing Value Handling
# ============================================

def handle_missing_values(df):

    df["description"] = df["description"].fillna("")
    df["listed_in"] = df["listed_in"].fillna("")
    df["director"] = df["director"].fillna("Unknown")
    df["cast"] = df["cast"].fillna("Unknown")
    df["country"] = df["country"].fillna("Unknown")

    return df


# ============================================
# Module 6: Advanced Text Normalization
# ============================================

def clean_data(text):

    if isinstance(text, str):

        text = text.lower()

        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    return ""


def preprocess_text(df):

    df["listed_in"] = df["listed_in"].apply(clean_data)

    df["description"] = df["description"].apply(clean_data)

    df["director"] = df["director"].apply(clean_data)

    df["cast"] = df["cast"].apply(clean_data)

    df["country"] = df["country"].apply(clean_data)

    return df