import pandas as pd
import sqlite3
import os

def init_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "raw", "complaints.csv")
    db_path = os.path.join(base_dir, "sql", "complaints.db")
    
    print(f"Loading raw data from {csv_path}...")
    # Use low_memory=False for mixed types
    df = pd.read_csv(csv_path, low_memory=False)
    
    print("Converting 'Date received'...")
    date_col = 'Date received' if 'Date received' in df.columns else 'Date Received'
    if date_col in df.columns:
        # Handling the DD-MM-YYYY format in the CSV
        df[date_col] = pd.to_datetime(df[date_col], format='%d-%m-%Y', errors='coerce')
    else:
        print(f"Warning: Could not find Date Received column. Available columns: {df.columns.tolist()}")
    
    print(f"Saving to database at {db_path}...")
    with sqlite3.connect(db_path) as conn:
        df.to_sql("complaints", conn, if_exists="replace", index=False)
        
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
