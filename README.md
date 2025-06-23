# LSW Task Manager

A simple task assignment and management app for managers built with Flask, SQLite, and modern web technologies.

## 🌐 Live Demo

**Live Demo:** [Coming Soon - Deploy to get your URL]

*Note: This app needs to be deployed to a hosting platform to be accessible online. See deployment options below.*

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jiachyen/LSW-Task-manager.git
   cd LSW-Task-manager
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser and go to:** `http://127.0.0.1:5000`

## 🔑 Sample Login Credentials

### Manager Account:
- **Email:** `manager@company.com`
- **Password:** `anything` (any password works)

### Employee Accounts:
- **Email:** `employee1@company.com`, `employee2@company.com`, `employee3@company.com`
- **Password:** `anything` (any password works)

## 🚀 Deployment Options

To make your app accessible to others online, deploy to one of these platforms:

### Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository
5. Get your live URL instantly

### PythonAnywhere
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Create free account
3. Upload code or connect GitHub
4. Configure as Flask app

### Heroku
1. Go to [heroku.com](https://heroku.com)
2. Create account and connect GitHub
3. Deploy from repository

## Features

- **User Authentication**: Simple email-based login system
- **Task Management**: Create, assign, and track tasks
- **Manager Dashboard**: Overview of team task completion status
- **Employee Dashboard**: View and mark tasks as completed
- **Responsive Design**: Works on desktop and mobile devices
- **Stryker Branding**: Professional black and yellow theme

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Templates**: Jinja2
- **Styling**: Custom CSS with Stryker branding

## Project Structure

```
LSW-Task-manager/
├── app.py              # Main Flask application
├── models.py           # Database models and functions
├── auth.py             # Authentication functions
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── home.html
│   ├── overview.html
│   └── assign.html
└── static/            # Static files (CSS, JS, images)
    ├── css/
    ├── js/
    └── images/
```

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

## License

This project is open source and available under the [MIT License](LICENSE). 