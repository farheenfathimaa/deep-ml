# 1. Imports and FastAPI initialization
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import time
from typing import Annotated

app = FastAPI()
print("Hello! Python is running.")
print(app) # <fastapi.applications.FastAPI object ...>

'''
Notes: 

In short: Your code was correct. The problem was where Python packages were being installed versus where Python was looking for them.

Remember this workflow for every new Python project:
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
'''

# ------------------------------------

# 2. Pydantic model – Item
class Item(BaseModel):
    name:str
    qty:int

item1 = Item(name = "laptop", qty = 5)
print(item1)
# name='Laptop' qty=5

#item2 = Item(name = "laptop")
#print(item2)
# ValidationError: qty field required

#item3 = Item(name = "laptop", qty = "hello")
#print(item3)
# ValidationError: Input should be a valid integer

# ------------------------------------------------------

# 3. Dependency injection – get_db()

def get_db():
    return {'1':'pole'}

df = get_db()
print(df)
# {'1': 'pole'}

print(df['1'])
# pole


# ----------------------------------------
# 4. POST endpoint – add()
@app.post("/items", status_code = 201)
def add(item:Item):
    return item

# ------------------------
# 5. GET endpoint – get_asset()
@app.get("/assets/{aid}")
def get_asset(
    aid: str,
    db: Annotated[dict, Depends(get_db)]
):
    if aid not in db:
        raise HTTPException(404, "not found")
    return {'id': aid, 'kind': db[aid]}

# -------------------------------
# 6. Retry mechanism – fetch_with_retry()
# Example 1
def fetch_with_retry(call, tries = 3, wait = 1):
    for i in range(tries):
        try:
            return call()
        except TimeoutError:
            if i == tries -1:
                raise
            time.sleep(wait *2 **i)

def fetch_data():
    print("Fetching data...")
    return {"status": "success"}

result = fetch_with_retry(fetch_data)

print(result)
'''
Fetching data...
{'status': 'success'}
'''

# example 2
attempts = 0
def unstable_api():
    global attempts
    attempts +=1

    print(f"attempt {attempts}")

    if attempts < 3:
        raise TimeoutError('Request timed out')

    return {'data': "Fetched successfully"}

result = fetch_with_retry(unstable_api)
print(result)

'''
Attempt 1
Attempt 2
Attempt 3
{'data': 'Fetched successfully'}
'''

# example 3
# def failing_api():
#     print ("Trying...")
#     raise TimeoutError("Server not responding")

# fetch_with_retry(failing_api)

"""
Trying...
Trying...
Trying...

TimeoutError: Server not responding
"""