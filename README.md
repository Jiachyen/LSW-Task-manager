# LSW Task Manager

A simple task assignment and management app for managers built with Flask, SQLite, and modern web technologies.

## Features

- **User Authentication**: Simple email-based login system
- **Task Management**: Create, assign, and track tasks
- **Manager Dashboard**: Overview of team task completion status
- **Employee Dashboard**: View and mark tasks as completed
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Templating**: Jinja2
- **Styling**: Custom CSS with modern design

## File Structure

```
DefensiveSatisfiedCertification/
├── app.py                 # Main Flask application
├── models.py              # Database models and functions
├── auth.py                # Authentication functions
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── lsw.db                # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── home.html         # Employee dashboard
│   ├── overview.html     # Manager overview
│   └── assign.html       # Task assignment page
└── static/               # Static files
    ├── css/
    │   └── styles.css    # Main stylesheet
    ├── js/
    │   └── script.js     # JavaScript functionality
    └── images/           # Image assets (empty)
```

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your web browser and go to `http://127.0.0.1:5000`

## Usage

### Sample Accounts

The app comes with pre-configured sample accounts:

- **Manager**: `manager@company.com` (any password)
- **Employee 1**: `employee1@company.com` (any password)
- **Employee 2**: `employee2@company.com` (any password)
- **Employee 3**: `employee3@company.com` (any password)

### For Managers

1. **Login** with manager credentials
2. **View Team Overview** to see task completion status
3. **Assign Tasks** to team members
4. **Monitor Progress** through the overview dashboard
5. **Manage Own Tasks** - add, complete, and delete personal tasks
6. **Track Personal Progress** with built-in statistics

### For Employees

1. **Login** with employee credentials
2. **View Tasks** assigned for the current week
3. **Mark Tasks Complete** as you finish them
4. **Mark Tasks Incomplete** if you need to undo completion
5. **Add Your Own Tasks** for personal work items
6. **Delete Your Own Tasks** if they're no longer needed
7. **Track Progress** with built-in statistics

## Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `first_name`: User's first name
- `last_name`: User's last name
- `manager_email`: Email of the user's manager (NULL for managers)

### Tasks Table
- `id`: Primary key
- `name`: Task description
- `assigned_to`: Email of the assigned user
- `start_date`: Date when task was created
- `completed`: Boolean flag for completion status

## Features

### Authentication
- Simple email-based login
- Session management
- Role-based access control (Manager vs Employee)

### Task Management
- Create and assign tasks to team members (managers)
- Add personal tasks (managers and employees)
- Track completion status
- Mark tasks as complete/incomplete
- Delete personal tasks
- Weekly task filtering
- Progress visualization

### User Interface
- Modern, responsive design
- Interactive elements
- Progress bars and statistics
- Mobile-friendly layout

### Security Features
- Form validation
- CSRF protection (built into Flask)
- Input sanitization

## Development

### Adding New Users

To add new users, you can modify the `setup_sample_data()` function in `app.py` or add them directly to the database.

### Customizing Styles

Edit `static/css/styles.css` to customize the appearance of the application.

### Adding Features

The modular structure makes it easy to add new features:
- Add new routes in `app.py`
- Create new database functions in `models.py`
- Add new templates in `templates/`
- Extend JavaScript functionality in `static/js/script.js`

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py` line 75
2. **Database errors**: Delete `lsw.db` and restart the app
3. **Import errors**: Ensure all dependencies are installed

### Database Management

The SQLite database (`lsw.db`) is created automatically when you first run the app. You can use tools like DB Browser for SQLite to inspect and modify the database directly.

## Future Enhancements

Potential improvements for future versions:
- Password authentication
- Email notifications
- Task categories and priorities
- Time tracking
- Reporting and analytics
- User profile management
- API endpoints for mobile apps

## License

This project is for educational and demonstration purposes. 