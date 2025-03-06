from datetime import date, datetime, time
from fastapi import FastAPI
from pydantic import BaseModel, condecimal

import math
import sqlite3

app = FastAPI()
DATABASE = 'receipts.db'

# Classes for Item and Receipt for request body validation
class Item(BaseModel):
    shortDescription: str
    price: condecimal(decimal_places=2, gt=0)


class Receipt(BaseModel):
    retailer: str
    purchaseDate: date
    purchaseTime: time
    total: condecimal(decimal_places=2, gt=0)
    items: list[Item]


# POST /receipts/process
@app.post("/receipts/process")
async def process_receipt(receipt: Receipt):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    def calculate_points(receipt):
        points = 0

        points += len(receipt.items) // 2 * 5  # Add 5 points for every 2 items
        for char in receipt.retailer:  # Add 1 point for every alphanumeric character in the retailer name
            if char.isalnum():
                points += 1

        for item in receipt.items:  # Check if the length of the desc for each item is divisible by 3
            if len(item.shortDescription.strip()) % 3 == 0:
                points += math.ceil(float(item.price) * 0.2)

        if float(receipt.total) % 1 == 0:  # Check if total is a round dollar amount
            points += 50
        if float(receipt.total) % 0.25 == 0:  # Check if total is a multiple of 0.25
            points += 25
        if receipt.purchaseDate.day % 2 == 1:  # Check if the day is odd
            points += 6
        if datetime.strptime("14:00", "%H:%M").time() <= receipt.purchaseTime < datetime.strptime("16:00", "%H:%M").time():  # Check if the time is between 2pm and 4pm
            points += 10
        return points

    points = calculate_points(receipt)

    # Ideally would initialize this DB outside of the endpoint
    cursor.execute("CREATE TABLE IF NOT EXISTS receipts (id INTEGER PRIMARY KEY AUTOINCREMENT, points INTEGER)")
    cursor.execute("INSERT INTO receipts (points) VALUES (?)", (points,))
    conn.commit()

    id = cursor.lastrowid

    conn.close()

    return {"id": id}


# GET /receipts/{id}/points
@app.get("/receipts/{id}/points")
async def get_points(id: int):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Ideally would initialize this DB outside of the endpoint
    cursor.execute("CREATE TABLE IF NOT EXISTS receipts (id INTEGER PRIMARY KEY AUTOINCREMENT, points INTEGER)")
    cursor.execute("SELECT points FROM receipts WHERE id = ?", (id,))

    points = cursor.fetchone()

    if not points:
        return {"error": "Receipt not found"}

    conn.close()

    return {"points": points[0]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
