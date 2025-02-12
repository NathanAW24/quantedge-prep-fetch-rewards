Below is one example of how you might implement the exercise using Python’s FastAPI. In this solution, we create three endpoints:

1. **POST `/transactions`** – to add a new transaction.
2. **POST `/spend`** – to spend points following the “oldest points first” rule while ensuring no payer’s balance goes negative.
3. **GET `/balances`** – to return the current points balance per payer.

We use in‐memory data structures to store the transactions and the payer balances. For each positive transaction, we store an extra field (`remaining`) that tracks how many points from that transaction are still “available” to spend. When a negative transaction is added, we “adjust” the earlier positive transactions for that payer in timestamp order.

Below is the complete code with inline comments and an explanation. You can save this as (for example) `main.py` and follow the instructions afterward to run the service.

---

```python
# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

app = FastAPI(
    title="Fetch Rewards Points Service",
    description="A simple service to add transactions, spend points, and view payer balances.",
    version="1.0.0",
)

# In-memory data stores:
# - `transactions` holds each positive transaction along with its unspent points.
# - `balances` tracks the current total points for each payer.
transactions = []  # List of dicts: { "payer": str, "points": int, "timestamp": datetime, "remaining": int }
balances: Dict[str, int] = {}  # Maps payer name to their total points balance.

# Pydantic models for request bodies

class Transaction(BaseModel):
    payer: str
    points: int
    timestamp: datetime

class SpendRequest(BaseModel):
    points: int

# Endpoint: Add a new transaction
@app.post("/transactions", status_code=201)
def add_transaction(txn: Transaction):
    """
    Adds a transaction.
    
    - For positive points: simply adds a new transaction record with 'remaining' points.
    - For negative points: adjusts existing transactions for that payer (oldest first) so that the payer's balance does not go negative.
    
    Raises an error if the negative transaction would cause the payer's total points to become negative.
    """
    global transactions, balances

    # Initialize payer balance if not present.
    current_balance = balances.get(txn.payer, 0)
    new_balance = current_balance + txn.points

    if new_balance < 0:
        # Not enough points available for this payer to deduct.
        raise HTTPException(
            status_code=400,
            detail=f"Transaction would cause payer '{txn.payer}' balance to go negative."
        )
    
    # For a negative transaction, we need to deduct points from the earliest transactions for that payer.
    if txn.points < 0:
        remaining_to_deduct = -txn.points  # convert to a positive number for processing
        # Process only positive transactions with remaining points in order (oldest first)
        for t in sorted(transactions, key=lambda x: x["timestamp"]):
            if t["payer"] == txn.payer and t["remaining"] > 0:
                if t["remaining"] >= remaining_to_deduct:
                    t["remaining"] -= remaining_to_deduct
                    remaining_to_deduct = 0
                    break
                else:
                    remaining_to_deduct -= t["remaining"]
                    t["remaining"] = 0
        # At this point, remaining_to_deduct should be zero because we already checked the payer had enough total points.
    elif txn.points > 0:
        # For a positive transaction, add it to our available pool.
        transactions.append({
            "payer": txn.payer,
            "points": txn.points,
            "timestamp": txn.timestamp,
            "remaining": txn.points,
        })
    # (If txn.points == 0, nothing changes.)

    # Update the payer's balance
    balances[txn.payer] = new_balance
    return {"message": "Transaction added successfully."}


# Endpoint: Spend points
@app.post("/spend", response_model=List[Dict[str, int]])
def spend_points(spend_request: SpendRequest):
    """
    Spends points using the following rules:
    
    - The oldest points are spent first (based on transaction timestamp).
    - No payer's points balance goes negative.
    
    Returns a list of adjustments (deductions) by payer.
    """
    global transactions, balances

    points_to_spend = spend_request.points

    # Check that there are enough available points overall.
    total_available = sum(t["remaining"] for t in transactions)
    if points_to_spend > total_available:
        raise HTTPException(
            status_code=400,
            detail="Not enough points available to spend the requested amount."
        )

    # Dictionary to record points deducted per payer.
    deductions: Dict[str, int] = {}

    # Process transactions in order of timestamp.
    # We use a sorted copy of the transactions list.
    for t in sorted(transactions, key=lambda x: x["timestamp"]):
        if points_to_spend == 0:
            break  # Done spending all requested points.
        if t["remaining"] <= 0:
            continue  # Skip transactions that have no points left.
        
        available = t["remaining"]
        # Determine the deduction from this transaction.
        deduction = min(available, points_to_spend)
        
        # Deduct points from this transaction.
        t["remaining"] -= deduction
        points_to_spend -= deduction
        
        # Record the deduction for the payer (as a negative number).
        if t["payer"] in deductions:
            deductions[t["payer"]] -= deduction
        else:
            deductions[t["payer"]] = -deduction

    # Update overall payer balances.
    for payer, deduction in deductions.items():
        balances[payer] += deduction  # deduction is negative
    
    # Format the result as a list of dictionaries.
    result = [{"payer": payer, "points": points} for payer, points in deductions.items()]
    return result


# Endpoint: Get payer balances
@app.get("/balances")
def get_balances():
    """
    Returns the current points balance per payer.
    """
    return balances

```

