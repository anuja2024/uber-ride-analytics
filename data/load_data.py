import pandas as pd
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    port=os.getenv("DB_PORT", 5432),
    database=os.getenv("DB_NAME", "rideshare"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
)
cur = conn.cursor()

# Drop and recreate table cleanly
cur.execute("DROP TABLE IF EXISTS uber_rides;")
cur.execute("""
CREATE TABLE uber_rides (
    id SERIAL PRIMARY KEY,
    date DATE,
    time TIME,
    booking_id VARCHAR(50),
    booking_status VARCHAR(100),
    customer_id VARCHAR(50),
    vehicle_type VARCHAR(50),
    pickup_location VARCHAR(100),
    drop_location VARCHAR(100),
    avg_vtat FLOAT,
    avg_ctat FLOAT,
    booking_value FLOAT,
    ride_distance FLOAT,
    driver_rating FLOAT,
    customer_rating FLOAT,
    payment_method VARCHAR(50),
    cancelled_by_customer FLOAT,
    cancelled_by_driver FLOAT,
    incomplete_rides FLOAT
);
""")
conn.commit()
print("✅ Table created")

# Load and clean CSV
df = pd.read_csv("data/uber_data.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(f"✅ Loaded {len(df)} rows")

# Insert rows
inserted = 0
errors = 0

for _, row in df.iterrows():
    try:
        cur.execute("""
            INSERT INTO uber_rides (
                date, time, booking_id, booking_status,
                customer_id, vehicle_type, pickup_location, drop_location,
                avg_vtat, avg_ctat, booking_value, ride_distance,
                driver_rating, customer_rating, payment_method,
                cancelled_by_customer, cancelled_by_driver, incomplete_rides
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row.get("date"),
            row.get("time"),
            row.get("booking_id"),
            row.get("booking_status"),
            row.get("customer_id"),
            row.get("vehicle_type"),
            row.get("pickup_location"),
            row.get("drop_location"),
            row.get("avg_vtat"),
            row.get("avg_ctat"),
            row.get("booking_value"),
            row.get("ride_distance"),
            row.get("driver_ratings"),
            row.get("customer_rating"),
            row.get("payment_method"),
            row.get("cancelled_rides_by_customer", 0),
            row.get("cancelled_rides_by_driver", 0),
            row.get("incomplete_rides", 0),
        ))
        inserted += 1

        if inserted % 10000 == 0:
            conn.commit()
            print(f"  → {inserted} rows inserted...")

    except Exception as e:
        errors += 1
        conn.rollback()  # reset transaction after each error
        if errors <= 3:
            print(f"⚠️ Row error: {e}")

conn.commit()
cur.close()
conn.close()

print(f"\n✅ Done! {inserted} rows inserted, {errors} errors")