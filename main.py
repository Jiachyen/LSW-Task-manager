from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskapp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Make 'zip' available globally in all templates
app.jinja_env.globals.update(zip=zip)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), default='user')
    tasks = db.relationship('Task', backref='owner', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

def setup():
    with app.app_context():
        db.create_all()
        # Create users if not exist
        for username, password, role in [('user1', 'pass1', 'user'), ('user2', 'pass2', 'user'), ('admin', 'adminpass', 'admin')]:
            if not User.query.filter_by(username=username).first():
                user = User(username=username, password=password, role=role)
                db.session.add(user)
        db.session.commit()

        # Add initial tasks per user if none exist
        users = User.query.filter(User.role != 'admin').all()
        for user in users:
            if Task.query.filter_by(user_id=user.id).count() == 0:
                db.session.add(Task(name=f'{user.username} Task 1', user_id=user.id))
                db.session.add(Task(name=f'{user.username} Task 2', user_id=user.id))
        db.session.commit()

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('dashboard'))
        else:
            error = 'Invalid credentials'

    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks, user=current_user)

@app.route('/update_tasks', methods=['POST'])
@login_required
def update_tasks():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))

    completed_task_ids = request.form.getlist('completed_tasks')
    tasks = Task.query.filter_by(user_id=current_user.id).all()

    for task in tasks:
        # Allow checking completed or incomplete, no unchecking completed
        if not task.completed:
            task.completed = str(task.id) in completed_task_ids
    db.session.commit()

    return redirect(url_for('dashboard'))

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))

    task_name = request.form.get('task_name')
    if task_name:
        new_task = Task(name=task_name, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    # Only allow user to delete their own tasks
    if task.user_id != current_user.id:
        abort(403)  # Forbidden
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

# --- Admin dashboard with Edit button ---
@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))

    users = User.query.filter(User.role != 'admin').all()

    users_tasks = {
        user.username: [(task.name, task.completed) for task in user.tasks]
        for user in users
    }

    return render_template('admin_dashboard.html', users_tasks=users_tasks, users=users)


# --- New route: Edit user tasks page ---
@app.route('/admin/user/<int:user_id>/edit', methods=['GET'])
@login_required
def edit_user_tasks(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    tasks = Task.query.filter_by(user_id=user.id).all()
    return render_template('edit_user_tasks.html', user=user, tasks=tasks)

# --- Add task for a user (admin) ---
@app.route('/admin/user/<int:user_id>/add_task', methods=['POST'])
@login_required
def admin_add_task(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))

    user = User.query.get_or_404(user_id)
    task_name = request.form.get('task_name')
    if task_name:
        new_task = Task(name=task_name, user_id=user.id)
        db.session.add(new_task)
        db.session.commit()
        flash(f'Task "{task_name}" added for {user.username}.', 'success')
    return redirect(url_for('edit_user_tasks', user_id=user.id))

# --- Delete task for a user (admin) ---
@app.route('/admin/user/<int:user_id>/delete_task/<int:task_id>', methods=['POST'])
@login_required
def admin_delete_task(user_id, task_id):
    if current_user.role != 'admin':
        return redirect(url_for('dashboard'))

    task = Task.query.get_or_404(task_id)
    if task.user_id != user_id:
        abort(403)

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('edit_user_tasks', user_id=user_id))


if __name__ == '__main__':
    setup()
    app.run(host='0.0.0.0', port=5000, debug=True)

