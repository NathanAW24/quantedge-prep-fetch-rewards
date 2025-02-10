import os

import pandas as pd

from app.models.user import User

# Get the absolute path to the script's directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the CSV file relative to this script
DATA_FILE = os.path.join(SCRIPT_DIR, "../../data/users.csv")

def read_users_from_csv():
    df = pd.read_csv(DATA_FILE)
    return df

def write_users_to_csv(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False)

def get_user_by_id(user_id: str):
    print(DATA_FILE)
    df = read_users_from_csv()
    print(df)

    df['id'] = df['id'].astype(str)
    user_row = df[df['id'] == user_id]
    print(user_row)

    if not user_row.empty:
        row = user_row.iloc[0]
        return User(id=row['id'], name=row['name'], points=row['points'])
    return None
