import pandas as pd
import os

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
        df = pd.DataFrame(columns=['id', 'payer_id', 'user_id', 'timestamp'])
        df.to_csv(transactions_path, index=False)
