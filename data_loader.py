import pandas as pd

def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file)

    # Normalisasi nama kolom (biar fleksibel)
    df.columns = [c.strip().upper().replace(" ", "_") for c in df.columns]

    return df
