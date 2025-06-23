#!/usr/bin/env python3
"""
Fix database to add due_date column if it doesn't exist
"""

import sqlite3
import os

def fix_database():
    """Add due_date column to existing database if it doesn't exist"""
    db_path = 'lsw.db'
    
    if not os.path.exists(db_path):
        print("Database doesn't exist, creating new one...")
        from models import init_db
        init_db()
        return
    
    print("Checking database structure...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if due_date column exists
    cursor.execute("PRAGMA table_info(tasks)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'due_date' not in columns:
        print("Adding due_date column to tasks table...")
        try:
            cursor.execute("ALTER TABLE tasks ADD COLUMN due_date DATE")
            conn.commit()
            print("Successfully added due_date column!")
        except sqlite3.OperationalError as e:
            print(f"Error adding column: {e}")
    else:
        print("due_date column already exists.")
    
    # Check if there are any NULL values in due_date and set them to NULL explicitly
    cursor.execute("UPDATE tasks SET due_date = NULL WHERE due_date = ''")
    conn.commit()
    
    conn.close()
    print("Database fix completed!")

if __name__ == "__main__":
    fix_database() 