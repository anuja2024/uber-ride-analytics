import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

def get_engine():
    host     = os.getenv("DB_HOST", "localhost")
    port     = int(os.getenv("DB_PORT", 5432))
    database = os.getenv("DB_NAME", "rideshare")
    user     = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}?sslmode=require"
    return create_engine(url)

def get_kpis():
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT
                COUNT(*) AS total_bookings,
                ROUND(AVG(booking_value)::numeric, 2) AS avg_fare,
                ROUND(SUM(booking_value)::numeric, 2) AS total_revenue,
                ROUND(AVG(ride_distance)::numeric, 2) AS avg_distance,
                ROUND(AVG(driver_ratings)::numeric, 2) AS avg_driver_rating,
                ROUND(AVG(customer_rating)::numeric, 2) AS avg_customer_rating
            FROM uber_rides
            WHERE booking_status = 'Completed'
        """), conn)
    return df.iloc[0]

def get_bookings_by_status():
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT booking_status, COUNT(*) AS total
            FROM uber_rides
            GROUP BY booking_status
            ORDER BY total DESC
        """), conn)
    return df

def get_revenue_by_vehicle():
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT
                vehicle_type,
                COUNT(*) AS total_rides,
                ROUND(SUM(booking_value)::numeric, 2) AS total_revenue,
                ROUND(AVG(booking_value)::numeric, 2) AS avg_fare,
                ROUND(AVG(ride_distance)::numeric, 2) AS avg_distance,
                ROUND(AVG(driver_ratings)::numeric, 2) AS avg_rating
            FROM uber_rides
            WHERE booking_status = 'Completed'
            GROUP BY vehicle_type
            ORDER BY total_revenue DESC
        """), conn)
    return df

def get_bookings_over_time():
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT
                date,
                COUNT(*) AS total_bookings,
                ROUND(SUM(booking_value)::numeric, 2) AS daily_revenue,
                COUNT(*) FILTER (WHERE booking_status = 'Completed') AS completed
            FROM uber_rides
            GROUP BY date
            ORDER BY date
        """), conn)
    return df

def get_payment_method_split():
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT
                payment_method,
                COUNT(*) AS total,
                ROUND(SUM(booking_value)::numeric, 2) AS revenue
            FROM uber_rides
            WHERE booking_status = 'Completed'
            GROUP BY payment_method
            ORDER BY revenue DESC
        """), conn)
    return df

def get_cancellation_reasons():
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT
                'Customer' AS cancelled_by,
                COUNT(*) AS total
            FROM uber_rides
            WHERE booking_status = 'Cancelled by Customer'

            UNION ALL

            SELECT
                'Driver' AS cancelled_by,
                COUNT(*) AS total
            FROM uber_rides
            WHERE booking_status = 'Cancelled by Driver'
        """), conn)
    return df

def get_ratings_by_vehicle():
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT
                vehicle_type,
                ROUND(AVG(driver_ratings)::numeric, 2) AS avg_driver_rating,
                ROUND(AVG(customer_rating)::numeric, 2) AS avg_customer_rating,
                COUNT(*) AS total_rides
            FROM uber_rides
            WHERE booking_status = 'Completed'
            GROUP BY vehicle_type
            ORDER BY avg_customer_rating DESC
        """), conn)
    return df

def get_top_routes():
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT
                pickup_location,
                drop_location,
                COUNT(*) AS total_rides,
                ROUND(AVG(booking_value)::numeric, 2) AS avg_fare
            FROM uber_rides
            WHERE booking_status = 'Completed'
            GROUP BY pickup_location, drop_location
            ORDER BY total_rides DESC
            LIMIT 10
        """), conn)
    return df

def get_monthly_stats():
    engine = get_engine()
    with engine.connect() as conn:
        df = pd.read_sql(text("""
            SELECT
                TO_CHAR(date::date, 'Mon YYYY') AS month,
                DATE_TRUNC('month', date::date) AS month_date,
                COUNT(*) AS total_bookings,
                ROUND(SUM(booking_value)::numeric, 2) AS monthly_revenue,
                COUNT(*) FILTER (WHERE booking_status = 'Completed') AS completed
            FROM uber_rides
            GROUP BY month, month_date
            ORDER BY month_date
        """), conn)
    return df