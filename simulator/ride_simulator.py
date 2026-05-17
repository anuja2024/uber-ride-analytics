import psycopg2
import random
import time
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# ── Database connection ───────────────────────────────────────────────
def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", 5432),
        database=os.getenv("DB_NAME", "rideshare"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )

# ── Realistic data pools ──────────────────────────────────────────────
VEHICLE_TYPES = ["Auto", "Go Mini", "Go Sedan", "Bike",
                 "Premier Sedan", "eBike", "Uber XL"]

BOOKING_STATUSES = [
    "Completed", "Completed", "Completed", "Completed",
    "Completed", "Completed", "Completed",
    "Cancelled by Customer", "Cancelled by Driver",
    "No Driver Found", "Incomplete"
]

PAYMENT_METHODS = ["UPI", "UPI", "UPI", "Cash", "Cash",
                   "Credit Card", "Uber Wallet", "Debit Card"]

PICKUP_LOCATIONS = [
    "Connaught Place", "Rohini West", "Dwarka", "Saket",
    "Lajpat Nagar", "Karol Bagh", "Janakpuri", "Vasant Kunj",
    "Greater Kailash", "Punjabi Bagh", "Rajouri Garden",
    "IIT Delhi", "Hauz Khas", "Nehru Place", "South Extension",
    "Ashok Vihar", "Pitampura", "Shalimar Bagh", "Mayur Vihar",
    "Preet Vihar", "Laxmi Nagar", "Noida Sector 18",
    "Gurgaon Cyber City", "Faridabad", "Ghaziabad"
]

DROP_LOCATIONS = [
    "IGI Airport", "New Delhi Railway Station", "Hazrat Nizamuddin",
    "Indira Gandhi Stadium", "Pragati Maidan", "India Gate",
    "Lotus Temple", "Qutub Minar", "Red Fort", "Humayun Tomb",
    "Ambience Mall", "Select Citywalk", "DLF Mall", "Vegas Mall",
    "AIIMS", "Safdarjung Hospital", "GTB Hospital",
    "Delhi University", "Jamia Millia", "JNU Campus",
    "Cyber Hub Gurgaon", "Sector 62 Noida", "Botanical Garden"
]

CANCELLATION_REASONS_CUSTOMER = [
    "Wrong Address", "Change of plans",
    "Driver is not moving towards pickup",
    "Driver asked to cancel", "AC is not working"
]

CANCELLATION_REASONS_DRIVER = [
    "Customer related issue",
    "The customer was coughing/sick",
    "Personal & Car related issues",
    "More than permitted people"
]

# ── Generate one ride ──────────────────────────────────────────────────
def generate_ride():
    vehicle    = random.choice(VEHICLE_TYPES)
    status     = random.choice(BOOKING_STATUSES)
    pickup     = random.choice(PICKUP_LOCATIONS)
    drop       = random.choice(DROP_LOCATIONS)
    distance   = round(random.uniform(2.0, 45.0), 2)
    avg_vtat   = round(random.uniform(2.0, 15.0), 1)
    avg_ctat   = round(random.uniform(5.0, 60.0), 1)
    payment    = random.choice(PAYMENT_METHODS)

    # Fare based on distance
    base_fare  = 25
    per_km     = random.uniform(10, 20)
    fare       = round(base_fare + (distance * per_km), 2) if status == "Completed" else None

    driver_rating   = round(random.uniform(3.5, 5.0), 1) if status == "Completed" else None
    customer_rating = round(random.uniform(3.5, 5.0), 1) if status == "Completed" else None

    cancelled_by_customer = 1 if status == "Cancelled by Customer" else 0
    cancelled_by_driver   = 1 if status == "Cancelled by Driver" else 0
    incomplete            = 1 if status == "Incomplete" else 0

    reason_customer = random.choice(CANCELLATION_REASONS_CUSTOMER) \
        if cancelled_by_customer else None
    reason_driver   = random.choice(CANCELLATION_REASONS_DRIVER) \
        if cancelled_by_driver else None

    booking_id  = f"CNR{random.randint(100000, 999999)}"
    customer_id = f"CID{random.randint(1000, 9999)}"
    now         = datetime.now()

    return {
        "date":                   now.date(),
        "time":                   now.time(),
        "booking_id":             booking_id,
        "booking_status":         status,
        "customer_id":            customer_id,
        "vehicle_type":           vehicle,
        "pickup_location":        pickup,
        "drop_location":          drop,
        "avg_vtat":               avg_vtat,
        "avg_ctat":               avg_ctat,
        "booking_value":          fare,
        "ride_distance":          distance if status == "Completed" else None,
        "driver_ratings":         driver_rating,
        "customer_rating":        customer_rating,
        "payment_method":         payment if status == "Completed" else None,
        "cancelled_by_customer":  cancelled_by_customer,
        "cancelled_by_driver":    cancelled_by_driver,
        "incomplete_rides":       incomplete,
        "reason_for_cancelling_by_customer": reason_customer,
        "driver_cancellation_reason":        reason_driver,
    }

# ── Insert ride into database ──────────────────────────────────────────
def insert_ride(ride, cur):
    cur.execute("""
        INSERT INTO uber_rides (
            date, time, booking_id, booking_status, customer_id,
            vehicle_type, pickup_location, drop_location,
            avg_vtat, avg_ctat, booking_value, ride_distance,
            driver_ratings, customer_rating, payment_method
        ) VALUES (
            %(date)s, %(time)s, %(booking_id)s, %(booking_status)s,
            %(customer_id)s, %(vehicle_type)s, %(pickup_location)s,
            %(drop_location)s, %(avg_vtat)s, %(avg_ctat)s,
            %(booking_value)s, %(ride_distance)s, %(driver_ratings)s,
            %(customer_rating)s, %(payment_method)s
        )
    """, ride)

# ── Main loop ──────────────────────────────────────────────────────────
def run():
    print("🚗 Ride simulator starting...")
    print("Generating new rides every 2 seconds. Press Ctrl+C to stop.\n")

    tick = 0
    while True:
        try:
            conn = get_conn()
            cur  = conn.cursor()

            # Generate 2-5 rides per tick
            n = random.randint(2, 5)
            for _ in range(n):
                ride = generate_ride()
                insert_ride(ride, cur)

            conn.commit()
            cur.close()
            conn.close()

            tick += 1
            if tick % 10 == 0:
                print(f"[tick {tick}] ✅ {n} rides inserted — "
                      f"total simulated: ~{tick * 3}")

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(2)

if __name__ == "__main__":
    run()