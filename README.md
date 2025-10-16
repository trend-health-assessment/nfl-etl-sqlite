# NFL Player ETL + SQLite Analysis

ETL pipeline pulling **NFL player stats** from RapidAPI (Tank01) into SQLite.

## Prerequisites
- Python 3.10+
- RapidAPI key (sign up free)
- `pip install -r requirements.txt`

## Setup
```bash
## Windows (Command Prompt)
set RAPIDAPI_KEY = <RAPIDAPI_KEY>
set RAPIDAPI_HOST = <RAPIDAPI_HOST>
set DB_PATH = nfl.db

## Windows (Powershell)
$env:RAPIDAPI_KEY = <RAPIDAPI_KEY>
$env:RAPIDAPI_HOST = <RAPIDAPI_HOST>
$env:DB_PATH = nfl.db

## Linux/MacOS
export RAPIDAPI_KEY = <RAPIDAPI_KEY>
export RAPIDAPI_HOST = <RAPIDAPI_HOST>
export DB_PATH = nfl.db

python etl.py
