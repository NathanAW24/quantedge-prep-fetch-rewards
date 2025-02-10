import os
from typing import List, Optional
import pandas as pd

from datetime import datetime
from app.models.transaction import Transaction

# Get the absolute path to the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the CSV file relative to this script
DATA_FILE = os.path.join(SCRIPT_DIR, "../../data/transactions.csv")

def read_transactions_from_csv():
    df = pd.read_csv(DATA_FILE)
    return df

def write_transactions_to_csv(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False)


def create_user(transaction_data: dict) -> Transaction:
    df = read_transactions_from_csv()
    new_id = 1 if df.empty else int(df["id"].max()) + 1
    
    transaction_data["id"] = str(new_id)

    new_row = pd.DataFrame([transaction_data])
    df = pd.concat([df, new_row], ignore_index=True)
    write_transactions_to_csv(df)
    return Transaction(**transaction_data)
