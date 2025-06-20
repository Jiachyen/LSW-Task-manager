import sqlite3
from datetime import datetime
import os

DATABASE_PATH = 'lsw.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            manager_email TEXT,
            FOREIGN KEY (manager_email) REFERENCES users (email)
        )
    ''')
    
    # Create Tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            assigned_to TEXT NOT NULL,
            start_date DATE NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (assigned_to) REFERENCES users (email)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(email, first_name, last_name, manager_email=None):
    """Add a new user to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (email, first_name, last_name, manager_email)
            VALUES (?, ?, ?, ?)
        ''', (email, first_name, last_name, manager_email))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_by_email(email):
    """Get user by email"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    return user

def get_all_users():
    """Get all users"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users ORDER BY first_name, last_name')
    users = cursor.fetchall()
    conn.close()
    
    return users

def get_direct_reports(manager_email):
    """Get all direct reports for a manager"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE manager_email = ? ORDER BY first_name, last_name', (manager_email,))
    direct_reports = cursor.fetchall()
    conn.close()
    
    return direct_reports

def add_task(name, assigned_to):
    """Add a new task"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO tasks (name, assigned_to, start_date)
        VALUES (?, ?, ?)
    ''', (name, assigned_to, datetime.now().date()))
    conn.commit()
    conn.close()

def get_user_tasks(email):
    """Get all tasks for a specific user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM tasks 
        WHERE assigned_to = ? 
        ORDER BY start_date DESC
    ''', (email,))
    tasks = cursor.fetchall()
    conn.close()
    
    return tasks

def get_this_week_tasks(email):
    """Get tasks for this week for a specific user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get the start of this week (Monday)
    from datetime import datetime, timedelta
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    cursor.execute('''
        SELECT * FROM tasks 
        WHERE assigned_to = ? 
        AND start_date BETWEEN ? AND ?
        ORDER BY start_date DESC
    ''', (email, start_of_week, end_of_week))
    tasks = cursor.fetchall()
    conn.close()
    
    return tasks

def mark_task_completed(task_id):
    """Mark a task as completed"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE tasks SET completed = TRUE WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def mark_task_uncompleted(task_id):
    """Mark a task as incomplete"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE tasks SET completed = FALSE WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    """Delete a task from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def get_manager_overview(manager_email):
    """Get overview of direct reports' task completion for this week"""
    direct_reports = get_direct_reports(manager_email)
    overview = []
    
    for report in direct_reports:
        tasks = get_this_week_tasks(report['email'])
        completed_count = sum(1 for task in tasks if task['completed'])
        total_count = len(tasks)
        
        overview.append({
            'user': report,
            'tasks': tasks,
            'completed_count': completed_count,
            'total_count': total_count,
            'completion_rate': (completed_count / total_count * 100) if total_count > 0 else 0
        })
    
    return overview

# Initialize database when module is imported
if not os.path.exists(DATABASE_PATH):
    init_db() 