import sqlite3
import os
from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional

DATABASE_PATH = 'lsw.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_PATH, timeout=20.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            manager_email TEXT
        );
    """)
    
    # Create tasks table with due_date column
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            assigned_to TEXT NOT NULL,
            start_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            due_date DATE,
            completed BOOLEAN NOT NULL DEFAULT FALSE
        );
    """)
    
    # Add due_date column to existing tasks table if it doesn't exist
    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN due_date DATE")
    except sqlite3.OperationalError:
        # Column already exists, ignore error
        pass
    
    conn.commit()
    conn.close()

def execute_query(query: str, params: tuple = (), fetchone=False, fetchall=False, commit=False) -> Any:
    """Execute a database query safely"""
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        result = None
        if fetchone:
            row = cursor.fetchone()
            result = dict(row) if row else None
        if fetchall:
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
        if commit:
            conn.commit()
            
        return result
    except Exception as e:
        print(f"Database query error: {e}")
        if commit and conn:
            conn.rollback()
        return None if fetchone else []
    finally:
        if conn:
            conn.close()

def add_user(email: str, first_name: str, last_name: str, manager_email: Optional[str] = None):
    """Add a new user to the database"""
    query = "INSERT INTO users (email, first_name, last_name, manager_email) VALUES (?, ?, ?, ?)"
    execute_query(query, (email, first_name, last_name, manager_email), commit=True)

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    """Get a user by their email address"""
    query = "SELECT * FROM users WHERE email = ?"
    return execute_query(query, (email,), fetchone=True)

def get_direct_reports(manager_email: str) -> List[Dict[str, Any]]:
    """Get all direct reports for a manager"""
    query = "SELECT * FROM users WHERE manager_email = ?"
    return execute_query(query, (manager_email,), fetchall=True)

def get_user_tasks(email: str) -> List[Dict[str, Any]]:
    """Get all tasks for a user"""
    email = email.strip().lower()
    query = "SELECT * FROM tasks WHERE assigned_to = ? ORDER BY start_date DESC"
    return execute_query(query, (email,), fetchall=True)

def get_this_week_tasks(email: str) -> List[Dict[str, Any]]:
    """Get tasks for a user for the current week"""
    email = email.strip().lower()
    print(f"Fetching tasks for email: '{email}'")
    query = "SELECT * FROM tasks WHERE assigned_to = ? ORDER BY start_date DESC"
    result = execute_query(query, (email,), fetchall=True)
    print(f"Fetched {len(result)} tasks for {email}")
    for task in result:
        print(f"  - Task: {task['name']} (ID: {task['id']}, Completed: {task['completed']})")
    return result
    
def add_task(name: str, assigned_to: str, due_date: Optional[str] = None):
    """Add a new task with optional due date"""
    assigned_to = assigned_to.strip().lower()
    print(f"Adding task: '{name}' to '{assigned_to}' with due date: {due_date}")
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if due_date:
        query = "INSERT INTO tasks (name, assigned_to, start_date, due_date) VALUES (?, ?, ?, ?)"
        try:
            result = execute_query(query, (name, assigned_to, current_time, due_date), commit=True)
            print(f"Task added successfully with due date: {result}")
        except Exception as e:
            print(f"Failed to add task: {e}")
    else:
        query = "INSERT INTO tasks (name, assigned_to, start_date) VALUES (?, ?, ?)"
        try:
            result = execute_query(query, (name, assigned_to, current_time), commit=True)
            print(f"Task added successfully: {result}")
        except Exception as e:
            print(f"Failed to add task: {e}")
    return result

def update_task_due_date(task_id: int, due_date: Optional[str]):
    """Update the due date of a task"""
    if due_date:
        query = "UPDATE tasks SET due_date = ? WHERE id = ?"
        execute_query(query, (due_date, task_id), commit=True)
    else:
        query = "UPDATE tasks SET due_date = NULL WHERE id = ?"
        execute_query(query, (task_id,), commit=True)

def mark_task_completed(task_id: int):
    """Mark a task as completed"""
    query = "UPDATE tasks SET completed = TRUE WHERE id = ?"
    execute_query(query, (task_id,), commit=True)

def mark_task_uncompleted(task_id: int):
    """Mark a task as not completed"""
    query = "UPDATE tasks SET completed = FALSE WHERE id = ?"
    execute_query(query, (task_id,), commit=True)
    
def delete_task(task_id: int):
    """Delete a task"""
    query = "DELETE FROM tasks WHERE id = ?"
    execute_query(query, (task_id,), commit=True)

def get_manager_overview(manager_email: str) -> List[Dict[str, Any]]:
    """Get an overview of team task completion for a manager"""
    direct_reports = get_direct_reports(manager_email)
    overview = []
    
    if not direct_reports:
        return []

    for report in direct_reports:
        email = report['email']
        tasks = get_user_tasks(email)
        
        completed_count = sum(1 for task in tasks if task['completed'])
        total_count = len(tasks)
        completion_rate = (completed_count / total_count * 100) if total_count > 0 else 0
        
        overview.append({
            'user': report,
            'completed_count': completed_count,
            'total_count': total_count,
            'completion_rate': round(completion_rate, 1),
            'tasks': tasks
        })
    return overview

def get_overdue_tasks(email: str) -> List[Dict[str, Any]]:
    """Get overdue tasks for a user"""
    email = email.strip().lower()
    today = date.today().isoformat()
    query = """
        SELECT * FROM tasks 
        WHERE assigned_to = ? 
        AND due_date < ? 
        AND completed = FALSE 
        ORDER BY due_date ASC
    """
    return execute_query(query, (email, today), fetchall=True)

def get_upcoming_tasks(email: str, days: int = 7) -> List[Dict[str, Any]]:
    """Get tasks due within the next N days for a user"""
    email = email.strip().lower()
    today = date.today().isoformat()
    future_date = (date.today() + timedelta(days=days)).isoformat()
    query = """
        SELECT * FROM tasks 
        WHERE assigned_to = ? 
        AND due_date >= ? 
        AND due_date <= ? 
        AND completed = FALSE 
        ORDER BY due_date ASC
    """
    return execute_query(query, (email, today, future_date), fetchall=True)

def get_task_status(task: Dict[str, Any]) -> str:
    """Get the status of a task based on due date and completion"""
    if task['completed']:
        return 'completed'
    
    if not task['due_date']:
        return 'no_due_date'
    
    try:
        due_date = datetime.strptime(task['due_date'], '%Y-%m-%d').date()
        today = date.today()
        
        if due_date < today:
            return 'overdue'
        elif due_date == today:
            return 'due_today'
        elif due_date <= (today + timedelta(days=3)):
            return 'due_soon'
        else:
            return 'on_track'
    except (ValueError, TypeError) as e:
        print(f"Error parsing due date '{task['due_date']}': {e}")
        return 'no_due_date'

def get_user_tasks_with_status(email: str) -> List[Dict[str, Any]]:
    """Get all tasks for a user with status information"""
    tasks = get_user_tasks(email)
    for task in tasks:
        task['status'] = get_task_status(task)
    return tasks

# Initialize database when module is imported
if not os.path.exists('lsw.db'):
    init_db() 
    