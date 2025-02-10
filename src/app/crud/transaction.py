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

def create_transaction(transaction_data: dict) -> Optional[Transaction]:
    df = read_transactions_from_csv()
    new_id = 1 if df.empty else int(df["id"].max()) + 1
    transaction_data["id"] = str(new_id)

    try:
        transaction = Transaction(**transaction_data, expired=False)
    except Exception as e:
        print(f"Failed to create transaction: {e}")
        return None

    new_row = pd.DataFrame([{**transaction_data, "expired" : False}])
    df = pd.concat([df, new_row], ignore_index=True)

    write_transactions_to_csv(df)
    return transaction

def get_all_transactions_with_user_id(user_id: str):
    # also sort by timestamp ascendaing
    # TODO: only take non-expired one and positive points too
    df = read_transactions_from_csv()
    # Ensure 'user_id' and 'id' are strings
    df["user_id"] = df["user_id"].astype(str)
    df["payer_id"] = df["payer_id"].astype(str)
    df["id"] = df["id"].astype(str)

    # Ensure 'expired' column is treated as boolean
    df["expired"] = df["expired"].astype(bool)

    filtered_df = df[(df["user_id"] == user_id) & (df["expired"] == False) & (df["points"] > 0)]
    filtered_df = filtered_df.sort_values(by="timestamp", ascending=True)
    
    return [
        Transaction(
            id=row["id"],
            user_id=row["user_id"],
            payer_id=row["payer_id"],
            points=row["points"],
            timestamp=row["timestamp"],
            expired=row["expired"]
        )
        for _, row in filtered_df.iterrows()
    ]

def update_transaction_expiry(transaction_id: str):
    df = read_transactions_from_csv()

    # Ensure 'id' column is treated as string
    df["id"] = df["id"].astype(str)

    # Check if transaction_id exists in the DataFrame
    if transaction_id not in df["id"].values:
        print(f"Transaction ID {transaction_id} not found.")
        return False

    # Update the 'expired' field to True for the matching transaction
    df.loc[df["id"] == transaction_id, "expired"] = True

    # Save the updated DataFrame back to CSV
    write_transactions_to_csv(df)
    
    return True

def update_transaction_points(transaction_id: str, points: int):
    df = read_transactions_from_csv()

    # Ensure 'id' column is treated as string
    df["id"] = df["id"].astype(str)

    # Check if transaction_id exists in the DataFrame
    if transaction_id not in df["id"].values:
        print(f"Transaction ID {transaction_id} not found.")
        return False

    # Update the 'points' field to True for the matching transaction
    df.loc[df["id"] == transaction_id, "points"] = points

    # Save the updated DataFrame back to CSV
    write_transactions_to_csv(df)
    
    return True
