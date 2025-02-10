# QuantEdge Prep Fetch Rewards

Based on the requirements inside [here](problem-desc.pdf)

# Project Structure
Important part is the `/app/*` and `/data/*` directory inside `/src/*`.
```
...
- src
  - .pytest_cache
    - .gitignore
    - CACHEDIR.TAG
    - README.md
    - v
      - cache
        - nodeids
        - stepwise
  - app
    - __init__.py
    - __pycache__
      - __init__.cpython-311.pyc
      - dependencies.cpython-311.pyc
      - main.cpython-311.pyc
    - crud
      - __init__.py
      - __pycache__
        - __init__.cpython-311.pyc
        - payer.cpython-311.pyc
        - transaction.cpython-311.pyc
        - user.cpython-311.pyc
      - payer.py
      - transaction.py
      - user.py
    - dependencies.py
    - main.py
    - models
      - __init__.py
      - __pycache__
        - __init__.cpython-311.pyc
        - payer.cpython-311.pyc
        - transaction.cpython-311.pyc
        - user.cpython-311.pyc
      - payer.py
      - transaction.py
      - user.py
    - routers
      - __init__.py
      - __pycache__
        - __init__.cpython-311.pyc
        - payer.cpython-311.pyc
        - transaction.cpython-311.pyc
        - transaction_router.cpython-311.pyc
        - user.cpython-311.pyc
      - payer.py
      - transaction.py
      - user.py
    - schemas
      - __init__.py
      - __pycache__
        - __init__.cpython-311.pyc
        - points_balance.cpython-311.pyc
        - spend_points.cpython-311.pyc
        - transaction.cpython-311.pyc
      - points_balance.py
      - spend_points.py
      - transaction.py
    - services
      - __init__.py
      - __pycache__
        - __init__.cpython-311.pyc
        - add_transaction.cpython-311.pyc
        - points_balance.cpython-311.pyc
        - spend_points.cpython-311.pyc
      - add_transaction.py
      - points_balance.py
      - spend_points.py
    - utils
      - __init__.py
  - data
    - payers.csv
    - transactions.csv
    - users.csv
...
```

