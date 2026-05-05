import csv
import os
from fastapi import FastAPI

app = FastAPI()

CSV_FILE = "readings.csv"
FIELDS = ["esp32_id", "ts", "temp", "hum"]


def ensure_csv_schema():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
        return

    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.DictReader(f)
        existing_fields = reader.fieldnames or []
        rows = list(reader)

    if existing_fields == FIELDS:
        return

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELDS})


ensure_csv_schema()


@app.post("/readings")
def add_reading(reading: dict):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writerow({field: reading.get(field, "") for field in FIELDS})
    return {"ok": True}


@app.get("/readings")
def get_readings():
    with open(CSV_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)
