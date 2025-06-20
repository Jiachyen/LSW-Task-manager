from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import *
from auth import *
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')  # Use environment variable in production

# Initialize database and add some sample data
def setup_sample_data():
    """Add sample users and tasks for testing"""
    # Add sample users
    sample_users = [
        ('manager@company.com', 'John', 'Manager', None),  # Manager
        ('employee1@company.com', 'Alice', 'Smith', 'manager@company.com'),
        ('employee2@company.com', 'Bob', 'Johnson', 'manager@company.com'),
        ('employee3@company.com', 'Carol', 'Davis', 'manager@company.com'),
    ]
    
    for email, first_name, last_name, manager_email in sample_users:
        add_user(email, first_name, last_name, manager_email)
    
    # Add sample tasks
    sample_tasks = [
        ('Complete weekly report', 'employee1@company.com'),
        ('Review project documentation', 'employee1@company.com'),
        ('Update team schedule', 'employee2@company.com'),
        ('Prepare presentation slides', 'employee2@company.com'),
        ('Conduct team meeting', 'employee3@company.com'),
        ('Submit expense reports', 'employee3@company.com'),
        # Add some tasks for the manager
        ('Review quarterly budget', 'manager@company.com'),
        ('Prepare board presentation', 'manager@company.com'),
        ('Schedule team training', 'manager@company.com'),
    ]
    
    for task_name, assigned_to in sample_tasks:
        add_task(task_name, assigned_to)

# Initialize database and sample data
if not os.path.exists('lsw.db'):
    init_db()
    setup_sample_data()

@app.route('/')
def index():
    if is_authenticated():
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        # Simple authentication - any password works as long as email exists
        if login_user(email):
            return redirect(url_for('home'))
        else:
            flash('Invalid email address', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@require_auth
def home():
    user = get_current_user()
    if user:
        tasks = get_this_week_tasks(user['email'])
        return render_template('home.html', tasks=tasks, user=user)
    return redirect(url_for('login'))

@app.route('/overview')
@require_manager
def overview():
    user = get_current_user()
    if user:
        overview_data = get_manager_overview(user['email'])
        return render_template('overview.html', overview_data=overview_data, user=user)
    return redirect(url_for('login'))

@app.route('/assign')
@require_manager
def assign():
    user = get_current_user()
    if user:
        direct_reports = get_direct_reports(user['email'])
        return render_template('assign.html', direct_reports=direct_reports, user=user)
    return redirect(url_for('login'))

@app.route('/assign_task', methods=['POST'])
@require_manager
def assign_task():
    task_name = request.form.get('task_name')
    assigned_to = request.form.get('assigned_to')
    
    if task_name and assigned_to:
        add_task(task_name, assigned_to)
        flash(f'Task "{task_name}" assigned successfully!', 'success')
    else:
        flash('Please provide both task name and assignee', 'error')
    
    return redirect(url_for('assign'))

@app.route('/complete_task', methods=['POST'])
@require_auth
def complete_task():
    task_id = request.form.get('task_id')
    if task_id:
        mark_task_completed(int(task_id))
        flash('Task marked as completed!', 'success')
    
    return redirect(url_for('home'))

@app.route('/uncomplete_task', methods=['POST'])
@require_auth
def uncomplete_task():
    task_id = request.form.get('task_id')
    if task_id:
        mark_task_uncompleted(int(task_id))
        flash('Task marked as incomplete!', 'success')
    
    return redirect(url_for('home'))

@app.route('/add_own_task', methods=['POST'])
@require_auth
def add_own_task():
    user = get_current_user()
    if user:
        task_name = request.form.get('task_name')
        if task_name:
            add_task(task_name, user['email'])
            flash(f'Task "{task_name}" added successfully!', 'success')
        else:
            flash('Please provide a task name', 'error')
    
    return redirect(url_for('home'))

@app.route('/delete_own_task', methods=['POST'])
@require_auth
def delete_own_task():
    user = get_current_user()
    if user:
        task_id = request.form.get('task_id')
        if task_id:
            # Verify the task belongs to the current user (both managers and employees)
            tasks = get_user_tasks(user['email'])
            task_exists = any(str(task['id']) == str(task_id) for task in tasks)
            
            if task_exists:
                delete_task(int(task_id))
                flash('Task deleted successfully!', 'success')
            else:
                flash('Task not found or you do not have permission to delete it.', 'error')
        else:
            flash('Task ID is required', 'error')
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Get port from environment variable (for deployment) or use 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    
    # For deployment platforms, always bind to 0.0.0.0
    print(f"Starting LSW Task Manager on port {port}")
    app.run(debug=False, host='0.0.0.0', port=port) 