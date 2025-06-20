from flask import session, redirect, url_for
from models import get_user_by_email

def login_user(email):
    """Simple login - just store email in session"""
    user = get_user_by_email(email)
    if user:
        session['user_email'] = email
        session['user_name'] = f"{user['first_name']} {user['last_name']}"
        session['is_manager'] = bool(user['manager_email'] is None)  # No manager = is a manager
        return True
    return False

def logout_user():
    """Logout user by clearing session"""
    session.clear()

def get_current_user():
    """Get current user from session"""
    if 'user_email' in session:
        return get_user_by_email(session['user_email'])
    return None

def is_authenticated():
    """Check if user is authenticated"""
    return 'user_email' in session

def is_manager():
    """Check if current user is a manager"""
    return session.get('is_manager', False)

def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_manager(f):
    """Decorator to require manager role"""
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return redirect(url_for('login'))
        if not is_manager():
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function 