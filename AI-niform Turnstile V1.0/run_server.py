#!/usr/bin/env python3
"""
AI-niform Server Launcher
This script helps you run your web server with different configurations
for local network access and external access.
"""

import subprocess
import sys
import socket
import argparse
from pathlib import Path

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def check_port_available(port):
    """Check if a port is available"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.close()
        return True
    except OSError:
        return False

def main():
    parser = argparse.ArgumentParser(description='AI-niform Server Launcher')
    parser.add_argument('--port', '-p', type=int, default=5000, help='Port to run on (default: 5000)')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0 for all interfaces)')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--production', action='store_true', help='Run in production mode')
    
    args = parser.parse_args()
    
    # Check if port is available
    if not check_port_available(args.port):
        print(f"❌ Port {args.port} is already in use!")
        print(f"💡 Try a different port: python run_server.py --port 8080")
        sys.exit(1)
    
    local_ip = get_local_ip()
    
    print(f"\n🚀 AI-niform Server Configuration")
    print(f"📡 Host: {args.host}")
    print(f"🔌 Port: {args.port}")
    print(f"🐛 Debug: {args.debug or not args.production}")
    print(f"\n📱 Access URLs:")
    print(f"   Local: http://localhost:{args.port}")
    print(f"   Network: http://{local_ip}:{args.port}")
    print(f"\n💡 For mobile/tablet access:")
    print(f"   1. Connect device to same WiFi network")
    print(f"   2. Open browser and go to: http://{local_ip}:{args.port}")
    print(f"\n💡 For external internet access:")
    print(f"   1. Configure router port forwarding (port {args.port})")
    print(f"   2. Use your public IP address")
    print(f"\n🛑 Press Ctrl+C to stop the server\n")
    
    # Prepare command
    cmd = [sys.executable, "web_server.py"]
    
    # Override the port in web_server.py by setting environment variable
    import os
    os.environ['FLASK_PORT'] = str(args.port)
    os.environ['FLASK_HOST'] = args.host
    os.environ['FLASK_DEBUG'] = str(args.debug or not args.production)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    main()




