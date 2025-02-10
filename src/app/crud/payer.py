import os

import pandas as pd

from app.models.payer import Payer

# Get the absolute path to the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the CSV file relative to this script
DATA_FILE = os.path.join(SCRIPT_DIR, "../../data/payers.csv")

def read_payers_from_csv():
    df = pd.read_csv(DATA_FILE)
    return df

def write_payers_to_csv(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False)

def get_payer_by_id(payer_id: str):
    print(DATA_FILE)
    df = read_payers_from_csv()
    print(df)

    df['id'] = df['id'].astype(str)
    payer_row = df[df['id'] == payer_id]
    print(payer_row)

    if not payer_row.empty:
        row = payer_row.iloc[0]
        return Payer(id=row['id'], name=row['name'], points=row['points'])
    return None
