# Python Syntax Quick Reference

## Variables & Types

```python
x = 5
name = "Alice"
flag = True
nothing = None
big = float('inf')
```

---

## If / Else

```python
if x > 0:
    print("positive")
elif x == 0:
    print("zero")
else:
    print("negative")

# one-liner
result = "yes" if x > 0 else "no"
```

---

## Functions

```python
def greet(name):
    return "Hello " + name

def greet(name: str) -> str:       # with type hints
    return "Hello " + name

def connect(host, port=8080):      # default argument
    pass

def set_at(key, ttl=None):         # optional argument
    if ttl is None:
        expires = float('inf')
    else:
        expires = ttl + 10
```

---

## Classes

```python
class Dog:
    def __init__(self, name):      # constructor
        self.name = name           # instance variable

    def bark(self):
        return self.name + " says woof"

d = Dog("Rex")
print(d.bark())
```

---

## Dictionaries

```python
d = {}
d = {"key": "value"}              # colon, not equals

d["key"] = "value"                # set
d["key"]                          # get — KeyError if missing
d.get("key")                      # get — None if missing
d.get("key", "default")           # get with fallback

del d["key"]                      # delete — KeyError if missing
d.pop("key", None)                # safe delete

"key" in d                        # membership check
"key" not in d

for k in d:                       # iterate keys
for k, v in d.items():            # iterate key-value pairs
for v in d.values():              # iterate values

len(d)

# nested safe access
d.get("key", {}).get("field")

# dict comprehension
{k: v for k, v in d.items() if v > 0}
```

### Storing a Dict with Multiple Fields as a Value (DB pattern)

```python
# SET — store a dict as the value (use this over tuples for 3+ fields)
store = {}
store["task1"] = {"payload": "do work", "priority": 1, "expires_at": time.time() + ttl}

# GET — access individual fields by name (clearer than index)
entry = store.get("task1")
if entry is not None:
    print(entry["payload"])       # "do work"
    print(entry["expires_at"])    # timestamp

# CHECK expiry
entry = store.get("task1")
if entry is not None and entry["expires_at"] > time.time():
    return entry["payload"]

# SEPARATE independent checks — don't combine unrelated conditions
# WRONG — mixes two different concerns in one if:
if task_id not in store and ttl is not None:
    store[task_id] = {...}

# RIGHT — handle each concern separately:
if task_id in store:              # check 1: does it already exist?
    return None

if ttl is None:                   # check 2: handle ttl independently
    expires_at = None
else:
    expires_at = time.time() + ttl

store[task_id] = {"payload": payload, "expires_at": expires_at}
```

---

### Storing Tuples as Values (DB pattern)

```python
# SET — store a tuple as the value
store = {}
store["user1"] = ("Alice", float('inf'))    # (value, expires_at)
store["user2"] = ("Bob", 100)               # expires at t=100

# GET — unpack the tuple
entry = store.get("user1")
if entry is not None:
    value, expires_at = entry               # unpack both at once
    print(value)                            # "Alice"
    print(expires_at)                       # inf

# CHECK expiry then get value
entry = store.get("user1")
if entry is not None and entry[1] > timestamp:   # entry[1] is expires_at
    value = entry[0]                             # entry[0] is value

# CLEANER — unpack first, then check
entry = store.get("user1")
if entry is not None:
    value, expires_at = entry
    if expires_at > timestamp:
        return value

# DELETE
if "user1" in store:
    del store["user1"]

# NESTED dict with tuple values (the real DB structure)
store = {}                                       # store[key][field] = (value, expires_at)
store["user1"] = {}
store["user1"]["name"] = ("Alice", float('inf'))
store["user1"]["age"] = ("30", 100)

# get a nested field safely
fields = store.get("user1", {})
entry = fields.get("name")
if entry is not None:
    value, expires_at = entry
```

---

## Lists

```python
lst = []
lst = [1, 2, 3]

lst.append(x)                     # add to end — NOT .add()
lst.insert(0, x)                  # insert at index

lst.pop()                         # remove + return last
lst.pop(0)                        # remove + return at index
del lst[0]                        # remove at index

lst[0]                            # first item
lst[-1]                           # last item
lst[1:3]                          # slice: index 1 and 2

x in lst
len(lst)

lst.sort()                        # in-place
sorted(lst)                       # new list, original unchanged
sorted(lst, key=lambda x: x[0])  # sort by first element of tuple

# list comprehension
[x * 2 for x in lst]
[x for x in lst if x > 0]
```

---

## For Loops

```python
for i in range(5):                # 0, 1, 2, 3, 4
for i in range(1, 6):             # 1, 2, 3, 4, 5
for item in lst:
for i, item in enumerate(lst):    # index + value
for k, v in d.items():
```

---

## String Methods

```python
s = "Hello World"
s.lower()                         # "hello world"
s.upper()                         # "HELLO WORLD"
s.startswith("He")                # True  — NOT startsWith
s.endswith("ld")                  # True
s.split(" ")                      # ["Hello", "World"]
" ".join(["Hello", "World"])      # "Hello World"
s.strip()                         # remove whitespace from both ends
len(s)

# f-string formatting
f"{field}({value})"               # "name(Alice)"
f"x is {x}"
```

---

## Tuples

```python
t = (1, 2)
a, b = t                          # unpack
a, b = b, a                       # swap

# common: store pairs
entry = ("value", float('inf'))
value, expires_at = entry         # unpack
```

---

## None Checks

```python
if x is None:
if x is not None:
if x:                             # falsy: None, 0, "", [], {}
if not x:
```

---

## Import

```python
import threading
import copy
import bisect
from collections import defaultdict
import time
import asyncio
```

---

## Common Gotchas

| Wrong | Right |
|-------|-------|
| `startsWith` | `startswith` |
| `lst.add(x)` | `lst.append(x)` |
| `self.store(key)` | `self.store[key]` |
| `{"key" = value}` | `{"key": value}` |
| `ttl:None` | `ttl=None` |
| `async` | `async def` |
| `for k in self` | `for k in d` |
