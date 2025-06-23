#!/usr/bin/env python3
"""
Debug script to test task functionality
"""

from models import *
from auth import *

def test_task_functionality():
    print("=== Testing Task Functionality ===")
    
    # Test 1: Check if user exists
    test_email = "employee1@company.com"
    user = get_user_by_email(test_email)
    print(f"1. User {test_email} exists: {user is not None}")
    if user:
        print(f"   User details: {dict(user)}")
    
    # Test 2: Add a test task
    test_task_name = "DEBUG TEST TASK"
    print(f"\n2. Adding test task: '{test_task_name}' to '{test_email}'")
    add_task(test_task_name, test_email)
    
    # Test 3: Get tasks for user
    print(f"\n3. Getting tasks for {test_email}")
    tasks = get_user_tasks(test_email)
    print(f"   Found {len(tasks)} tasks:")
    for task in tasks:
        print(f"   - ID: {task['id']}, Name: '{task['name']}', Completed: {task['completed']}")
    
    # Test 4: Get this week's tasks
    print(f"\n4. Getting this week's tasks for {test_email}")
    week_tasks = get_this_week_tasks(test_email)
    print(f"   Found {len(week_tasks)} tasks:")
    for task in week_tasks:
        print(f"   - ID: {task['id']}, Name: '{task['name']}', Completed: {task['completed']}")
    
    # Test 5: Check database directly
    print(f"\n5. Checking database directly:")
    import sqlite3
    conn = sqlite3.connect('lsw.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE assigned_to = ? ORDER BY id DESC", (test_email,))
    db_tasks = cursor.fetchall()
    print(f"   Database shows {len(db_tasks)} tasks for {test_email}:")
    for task in db_tasks:
        print(f"   - ID: {task[0]}, Name: '{task[1]}', Assigned to: '{task[2]}', Completed: {task[4]}")
    conn.close()

if __name__ == "__main__":
    test_task_functionality() 