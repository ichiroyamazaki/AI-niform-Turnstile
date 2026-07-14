import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import json
import os
from datetime import datetime
import math
from firebase_config import firebase_manager, add_to_firebase, search_in_firebase, get_from_firebase

class ModernGuidanceLogin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Uniform System - Guidance Login")
        
        # Set reasonable window size
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#ffffff")
        
        # Center the window
        self.center_window()
        
        # Configure style
        self.setup_styles()
        
        # Create main interface
        self.create_interface()
        
        # Load sample users
        self.load_sample_users()
        
        # Bind Enter key
        self.root.bind('<Return>', lambda event: self.login())
        
        # Focus on username entry
        self.username_entry.focus()
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Setup modern styles for the UI"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure("Title.TLabel", 
                           font=("Segoe UI", 24, "bold"),
                           foreground="#1877f2",
                           background="#ffffff")
        
        self.style.configure("Subtitle.TLabel",
                           font=("Segoe UI", 16),
                           foreground="#65676b",
                           background="#ffffff")
        
        self.style.configure("Field.TLabel",
                           font=("Segoe UI", 12, "bold"),
                           foreground="#1c1e21",
                           background="#ffffff")
        
        self.style.configure("Modern.TButton",
                           font=("Segoe UI", 16, "bold"),
                           background="#1877f2",
                           foreground="#ffffff")
        
        self.style.map("Modern.TButton",
                      background=[('active', '#166fe5')])
    
    def create_interface(self):
        """Create the main login interface"""
        # Main container with Facebook-style design
        main_container = tk.Frame(self.root, bg="#ffffff")
        main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Logo/Icon with Facebook-style design
        logo_frame = tk.Frame(main_container, bg="#ffffff", height=60)
        logo_frame.pack(fill=tk.X, pady=(20, 20))
        logo_frame.pack_propagate(False)
        
        # Facebook-style logo
        logo_label = tk.Label(logo_frame, 
                             text="🎓", 
                             font=("Segoe UI", 36),
                             bg="#ffffff",
                             fg="#1877f2")
        logo_label.pack()
        
        # Title with Facebook blue
        title_label = ttk.Label(main_container, 
                               text="AI Uniform System",
                               style="Title.TLabel")
        title_label.pack(pady=(0, 10))
        
        # Subtitle with Facebook gray
        subtitle_label = ttk.Label(main_container,
                                   text="Guidance Counselor Portal",
                                   style="Subtitle.TLabel")
        subtitle_label.pack(pady=(0, 30))
        
                # Facebook-style form container with border
        form_frame = tk.Frame(main_container, bg="#ffffff", relief="solid", bd=2)
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Form inner with proper padding
        form_inner = tk.Frame(form_frame, bg="#ffffff", padx=30, pady=30)
        form_inner.pack(fill=tk.BOTH, expand=True)
        
        # Username field with Facebook styling
        username_label = ttk.Label(form_inner, text="Username", style="Field.TLabel")
        username_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Appropriately sized username entry
        self.username_entry = tk.Entry(form_inner, 
                                       font=("Segoe UI", 12),
                                       bg="#ffffff",
                                       fg="#1c1e21",
                                       insertbackground="#1877f2",
                                       relief="solid",
                                       bd=2,
                                       highlightthickness=2,
                                       highlightbackground="#1877f2",
                                       highlightcolor="#1877f2",
                                       width=25)
        self.username_entry.pack(pady=(0, 20), ipady=8)
        
        # Password field with Facebook styling
        password_label = ttk.Label(form_inner, text="Password", style="Field.TLabel")
        password_label.pack(anchor=tk.W, pady=(0, 8))
        
        # Appropriately sized password entry
        self.password_entry = tk.Entry(form_inner, 
                                       font=("Segoe UI", 12),
                                       bg="#ffffff",
                                       fg="#1c1e21",
                                       insertbackground="#1877f2",
                                       show="●",
                                       relief="solid",
                                       bd=2,
                                       highlightthickness=2,
                                       highlightbackground="#1877f2",
                                       highlightcolor="#1877f2",
                                       width=25)
        self.password_entry.pack(pady=(0, 25), ipady=8)
        
        # Main login button with improved design
        self.login_button = tk.Button(form_inner,
                                       text="🔐 LOG IN",
                                       font=("Segoe UI", 14, "bold"),
                                       bg="#1877f2",
                                       fg="#ffffff",
                                       relief="flat",
                                       bd=0,
                                       cursor="hand2",
                                       activebackground="#166fe5",
                                       activeforeground="#ffffff",
                                       command=self.login,
                                       width=25,
                                       height=2)
        self.login_button.pack(pady=(20, 15), ipady=10)
        
        # Secondary buttons frame
        secondary_frame = tk.Frame(form_inner, bg="#ffffff")
        secondary_frame.pack(fill=tk.X, pady=(10, 15))
        
        # Show/Hide password button
        self.show_password_btn = tk.Button(secondary_frame,
                                          text="👁️ Show Password",
                                          font=("Segoe UI", 10),
                                          bg="#f0f2f5",
                                          fg="#1c1e21",
                                          relief="flat",
                                          cursor="hand2",
                                          width=15,
                                          command=self.toggle_password)
        self.show_password_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear fields button
        clear_btn = tk.Button(secondary_frame,
                             text="🗑️ Clear Fields",
                             font=("Segoe UI", 10),
                             bg="#f0f2f5",
                             fg="#1c1e21",
                             relief="flat",
                             cursor="hand2",
                             width=15,
                             command=self.clear_fields)
        clear_btn.pack(side=tk.LEFT)
        
        # Help/Info section
        help_frame = tk.Frame(form_inner, bg="#f8f9fa", relief="solid", bd=1)
        help_frame.pack(fill=tk.X, pady=(15, 0))
        
        help_title = tk.Label(help_frame,
                             text="💡 Quick Help",
                             font=("Segoe UI", 11, "bold"),
                             bg="#f8f9fa",
                             fg="#1877f2")
        help_title.pack(pady=(10, 5))
        
        help_text = tk.Label(help_frame,
                            text="• Press Enter key to login quickly\n• Use Tab to navigate between fields\n• Click 'Show Password' to verify your input",
                            font=("Segoe UI", 9),
                            bg="#f8f9fa",
                            fg="#65676b",
                            justify=tk.LEFT)
        help_text.pack(pady=(0, 10))
        
        # Status label with Facebook styling
        self.status_label = tk.Label(form_inner,
                                      text="",
                                      font=("Segoe UI", 11),
                                      fg="#1877f2",
                                      bg="#ffffff")
        self.status_label.pack()
        

        
        # Demo credentials section with better design
        demo_frame = tk.Frame(main_container, bg="#e3f2fd", relief="solid", bd=1)
        demo_frame.pack(fill=tk.X, pady=(20, 15))
        
        demo_title = tk.Label(demo_frame,
                             text="🔑 Demo Credentials",
                             font=("Segoe UI", 11, "bold"),
                             fg="#1565c0",
                             bg="#e3f2fd")
        demo_title.pack(pady=(10, 5))
        
        demo_info = tk.Label(demo_frame,
                            text="Username: guidance1\nPassword: guidance123",
                            font=("Segoe UI", 10),
                            fg="#1976d2",
                            bg="#e3f2fd",
                            justify=tk.CENTER)
        demo_info.pack(pady=(0, 5))
        
        # Quick fill button
        quick_fill_btn = tk.Button(demo_frame,
                                  text="⚡ Quick Fill Demo",
                                  font=("Segoe UI", 9, "bold"),
                                  bg="#2196f3",
                                  fg="#ffffff",
                                  relief="flat",
                                  cursor="hand2",
                                  width=15,
                                  command=self.quick_fill_demo)
        quick_fill_btn.pack(pady=(0, 10))
        
        # Footer with better styling
        footer_frame = tk.Frame(main_container, bg="#ffffff")
        footer_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Copyright
        copyright_label = tk.Label(footer_frame,
                                   text="© 2024 AI Uniform System - Guidance Portal",
                                   font=("Segoe UI", 9),
                                   fg="#65676b",
                                   bg="#ffffff")
        copyright_label.pack()
    

    
    def load_sample_users(self):
        """Load sample guidance users from Firebase or create default ones"""
        try:
            # Try to get users from Firebase (ensure 'username' exists)
            firebase_users = get_from_firebase('users', 200)
            loaded = 0
            if firebase_users:
                self.users = {}
                for user in firebase_users:
                    if user.get('role') == 'Guidance Counselor' and user.get('username'):
                        username = user['username']
                        self.users[username] = {
                            'username': username,
                            'password_hash': user.get('password_hash', ''),
                            'full_name': user.get('full_name', ''),
                            'role': user.get('role', 'Guidance Counselor'),
                            'status': user.get('status', 'ACTIVE'),
                            'firebase_id': user.get('id')
                        }
                        loaded += 1
                print(f"✅ Loaded {loaded} users from Firebase")
            # Seed defaults if none found
            if not firebase_users or loaded == 0:
                self.create_default_users()
        except Exception as e:
            print(f"⚠️ Firebase connection failed, using local users: {e}")
            self.create_default_users()
    
    def create_default_users(self):
        """Create default guidance users (upsert into Firebase with username)"""
        # Generate proper password hashes
        password = "guidance123"
        password_hash = self.hash_password(password)
        
        self.users = {
            'guidance1': {
                'username': 'guidance1',
                'password_hash': password_hash,
                'full_name': 'Mrs. Sarah Johnson',
                'role': 'Guidance Counselor',
                'status': 'ACTIVE'
            },
            'guidance2': {
                'username': 'guidance2',
                'password_hash': password_hash,
                'full_name': 'Ms. Emily Chen',
                'role': 'Guidance Counselor',
                'status': 'ACTIVE'
            }
        }
        
        # Try to upsert to Firebase (avoid duplicates by username)
        try:
            for username, user_data in self.users.items():
                existing = search_in_firebase('users', 'username', username)
                if existing and len(existing) > 0:
                    # Already exists; keep the firebase id and do not re-add
                    self.users[username]['firebase_id'] = existing[0].get('id')
                    continue
                doc_id = add_to_firebase('users', user_data)
                if doc_id:
                    self.users[username]['firebase_id'] = doc_id
                    print(f"✅ User {username} saved to Firebase with ID: {doc_id}")
        except Exception as e:
            print(f"⚠️ Failed to save users to Firebase: {e}")
        
        print(f"✅ Created/loaded {len(self.users)} default users")
        print(f"Users available: {list(self.users.keys())}")
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        """Handle login authentication"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Debug information
        print(f"Login attempt - Username: {username}, Password: {password}")
        
        # Clear previous status
        self.status_label.config(text="")
        
        # Validation
        if not username or not password:
            self.status_label.config(text="⚠️ Please enter both username and password", fg="#e41e3f")
            print("Validation failed: Empty fields")
            return
        
        # If not present locally, try to fetch from Firebase by username
        if (not hasattr(self, 'users')):
            self.users = {}
        if username not in self.users:
            try:
                remote = search_in_firebase('users', 'username', username)
                if remote:
                    user = remote[0]
                    self.users[username] = {
                        'username': username,
                        'password_hash': user.get('password_hash', ''),
                        'full_name': user.get('full_name', ''),
                        'role': user.get('role', 'Guidance Counselor'),
                        'status': user.get('status', 'ACTIVE'),
                        'firebase_id': user.get('id')
                    }
                    print(f"✅ User {username} loaded from Firebase on-demand")
            except Exception as e:
                print(f"⚠️ On-demand user fetch failed: {e}")
        
        # Check if user exists
        if username not in self.users:
            self.status_label.config(text="❌ Invalid username or password", fg="#e41e3f")
            print(f"User not found: {username}")
            print(f"Available users: {list(self.users.keys())}")
            return
        
        user_data = self.users[username]
        print(f"User found: {user_data}")
        
        # Check password
        input_hash = self.hash_password(password)
        stored_hash = user_data['password_hash']
        print(f"Input password hash: {input_hash}")
        print(f"Stored password hash: {stored_hash}")
        print(f"Hash match: {input_hash == stored_hash}")
        
        if input_hash != stored_hash:
            self.status_label.config(text="❌ Invalid username or password", fg="#e41e3f")
            print("Password hash mismatch")
            return
        
        # Check if account is active
        if user_data['status'] != "ACTIVE":
            self.status_label.config(text="🚫 Account is deactivated. Please contact administrator.", fg="#e41e3f")
            print("Account deactivated")
            return
        
        # Login successful
        print("Login successful!")
        self.show_success_message(user_data)
    
    def show_success_message(self, user_data):
        """Show success message and prepare for dashboard"""
        # Disable login button temporarily
        self.login_button.config(state="disabled")
        
        # Show success message with Facebook styling
        self.status_label.config(text="✅ Login successful! Opening dashboard...", fg="#42b883")
        
        # Simulate loading
        self.root.after(2000, lambda: self.open_dashboard(user_data))
    
    def open_dashboard(self, user_data):
        """Open the guidance dashboard"""
        try:
            # Import and create dashboard
            from guidance_dashboard import GuidanceDashboard
            
            # Hide login window
            self.root.withdraw()
            
            # Create dashboard, pass the login root as parent to use Toplevel
            dashboard = GuidanceDashboard(user_data, parent=self.root)
            
            # Set up dashboard closure handling
            def on_dashboard_closed():
                # Check if login window still exists before trying to show it
                try:
                    if self.root.winfo_exists():
                        # Show login window again when dashboard closes
                        self.root.deiconify()
                        # Reset form
                        self.username_entry.delete(0, tk.END)
                        self.password_entry.delete(0, tk.END)
                        self.status_label.config(text="", fg="#1877f2")
                        self.login_button.config(state="normal")
                        self.username_entry.focus()
                    else:
                        # Login window was destroyed, restart the app
                        self.restart_app()
                except tk.TclError:
                    # Login window was destroyed, restart the app
                    self.restart_app()
            
            # Override the dashboard's logout method to call our callback
            original_logout = dashboard.logout
            def logout_with_callback():
                if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
                    dashboard.root.destroy()
                    on_dashboard_closed()
            
            dashboard.logout = logout_with_callback
            
            # Bind dashboard window close event
            dashboard.root.protocol("WM_DELETE_WINDOW", on_dashboard_closed)
            
            # Run dashboard (waits until it is closed)
            dashboard.run()
            
            # When dashboard.run() returns, show login again if window still exists
            try:
                on_dashboard_closed()
            except tk.TclError:
                pass
            
        except ImportError:
            messagebox.showerror("Error", "Dashboard module not found. Please ensure guidance_dashboard.py is in the same directory.")
            self.root.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open dashboard: {str(e)}")
            self.root.deiconify()
    
    def restart_app(self):
        """Restart the application if the main window was destroyed"""
        try:
            # Create a new login window
            new_app = ModernGuidanceLogin()
            new_app.run()
        except Exception as e:
            print(f"Failed to restart app: {e}")
            # Fallback: just exit
            import sys
            sys.exit(1)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

    def toggle_password(self):
        """Toggle password visibility"""
        if self.password_entry.cget('show') == '●':
            self.password_entry.config(show='')
            self.show_password_btn.config(text="🙈 Hide Password")
        else:
            self.password_entry.config(show='●')
            self.show_password_btn.config(text="👁️ Show Password")
    
    def clear_fields(self):
        """Clear all input fields"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.status_label.config(text="")
        self.username_entry.focus()
    
    def quick_fill_demo(self):
        """Quick fill demo credentials"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.insert(0, "guidance1")
        self.password_entry.insert(0, "guidance123")
        self.status_label.config(text="✅ Demo credentials filled!", fg="#28a745")
        self.login_button.focus()

if __name__ == "__main__":
    app = ModernGuidanceLogin()
    app.run()
