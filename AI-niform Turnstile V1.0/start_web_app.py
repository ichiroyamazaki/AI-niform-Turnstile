#!/usr/bin/env python3
"""
AI Uniform System - Web Application Launcher
This script starts the modern web application with proper configuration.
"""

import os
import sys
import webbrowser
import time
from threading import Timer

def open_browser():
    """Open the web browser after a short delay"""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://127.0.0.1:5000')

def main():
    """Main function to start the web application"""
    print("🎓 AI Uniform System - Web Application")
    print("=" * 50)
    
    # Check if required files exist
    required_files = [
        'modern_login_ui.py',
        'users.txt',
        'templates/login.html',
        'templates/guidance_dashboard.html',
        'templates/admin_dashboard.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all files are present before starting the application.")
        return False
    
    print("✅ All required files found")
    print("🚀 Starting web application...")
    print("📱 The application will open in your default browser")
    print("🌐 Access URLs:")
    print("   - http://127.0.0.1:5000")
    print("   - http://localhost:5000")
    print("\n🔑 Demo Credentials:")
    print("   - Username: guidance1")
    print("   - Password: guidance123")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Open browser in a separate thread
    Timer(1.0, open_browser).start()
    
    # Start the Flask application
    try:
        from modern_login_ui import app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down web application...")
        print("Thank you for using AI Uniform System!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)





