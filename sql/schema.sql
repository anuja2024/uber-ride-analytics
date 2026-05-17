CREATE TABLE IF NOT EXISTS cities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lat FLOAT NOT NULL,
    lon FLOAT NOT NULL,
    base_demand INTEGER DEFAULT 100
);

CREATE TABLE IF NOT EXISTS drivers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city_id INTEGER REFERENCES cities(id),
    status VARCHAR(20) DEFAULT 'available',
    rating FLOAT DEFAULT 4.5,
    total_trips INTEGER DEFAULT 0,
    joined_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rides (
    id SERIAL PRIMARY KEY,
    driver_id INTEGER REFERENCES drivers(id),
    city_id INTEGER REFERENCES cities(id),
    status VARCHAR(20) NOT NULL,
    pickup_lat FLOAT,
    pickup_lon FLOAT,
    dropoff_lat FLOAT,
    dropoff_lon FLOAT,
    requested_at TIMESTAMP DEFAULT NOW(),
    accepted_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    fare FLOAT,
    distance_km FLOAT,
    surge_multiplier FLOAT DEFAULT 1.0,
    wait_time_seconds INTEGER,
    trip_duration_seconds INTEGER
);

CREATE TABLE IF NOT EXISTS surge_events (
    id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(id),
    multiplier FLOAT NOT NULL,
    triggered_at TIMESTAMP DEFAULT NOW(),
    demand_count INTEGER,
    available_drivers INTEGER
);

INSERT INTO cities (name, lat, lon, base_demand) VALUES
    ('Berlin', 52.52, 13.40, 150),
    ('Munich', 48.14, 11.58, 120),
    ('Hamburg', 53.55, 10.00, 110),
    ('Frankfurt', 50.11, 8.68, 100),
    ('Cologne', 50.94, 6.96, 90),
    ('Dortmund', 51.51, 7.46, 80)
ON CONFLICT DO NOTHING;