---

## Explanation

1. **Data Storage**

   - We use two global variables:
     - `transactions`: A list that stores all positive transactions. Each transaction is represented by a dictionary that includes the payer, the number of points, the timestamp, and a `remaining` field that tracks how many points in that transaction have not yet been spent.
     - `balances`: A dictionary mapping each payer to their current total points. This is updated whenever transactions are added or points are spent.

2. **Adding a Transaction (`POST /transactions`)**

   - **Positive transactions:**  
     When a transaction with positive points is added, we simply append it to the `transactions` list with its full amount in the `remaining` field and update the payer’s balance.

   - **Negative transactions:**  
     When a transaction with negative points is added, we first ensure that subtracting those points does not cause the payer’s total balance to become negative. Then we iterate over the existing transactions (sorted by timestamp) for that payer to reduce their `remaining` points by the absolute value of the negative amount. This “deducts” points from the oldest available transactions.

3. **Spending Points (`POST /spend`)**

   - The spend endpoint accepts a JSON payload indicating how many points to spend.
   - It first checks that there are enough unspent points overall.
   - Then, it processes the available transactions in order of increasing timestamp (i.e. the oldest transactions first). For each transaction, it deducts as many points as possible without exceeding the transaction’s available points, and records a deduction per payer.
   - Finally, it updates each payer’s balance accordingly and returns a summary list (for example, `[{"payer": "DANNON", "points": -100}, ...]`).

4. **Getting Balances (`GET /balances`)**

   - This endpoint simply returns the current state of the `balances` dictionary so that you can see how many points each payer currently has.

## Practical Application

1. **Running the Service**

   - Make sure you have FastAPI and Uvicorn installed. You can install them using pip:
     ```bash
     pip install fastapi uvicorn
     ```

   - Save the code above into a file named `main.py`.

   - Run the server with Uvicorn:
     ```bash
     uvicorn main:app --reload
     ```
     The `--reload` flag allows the server to automatically restart if you make changes to your code.

2. **Interacting with the API**

   - **Add Transactions:**  
     Send POST requests to `http://127.0.0.1:8000/transactions` with JSON payloads. For example:
     ```json
     { "payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z" }
     ```
     Repeat for each transaction.

   - **Spend Points:**  
     Send a POST request to `http://127.0.0.1:8000/spend` with a payload like:
     ```json
     { "points": 5000 }
     ```
     The response will be a list of deductions by payer, e.g.,
     ```json
     [
       { "payer": "DANNON", "points": -100 },
       { "payer": "UNILEVER", "points": -200 },
       { "payer": "MILLER COORS", "points": -4700 }
     ]
     ```

   - **View Balances:**  
     Send a GET request to `http://127.0.0.1:8000/balances` to see the current balances:
     ```json
     {
       "DANNON": 1000,
       "UNILEVER": 0,
       "MILLER COORS": 5300
     }
     ```

3. **Documentation**

   - FastAPI automatically generates interactive API documentation at `http://127.0.0.1:8000/docs`. This is very useful for testing your endpoints and understanding the request/response formats.

---

This implementation provides a clear, maintainable solution following the requirements. You can further enhance it by adding tests or persisting data to a database if needed. Feel free to adjust the error handling and logging to match production standards if you wish.