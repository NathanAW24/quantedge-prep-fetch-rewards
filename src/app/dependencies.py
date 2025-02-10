import pandas as pd
import os
import random
from datetime import datetime

import pytz

def run_migration():
    output_dir = os.path.join(os.path.dirname(__file__), '../data/')
    os.makedirs(output_dir, exist_ok=True)

    users_path = os.path.join(output_dir, 'users.csv')
    if not os.path.exists(users_path):
        df = pd.DataFrame(columns=['id', 'name', 'points'])
        df.to_csv(users_path, index=False)

    payers_path = os.path.join(output_dir, 'payers.csv')
    if not os.path.exists(payers_path):
        df = pd.DataFrame(columns=['id', 'name', 'points'])
        df.to_csv(payers_path, index=False)

    transactions_path = os.path.join(output_dir, 'transactions.csv')
    if not os.path.exists(transactions_path):
        df = pd.DataFrame(columns=['id', 'payer_id', 'user_id', 'points', 'timestamp', 'expired'])
        df.to_csv(transactions_path, index=False)


def synchronize_balances(users_path, payers_path, transactions_path):
    """
    Synchronizes balances by applying transaction points to users and payers.
    """
    users_df = pd.read_csv(users_path)
    payers_df = pd.read_csv(payers_path)
    transactions_df = pd.read_csv(transactions_path)

    # Ensure correct data types
    users_df["id"] = users_df["id"].astype(str)
    payers_df["id"] = payers_df["id"].astype(str)
    transactions_df["user_id"] = transactions_df["user_id"].astype(str)
    transactions_df["payer_id"] = transactions_df["payer_id"].astype(str)

    # Iterate through transactions and update user & payer balances
    for _, transaction in transactions_df.iterrows():
        user_id = transaction["user_id"]
        payer_id = transaction["payer_id"]
        points = transaction["points"]

        # Update user and payer balances based on points
        users_df.loc[users_df["id"] == user_id, "points"] += points
        payers_df.loc[payers_df["id"] == payer_id, "points"] -= points

    # Save the updated data back to CSV
    users_df.to_csv(users_path, index=False)
    payers_df.to_csv(payers_path, index=False)

def run_seed():
    """
    Seeds the users, payers, and transactions, then synchronizes balances.
    """
    output_dir = os.path.join(os.path.dirname(__file__), '../data/')
    
    users_path = os.path.join(output_dir, 'users.csv')
    payers_path = os.path.join(output_dir, 'payers.csv')
    transactions_path = os.path.join(output_dir, 'transactions.csv')

    users_df = pd.read_csv(users_path) if os.path.exists(users_path) else pd.DataFrame(columns=['id', 'name', 'points'])
    payers_df = pd.read_csv(payers_path) if os.path.exists(payers_path) else pd.DataFrame(columns=['id', 'name', 'points'])
    transactions_df = pd.read_csv(transactions_path) if os.path.exists(transactions_path) else pd.DataFrame(columns=['id', 'payer_id', 'user_id', 'points', 'timestamp', 'expired'])

    # Seed users if empty
    if users_df.empty:
        users = [
            {'id': '1', 'name': 'Alice', 'points': 0},
            {'id': '2', 'name': 'Bob', 'points': 0},
            {'id': '3', 'name': 'Charlie', 'points': 0}
        ]
        users_df = pd.DataFrame(users)
        users_df.to_csv(users_path, index=False)

    # Seed payers if empty
    if payers_df.empty:
        payers = [
            {'id': '1', 'name': 'Amazon', 'points': 1000},
            {'id': '2', 'name': 'Google', 'points': 1000},
            {'id': '3', 'name': 'Facebook', 'points': 1000}
        ]
        payers_df = pd.DataFrame(payers)
        payers_df.to_csv(payers_path, index=False)

    # Seed transactions if empty
    if transactions_df.empty:
        transactions = []
        user_ids = users_df['id'].tolist()
        payer_ids = payers_df['id'].tolist()

        random.seed(42)  

        for i in range(1, 10):
            transaction = {
                'id': f'{i}',
                # 'payer_id': random.choice(payer_ids),
                # 'user_id': random.choice(user_ids),
                'payer_id': "1",
                'user_id': "1",
                'points': random.randint(1, 10),  # Allow both positive and negative transactions
                'timestamp': datetime.utcnow().replace(tzinfo=pytz.UTC),
                'expired': False
            }
            transactions.append(transaction)

        transactions_df = pd.DataFrame(transactions)
        transactions_df.to_csv(transactions_path, index=False)

    # After seeding, synchronize balances
    synchronize_balances(users_path, payers_path, transactions_path)



def run_drop():
    """ Deletes all files inside the data/ directory but keeps the directory itself. """
    output_dir = os.path.join(os.path.dirname(__file__), '../data/')
    
    if os.path.exists(output_dir):
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

def run_init():
    run_drop()
    run_migration()
    run_seed()
