# Uber Ride Analytics Platform

A production-style real-time analytics platform built on 150,000 real Uber rides from India (2024). Features a live ride simulator, multi-page interactive dashboard and automated KPI tracking.

---

## Live Demo

🚀 [View Live Dashboard](https://uber-ride-analytics-2024.streamlit.app/)

---

## Architecture
Raw CSV Data (150K rides)
↓
Python ETL Pipeline (pandas + SQLAlchemy)
↓
PostgreSQL Database (8 analytics queries)
↓
Real-Time Simulator (generates new rides every 2s)
↓
Streamlit Dashboard (6 pages, auto-refreshes every 10s)

---

## Dashboard Pages

| Page | Description |
|---|---|
| Home | Landing page with live stats and interactive preview |
| Overview | KPIs, booking status, monthly trends, daily revenue |
| Vehicle Type | Revenue and ride share by vehicle category |
| Revenue | Monthly trends, payment methods, fare analysis |
| Cancellation | Customer vs driver cancellations with insights |
| Ratings | Driver and customer ratings by vehicle, radar chart |

---

## Key Features

- **Real-time simulation** — Python simulator generates new rides every 2 seconds
- **Auto-refresh dashboard** — Streamlit refreshes every 10 seconds with live data
- **Multi-page architecture** — modular components and views
- **150,000 real rides** — real Kaggle dataset, not synthetic data
- **Professional dark UI** — enterprise-style design with Plotly charts

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python | Data pipeline, simulator, analytics |
| PostgreSQL | Database for all ride data |
| SQLAlchemy | Database ORM and query engine |
| Streamlit | Multi-page web dashboard |
| Plotly | Interactive charts and visualizations |
| Pandas | Data manipulation and ETL |

---

## Key Metrics from Dataset

| Metric | Value |
|---|---|
| Total bookings | 150,000 |
| Completed rides | 93,000 |
| Success rate | 62% |
| Total revenue | ₹47M |
| Avg fare | ₹508 |
| Avg distance | 26 km |
| Avg driver rating | 4.23 / 5.0 |
| Avg customer rating | 4.40 / 5.0 |

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/uber-ride-analytics.git
cd uber-ride-analytics
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL

Create a database called `rideshare` and copy `.env.example` to `.env`:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=rideshare
DB_USER=postgres
DB_PASSWORD=yourpassword

### 5. Download dataset

Download the Uber Ride Analytics Dataset from Kaggle and save as `data/uber_data.csv`

[Kaggle Dataset Link](https://www.kaggle.com/datasets/uber-ride-analytics-2024)

### 6. Load the data

```bash
python data/load_data.py
```

### 7. Run the simulator (Terminal 1)

```bash
python simulator/ride_simulator.py
```

### 8. Run the dashboard (Terminal 2)

```bash
streamlit run dashboard/app.py
```

Open `http://localhost:8501` in your browser.

---

## Screenshots

### Home Page
![Home](dashboard/assets/uber_logo.jpg)

---

## What This Project Demonstrates

- **Data Engineering** — ETL pipeline from raw CSV to PostgreSQL
- **Analytics Engineering** — 8 SQL-backed KPI functions
- **Real-time Systems** — live simulator + auto-refresh dashboard
- **Dashboard Engineering** — 6-page modular Streamlit application
- **Software Architecture** — clean separation of components, views and data layer
- **Business Intelligence** — operational KPIs, trends and anomaly detection

---


## Author

Built as part of a data engineering portfolio targeting analytics and BI roles.

- GitHub: https://github.com/anuja2024
- LinkedIn: https://www.linkedin.com/in/anujapatade/
