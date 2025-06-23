import sqlite3
import os

DB_FILE = "lsw.db"

def inspect_database():
    """
    Connects to the SQLite database and prints a list of tables and their schemas.
    """
    if not os.path.exists(DB_FILE):
        print(f"Database file not found: {DB_FILE}")
        return

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Get a list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        if not tables:
            print("No tables found in the database.")
            return

        print("Tables in the database:")
        for table_name_tuple in tables:
            table_name = table_name_tuple[0]
            if table_name == 'sqlite_sequence':
                continue
            print(f"\n--- Table: {table_name} ---")

            # Get the table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            schema = cursor.fetchall()
            print("Schema:")
            for column in schema:
                print(f"  {column[1]} ({column[2]})")

            # Get the first 5 rows of data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            rows = cursor.fetchall()
            print("\nSample Data (first 5 rows):")
            for row in rows:
                print(f"  {row}")
            print() # Add a newline for better separation

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    inspect_database() 