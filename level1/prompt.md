# Level 1 — Basic In-Memory Database

Implement an `InMemoryDB` class in `practice/level1/db.py`.

## Methods

```python
class InMemoryDB:
    def __init__(self):
        # initialize storage

    def set(self, key: str, value) -> None:
        # store key/value pair

    def get(self, key: str):
        # return value, or None if key doesn't exist

    def delete(self, key: str):
        # delete key, return True if existed, None if not

    def keys(self) -> list:
        # return list of all keys

    def scan(self, prefix: str) -> list:
        # return list of keys starting with prefix
```

## Notes

- `get` on missing key → `None`
- `delete` on missing key → `None`  
- `scan("")` → all keys (empty prefix matches everything)
- No ordering required on returned lists

## Run Tests

```bash
python -m unittest practice/level1/test_db.py -v
```

## Time Target

< 10 minutes
