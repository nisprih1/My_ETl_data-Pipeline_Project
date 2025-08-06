import pandas as pd

def clean_and_transform(df):
    # Sample Cleaning Rules (modify as needed)
    if 'email' in df.columns:
        df['email'] = df['email'].str.lower().str.strip()

    if 'dob' in df.columns:
        df['dob'] = pd.to_datetime(df['dob'], errors='coerce')

    if 'is_active' in df.columns:
        df['is_active'] = df['is_active'].astype(bool)

    # Drop rows with missing critical values
    df.dropna(subset=['id', 'email'], inplace=True)

    return df
