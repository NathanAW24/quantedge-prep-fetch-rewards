import pandas as pd
import os
import random
from datetime import datetime

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
        df = pd.DataFrame(columns=['id', 'payer_id', 'user_id', 'points', 'timestamp'])
        df.to_csv(transactions_path, index=False)


def run_seed():
    output_dir = os.path.join(os.path.dirname(__file__), '../data/')
    
    users_path = os.path.join(output_dir, 'users.csv')
    payers_path = os.path.join(output_dir, 'payers.csv')
    transactions_path = os.path.join(output_dir, 'transactions.csv')

    users_df = pd.read_csv(users_path) if os.path.exists(users_path) else pd.DataFrame(columns=['id', 'name', 'points'])
    payers_df = pd.read_csv(payers_path) if os.path.exists(payers_path) else pd.DataFrame(columns=['id', 'name', 'points'])
    transactions_df = pd.read_csv(transactions_path) if os.path.exists(transactions_path) else pd.DataFrame(columns=['id', 'payer_id', 'user_id', 'points', 'timestamp'])

    if users_df.empty:
        users = [
            {'id': '1', 'name': 'Alice', 'points': 100},
            {'id': '2', 'name': 'Bob', 'points': 200},
            {'id': '3', 'name': 'Charlie', 'points': 300}
        ]
        users_df = pd.DataFrame(users)
        users_df.to_csv(users_path, index=False)

    if payers_df.empty:
        payers = [
            {'id': '1', 'name': 'Amazon', 'points': 500},
            {'id': '2', 'name': 'Google', 'points': 600},
            {'id': '3', 'name': 'Facebook', 'points': 700}
        ]
        payers_df = pd.DataFrame(payers)
        payers_df.to_csv(payers_path, index=False)

    if transactions_df.empty:
        transactions = []
        user_ids = users_df['id'].tolist()
        payer_ids = payers_df['id'].tolist()

        for i in range(1, 6):
            transaction = {
                'id': f'{i}',
                'payer_id': random.choice(payer_ids),
                'user_id': random.choice(user_ids),
                'points': random.randint(10, 200),
                'timestamp': datetime.now().isoformat()
            }
            transactions.append(transaction)

        transactions_df = pd.DataFrame(transactions)
        transactions_df.to_csv(transactions_path, index=False)

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
