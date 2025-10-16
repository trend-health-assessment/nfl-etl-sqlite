# NFL Player ETL + SQLite Analysis

ETL pipeline pulling **NFL player stats** from RapidAPI (Tank01) into SQLite.

## Prerequisites
- Python 3.10+
- RapidAPI key (sign up free)
- `pip install -r requirements.txt`

## Setup
```bash
set RAPIDAPI_KEY = <RAPIDAPI_KEY>
set RAPIDAPI_HOST = <RAPIDAPI_HOST>
set DB_PATH = nfl.db
python etl.py
