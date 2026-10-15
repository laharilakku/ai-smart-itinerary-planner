-- Smart Itinerary — Initial Schema

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    preferred_currency VARCHAR(10) DEFAULT 'INR',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trips
CREATE TYPE trip_status AS ENUM ('draft', 'planned', 'ongoing', 'completed');

CREATE TABLE IF NOT EXISTS trips (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    title VARCHAR(200) NOT NULL,
    destination VARCHAR(200) NOT NULL,
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    status trip_status DEFAULT 'draft',
    total_budget FLOAT DEFAULT 0,
    currency VARCHAR(10) DEFAULT 'INR',
    notes TEXT,
    optimized_route JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Attractions
CREATE TABLE IF NOT EXISTS attractions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    rating FLOAT DEFAULT 0,
    visit_duration_hrs FLOAT DEFAULT 1,
    entry_fee FLOAT DEFAULT 0,
    description TEXT,
    tags JSONB DEFAULT '[]',
    feature_vector JSONB,
    cluster_id INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trip Stops
CREATE TABLE IF NOT EXISTS trip_stops (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    attraction_id INTEGER REFERENCES attractions(id),
    order_index INTEGER DEFAULT 0,
    name VARCHAR(200),
    latitude FLOAT,
    longitude FLOAT,
    arrival_time TIMESTAMPTZ,
    departure_time TIMESTAMPTZ,
    travel_time_to_next_mins FLOAT,
    distance_to_next_km FLOAT,
    notes TEXT
);

-- Expenses
CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    trip_id INTEGER NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    category VARCHAR(100),
    description VARCHAR(300),
    amount FLOAT NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    amount_inr FLOAT,
    date TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_trips_user ON trips(user_id);
CREATE INDEX idx_stops_trip ON trip_stops(trip_id);
CREATE INDEX idx_attractions_city ON attractions(city);
CREATE INDEX idx_expenses_trip ON expenses(trip_id);
