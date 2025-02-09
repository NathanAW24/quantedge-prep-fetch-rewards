# Short Notes
- User only see single balance (points) in their accounts
- Trasaction record {payer: string, points: integer, timestamp: date}
  - User earn points --> Just add lmao
  - User spends points --> what points to spend first? (payer is just the points-partner)
    - Oldest points spend first (transaction timestamp, not order received)
    - No payer's points to be negative

# Routes
- Add transaction for specific payer and date
- Spend points, list of {payer: string, points: integer}
- Return all payer points balances