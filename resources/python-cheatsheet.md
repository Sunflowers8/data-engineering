# Python Cheatsheet for Data Engineering

## 1. Variables and Data Types

```python
name = "ShopFlow"
count = 24
amount = 120.50
active = True
```

Common types: `str`, `int`, `float`, `bool`, `list`, `dict`.

For financial calculations, prefer `Decimal` over `float`.

## 2. Conditions and Loops

```python
status = "completed"

if status == "completed":
    print("Include in completed sales")
else:
    print("Exclude from completed sales")

for number in range(3):
    print(number)
```

## 3. Lists and Dictionaries

```python
orders = [
    {"order_id": "O1", "amount": 100},
    {"order_id": "O2", "amount": 200},
]

total = sum(order["amount"] for order in orders)
print(total)
```

## 4. Functions

```python
def is_valid_order(order):
    return bool(order.get("order_id"))
```

Functions keep processing logic reusable and testable.

## 5. Read CSV

```python
import csv

with open("orders.csv", newline="", encoding="utf-8") as file:
    orders = list(csv.DictReader(file))
```

## 6. Read JSON

```python
import json

with open("payments.json", encoding="utf-8") as file:
    payments = json.load(file)
```

## 7. Error Handling

```python
try:
    value = int("123")
except ValueError:
    value = None
```

Catch specific exceptions and record useful context.

## 8. Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Pipeline started")
logging.warning("Invalid row detected")
logging.error("Load failed")
```

Use logging for operational events rather than relying
only on `print()` statements.

## 9. Decimal and Timestamps

```python
from decimal import Decimal
from datetime import datetime, timezone

amount = Decimal("120.50")
timestamp = datetime.now(timezone.utc)
```

## 10. Pandas

```python
import pandas as pd

df = pd.read_csv("orders.csv")
print(df.head())
print(df.isna().sum())

completed = df[df["status"] == "completed"]
daily = completed.groupby("order_date")["amount"].sum()
```

## 11. Deduplication

```python
df = df.sort_values(
    ["updated_at", "source_seq"],
    ascending=[False, False]
)

latest = df.drop_duplicates(
    subset=["order_id"],
    keep="first"
)
```

Ensure timestamps are parsed correctly before sorting.

## 12. Testing

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
```

Run with:

```bash
python -m pytest -v
```

## 13. Important Engineering Practices

- Validate schemas before processing.
- Record invalid rows with a reason.
- Use stable business keys.
- Avoid duplicates on reruns.
- Handle late-arriving updates.
- Keep watermark updates transactionally safe.
- Log failures clearly.
- Test actual outputs, not just whether code runs.
