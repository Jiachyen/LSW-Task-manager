#!/usr/bin/env python3
"""
Test script for due date functionality
"""

from models import *
from datetime import date, timedelta

def test_due_date_functionality():
    """Test the due date functionality"""
    print("Testing due date functionality...")
    
    # Initialize database
    init_db()
    
    # Add test tasks with different due dates
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(days=7)
    
    # Add test user if not exists
    test_email = "test@example.com"
    if not get_user_by_email(test_email):
        add_user(test_email, "Test", "User")
    
    # Add tasks with different due dates
    add_task("Overdue Task", test_email, yesterday.isoformat())
    add_task("Due Today Task", test_email, today.isoformat())
    add_task("Due Tomorrow Task", test_email, tomorrow.isoformat())
    add_task("Due Next Week Task", test_email, next_week.isoformat())
    add_task("No Due Date Task", test_email)
    
    # Get tasks and test status
    tasks = get_user_tasks_with_status(test_email)
    
    print(f"\nFound {len(tasks)} tasks:")
    for task in tasks:
        status = get_task_status(task)
        due_date_str = task.get('due_date', 'No due date')
        print(f"- {task['name']}: Due {due_date_str}, Status: {status}")
    
    # Test overdue tasks
    overdue_tasks = get_overdue_tasks(test_email)
    print(f"\nOverdue tasks: {len(overdue_tasks)}")
    for task in overdue_tasks:
        print(f"- {task['name']}: Due {task['due_date']}")
    
    # Test upcoming tasks
    upcoming_tasks = get_upcoming_tasks(test_email, days=7)
    print(f"\nUpcoming tasks (next 7 days): {len(upcoming_tasks)}")
    for task in upcoming_tasks:
        print(f"- {task['name']}: Due {task['due_date']}")
    
    print("\nDue date functionality test completed!")

if __name__ == "__main__":
    test_due_date_functionality() 