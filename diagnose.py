#!/usr/bin/env python3
"""
Diagnostic script to check database and authentication
"""

from models import *
from auth import *

def diagnose_system():
    """Check if the system is working correctly"""
    print("=== System Diagnosis ===")
    
    # Check database
    print("\n1. Checking database...")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"   Found tables: {[table[0] for table in tables]}")
        
        # Check users table
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"   Users in database: {user_count}")
        
        # Check tasks table
        cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = cursor.fetchone()[0]
        print(f"   Tasks in database: {task_count}")
        
        # Check if due_date column exists
        cursor.execute("PRAGMA table_info(tasks)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"   Task table columns: {columns}")
        
        conn.close()
        print("   ✓ Database connection successful")
        
    except Exception as e:
        print(f"   ✗ Database error: {e}")
        return False
    
    # Check sample users
    print("\n2. Checking sample users...")
    sample_users = [
        'manager@company.com',
        'employee1@company.com', 
        'employee2@company.com',
        'employee3@company.com'
    ]
    
    for email in sample_users:
        user = get_user_by_email(email)
        if user:
            print(f"   ✓ {email}: {user['first_name']} {user['last_name']}")
        else:
            print(f"   ✗ {email}: Not found")
    
    # Check tasks for a user
    print("\n3. Checking tasks...")
    test_user = 'employee1@company.com'
    tasks = get_user_tasks(test_user)
    print(f"   Tasks for {test_user}: {len(tasks)}")
    for task in tasks:
        task_dict = dict(task)
        print(f"     - {task_dict['name']} (Due: {task_dict.get('due_date', 'None')})")
    
    print("\n=== Diagnosis Complete ===")
    return True

if __name__ == "__main__":
    diagnose_system() 