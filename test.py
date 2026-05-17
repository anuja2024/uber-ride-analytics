from analytics.queries import get_engine
import pandas as pd
from sqlalchemy import text
import numpy as np

engine = get_engine()

print("Reading data from CSV and fixing it...")
df = pd.read_csv("data/uber_data.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# Replace string "null" with proper NaN
df = df.replace("null", np.nan)
df = df.replace("NULL", np.nan)

# Convert numeric columns properly
numeric_cols = ['booking_value', 'ride_distance', 'driver_ratings', 
                'customer_rating', 'avg_vtat', 'avg_ctat']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

print(f"Total rows: {len(df)}")
print(f"NaN in booking_value: {df['booking_value'].isna().sum()}")
print(f"Sum of booking_value: {df['booking_value'].sum()}")

# Drop old table and reload clean data
print("\nReloading clean data into database...")
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS uber_rides"))
    conn.commit()

df.to_sql('uber_rides', engine, if_exists='replace', index=False)
print("✅ Done! Clean data loaded.")

# Verify
with engine.connect() as conn:
    result = pd.read_sql(text("""
        SELECT 
            COUNT(1) as total,
            SUM(booking_value) as total_rev,
            AVG(booking_value) as avg_fare
        FROM uber_rides
        WHERE booking_status = 'Completed'
    """), conn)
    print(f"\nVerification:")
    print(result)