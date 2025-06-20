#!/usr/bin/env python3
"""
LSW Task Manager - Startup Script
"""

import sys
import os

def main():
    try:
        # Import and run the Flask app
        from app import app
        
        print("=" * 50)
        print("LSW Task Manager")
        print("=" * 50)
        print("Starting server...")
        print("Access the application at: http://127.0.0.1:5000")
        print("Press Ctrl+C to stop the server")
        print("=" * 50)
        
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except ImportError as e:
        print(f"Error: Could not import required modules. {e}")
        print("Make sure you have installed the requirements:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting the application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 