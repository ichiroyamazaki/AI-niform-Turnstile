import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime
import logging
from typing import Dict, List
from firebase_config import (
    add_to_firebase, 
    get_from_firebase, 
    update_in_firebase, 
    delete_from_firebase, 
    search_in_firebase,
    upload_to_storage,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GuidanceDashboard:
    def __init__(self, user_data, parent=None):
        self.user_data = user_data
        self.parent = parent
        # Use Toplevel when parent is provided to avoid multiple Tk roots
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title(f"AI Uniform System - Guidance Dashboard - {user_data['full_name']}")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f8f9fa")
        
        # Initialize data storage
        self.violations = []
        self.appeals = []
        self.uniform_designs = []
        
        # Load sample data
        self.load_sample_data()
        
        # Create main interface
        self.create_interface()
        
        # Center window
        self.center_window()
        
        # Bind escape key to close window only
        self.root.bind('<Escape>', lambda event: self.root.destroy())
    
    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def load_sample_data(self):
        """Load sample data from Firebase or create default ones"""
        try:
            # Try to load violations from Firebase
            firebase_violations = get_from_firebase('violations')
            if firebase_violations:
                self.violations = firebase_violations
                print(f"✅ Loaded {len(self.violations)} violations from Firebase")
            else:
                self.create_sample_violations()
            
            # Try to load appeals from Firebase
            firebase_appeals = get_from_firebase('appeals')
            if firebase_appeals:
                self.appeals = firebase_appeals
                print(f"✅ Loaded {len(self.appeals)} appeals from Firebase")
            else:
                self.create_sample_appeals()
            
            # Try to load uniform designs from Firebase
            firebase_designs = get_from_firebase('uniform_designs')
            if firebase_designs:
                self.uniform_designs = firebase_designs
                print(f"✅ Loaded {len(self.uniform_designs)} uniform designs from Firebase")
            else:
                self.create_sample_designs()
                
        except Exception as e:
            print(f"⚠️ Firebase connection failed, using local data: {e}")
            self.create_sample_violations()
            self.create_sample_appeals()
            self.create_sample_designs()
    
    def create_sample_violations(self):
        """Create sample violations and save to Firebase"""
        sample_violations = [
            {
                'student_name': 'John Smith',
                'student_id': '2024-001',
                'violation_type': 'Improper Uniform',
                'date': '2024-01-15',
                'description': 'Wearing non-regulation shoes',
                'status': 'Pending',
                'reported_by': 'Security Guard'
            },
            {
                'student_name': 'Maria Garcia',
                'student_id': '2024-002',
                'violation_type': 'Missing ID',
                'date': '2024-01-16',
                'description': 'Student not wearing ID badge',
                'status': 'Resolved',
                'reported_by': 'Teacher'
            }
        ]
        
        self.violations = []
        for violation in sample_violations:
            try:
                doc_id = add_to_firebase('violations', violation)
                if doc_id:
                    violation['id'] = doc_id
                    self.violations.append(violation)
                    print(f"✅ Violation saved to Firebase with ID: {doc_id}")
            except Exception as e:
                print(f"⚠️ Failed to save violation to Firebase: {e}")
                # Add local ID if Firebase fails
                violation['id'] = f"V{len(self.violations)+1:03d}"
                self.violations.append(violation)
    
    def create_sample_appeals(self):
        """Create sample appeals and save to Firebase"""
        sample_appeals = [
            {
                'student_name': 'John Smith',
                'student_id': '2024-001',
                'violation_id': 'V001',
                'appeal_date': '2024-01-17',
                'reason': 'Shoes were temporarily borrowed due to emergency',
                'status': 'Pending Review',
                'submitted_by': 'Parent',
                'priority': 'Medium',
                'evidence_documents': [],
                'notes': 'Student claims shoes were borrowed due to emergency situation',
                'assigned_to': '',
                'review_date': '',
                'decision_reason': '',
                'appeal_type': 'Uniform Violation'
            },
            {
                'student_name': 'Maria Garcia',
                'student_id': '2024-002',
                'violation_id': 'V002',
                'appeal_date': '2024-01-18',
                'reason': 'Medical condition requiring special footwear',
                'status': 'Under Investigation',
                'submitted_by': 'Student',
                'priority': 'High',
                'evidence_documents': ['medical_certificate.pdf'],
                'notes': 'Student provided medical documentation',
                'assigned_to': 'Dr. Johnson',
                'review_date': '2024-01-20',
                'decision_reason': '',
                'appeal_type': 'Medical Exemption'
            },
            {
                'student_name': 'David Wilson',
                'student_id': '2024-003',
                'violation_id': 'V003',
                'appeal_date': '2024-01-19',
                'reason': 'Financial hardship affecting uniform purchase',
                'status': 'Pending Review',
                'submitted_by': 'Parent',
                'priority': 'High',
                'evidence_documents': ['financial_statement.pdf'],
                'notes': 'Family experiencing financial difficulties',
                'assigned_to': '',
                'review_date': '',
                'decision_reason': '',
                'appeal_type': 'Financial Hardship'
            }
        ]
        
        self.appeals = []
        for appeal in sample_appeals:
            try:
                doc_id = add_to_firebase('appeals', appeal)
                if doc_id:
                    appeal['id'] = doc_id
                    self.appeals.append(appeal)
                    print(f"✅ Appeal saved to Firebase with ID: {doc_id}")
            except Exception as e:
                print(f"⚠️ Failed to save appeal to Firebase: {e}")
                # Add local ID if Firebase fails
                appeal['id'] = f"A{len(self.appeals)+1:03d}"
                self.appeals.append(appeal)
    
    def create_sample_designs(self):
        """Create sample uniform designs and save to Firebase"""
        sample_designs = [
            {
                'name': 'Summer Uniform 2024',
                'course': 'Computer Science',
                'type': 'Polo Shirt',
                'colors': 'Blue and White',
                'submitted_date': '2024-01-10',
                'status': 'Under Review',
                'designer': 'Fashion Committee'
            },
            {
                'name': 'Engineering Lab Uniform',
                'course': 'Engineering',
                'type': 'Lab Coat',
                'colors': 'White',
                'submitted_date': '2024-01-12',
                'status': 'Approved',
                'designer': 'Engineering Department'
            },
            {
                'name': 'Business Professional Attire',
                'course': 'Business Administration',
                'type': 'Blouse',
                'colors': 'Navy Blue and White',
                'submitted_date': '2024-01-15',
                'status': 'Under Review',
                'designer': 'Business Faculty'
            }
        ]
        
        self.uniform_designs = []
        for design in sample_designs:
            try:
                doc_id = add_to_firebase('uniform_designs', design)
                if doc_id:
                    design['id'] = doc_id
                    self.uniform_designs.append(design)
                    print(f"✅ Uniform design saved to Firebase with ID: {doc_id}")
            except Exception as e:
                print(f"⚠️ Failed to save uniform design to Firebase: {e}")
                # Add local ID if Firebase fails
                design['id'] = f"UD{len(self.uniform_designs)+1:03d}"
                self.uniform_designs.append(design)
    
    def create_interface(self):
        """Create the main dashboard interface"""
        # Header
        self.create_header()
        
        # Main content with tabs
        self.create_tabs()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Create the dashboard header"""
        header_frame = tk.Frame(self.root, bg="#1877f2", height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Left side - Welcome and user info
        left_frame = tk.Frame(header_frame, bg="#1877f2")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)
        
        # Welcome message
        welcome_label = tk.Label(left_frame,
                                text=f"👋 Welcome, {self.user_data['full_name']}",
                                font=("Segoe UI", 18, "bold"),
                                fg="#ffffff",
                                bg="#1877f2")
        welcome_label.pack(anchor=tk.W)
        
        # Role and status
        role_label = tk.Label(left_frame,
                             text=f"👤 Role: {self.user_data['role']} | 📊 Status: {self.user_data['status']}",
                             font=("Segoe UI", 11),
                             fg="#ffffff",
                             bg="#1877f2")
        role_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Right side - Date and logout
        right_frame = tk.Frame(header_frame, bg="#1877f2")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)
        
        # Current date
        current_date = datetime.now().strftime("%B %d, %Y")
        date_label = tk.Label(right_frame,
                             text=f"📅 {current_date}",
                             font=("Segoe UI", 11),
                             fg="#ffffff",
                             bg="#1877f2")
        date_label.pack(anchor=tk.E, pady=(0, 8))
        
        # Logout button with better visibility
        logout_btn = tk.Button(right_frame,
                              text="🚪 Logout",
                              font=("Segoe UI", 13, "bold"),
                              bg="#ffffff",
                              fg="#1877f2",
                              relief="solid",
                              bd=1,
                              cursor="hand2",
                              width=15,
                              height=2,
                              command=self.logout)
        logout_btn.pack(anchor=tk.E, pady=(8, 0))
    
    def create_tabs(self):
        """Create the main tabbed interface"""
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#f8f9fa")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create individual tabs
        self.create_violations_tab()
        self.create_appeals_tab()
        self.create_uniform_designs_tab()
    
    def create_violations_tab(self):
        """Create the violations management tab"""
        violations_frame = ttk.Frame(self.notebook)
        self.notebook.add(violations_frame, text="Violations")
        
        # Tab header
        header_label = tk.Label(violations_frame,
                               text="Uniform Violations Management",
                               font=("Segoe UI", 16, "bold"),
                               bg="#f8f9fa")
        header_label.pack(pady=(20, 30))
        
        # Main controls frame
        controls_frame = tk.Frame(violations_frame, bg="#f8f9fa")
        controls_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Left side - Action buttons
        action_frame = tk.Frame(controls_frame, bg="#f8f9fa")
        action_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Add violation button
        add_btn = tk.Button(action_frame,
                           text="➕ Add New Violation",
                           font=("Segoe UI", 11, "bold"),
                           bg="#28a745",
                           fg="#ffffff",
                           relief="flat",
                           cursor="hand2",
                           width=18,
                           command=self.add_violation)
        add_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Right side - Search controls
        search_frame = tk.Frame(controls_frame, bg="#f8f9fa")
        search_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Search label and entry
        search_label = tk.Label(search_frame, text="🔍 Search:", font=("Segoe UI", 10, "bold"), bg="#f8f9fa")
        search_label.pack(side=tk.LEFT, padx=(0, 8))
        
        self.violation_search = tk.Entry(search_frame, width=20, font=("Segoe UI", 10))
        self.violation_search.pack(side=tk.LEFT, padx=(0, 8))
        
        # Search button
        search_btn = tk.Button(search_frame,
                              text="Search",
                              font=("Segoe UI", 10, "bold"),
                              bg="#007bff",
                              fg="#ffffff",
                              relief="flat",
                              cursor="hand2",
                              width=10,
                              command=self.search_violations)
        search_btn.pack(side=tk.LEFT)
        
        # Violations table
        self.create_violations_table(violations_frame)
    
    def create_violations_table(self, parent):
        """Create the violations data table"""
        # Table frame
        table_frame = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create Treeview
        columns = ('ID', 'Student Name', 'Student ID', 'Violation Type', 'Date', 'Status', 'Reported By')
        self.violations_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            self.violations_tree.heading(col, text=col)
            self.violations_tree.column(col, width=120, minwidth=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.violations_tree.yview)
        self.violations_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar
        self.violations_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double-click event
        self.violations_tree.bind('<Double-1>', self.edit_violation)
        
        # Load violations data
        self.load_violations_data()
    
    def create_appeals_tab(self):
        """Create the appeals management tab with enhanced functionality"""
        appeals_frame = ttk.Frame(self.notebook)
        self.notebook.add(appeals_frame, text="Appeals")
        
        # Clean, minimalist header
        header_frame = tk.Frame(appeals_frame, bg="#ffffff")
        header_frame.pack(fill=tk.X, pady=(25, 20))
        
        # Centered title with subtle styling
        title_frame = tk.Frame(header_frame, bg="#ffffff")
        title_frame.pack(expand=True)
        
        header_label = tk.Label(title_frame,
                               text="Appeals Management",
                               font=("Segoe UI", 18, "bold"),
                               bg="#ffffff",
                               fg="#2c3e50")
        header_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(title_frame,
                                 text="Process student appeals efficiently",
                                 font=("Segoe UI", 10),
                                 bg="#ffffff",
                                 fg="#7f8c8d")
        subtitle_label.pack(pady=(5, 0))
        
        # Primary action buttons - organized in a clean grid
        primary_actions_frame = tk.Frame(appeals_frame, bg="#ffffff")
        primary_actions_frame.pack(fill=tk.X, padx=40, pady=(0, 25))
        
        # Row 1: Main actions
        row1_frame = tk.Frame(primary_actions_frame, bg="#ffffff")
        row1_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Quick Process button (primary action)
        quick_process_btn = tk.Button(row1_frame,
                                     text="⚡ Quick Process Appeals",
                                     font=("Segoe UI", 12, "bold"),
                                     bg="#3498db",
                                     fg="#ffffff",
                                     relief="flat",
                                     cursor="hand2",
                                     width=20,
                                     height=2,
                                     command=self.quick_process_appeals)
        quick_process_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Add New Appeal button
        add_appeal_btn = tk.Button(row1_frame,
                                  text="➕ Add New Appeal",
                                  font=("Segoe UI", 12, "bold"),
                                  bg="#27ae60",
                                  fg="#ffffff",
                                  relief="flat",
                                  cursor="hand2",
                                  width=18,
                                  height=2,
                                  command=self.add_new_appeal)
        add_appeal_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Bulk Actions button
        bulk_actions_btn = tk.Button(row1_frame,
                                    text="📋 Bulk Actions",
                                    font=("Segoe UI", 12, "bold"),
                                    bg="#f39c12",
                                    fg="#ffffff",
                                    relief="flat",
                                    cursor="hand2",
                                    width=16,
                                    height=2,
                                    command=self.process_appeals)
        bulk_actions_btn.pack(side=tk.LEFT)
        
        # Row 2: Secondary actions
        row2_frame = tk.Frame(primary_actions_frame, bg="#ffffff")
        row2_frame.pack(fill=tk.X)
        
        # Process Appeals button
        process_btn = tk.Button(row2_frame,
                               text="⚙️ Process Individual",
                               font=("Segoe UI", 11),
                               bg="#95a5a6",
                               fg="#ffffff",
                               relief="flat",
                               cursor="hand2",
                               width=18,
                               command=self.process_appeals)
        process_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Appeal Statistics button
        stats_btn = tk.Button(row2_frame,
                             text="📊 View Statistics",
                             font=("Segoe UI", 11),
                             bg="#9b59b6",
                             fg="#ffffff",
                             relief="flat",
                             cursor="hand2",
                             width=18,
                             command=self.show_appeal_statistics)
        stats_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Export Appeals button
        export_btn = tk.Button(row2_frame,
                              text="📤 Export Data",
                              font=("Segoe UI", 11),
                              bg="#e74c3c",
                              fg="#ffffff",
                              relief="flat",
                              cursor="hand2",
                              width=16,
                              command=self.export_appeals)
        export_btn.pack(side=tk.LEFT)
        
        # Filter controls frame
        controls_frame = tk.Frame(appeals_frame, bg="#f8f9fa")
        controls_frame.pack(fill=tk.X, padx=40, pady=(0, 20))
        
        # Right side - Filter controls
        filter_frame = tk.Frame(controls_frame, bg="#f8f9fa")
        filter_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status filter label
        tk.Label(filter_frame, text="🔍 Status Filter:", font=("Segoe UI", 10, "bold"), 
                bg="#f8f9fa").pack(side=tk.LEFT, padx=(0, 8))
        
        # Status filter dropdown
        self.appeal_status_filter = tk.StringVar(value="All Statuses")
        status_filter_combo = ttk.Combobox(filter_frame, textvariable=self.appeal_status_filter, 
                                          values=["All Statuses", "Pending Review", "Under Investigation", "Approved", "Rejected", "Closed"],
                                          width=15, font=("Segoe UI", 10))
        status_filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Apply filter button
        apply_filter_btn = tk.Button(filter_frame,
                                    text="Apply",
                                    font=("Segoe UI", 10, "bold"),
                                    bg="#007bff",
                                    fg="#ffffff",
                                    relief="flat",
                                    cursor="hand2",
                                    width=8,
                                    command=self.apply_appeal_filter)
        apply_filter_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # Clear filter button
        clear_filter_btn = tk.Button(filter_frame,
                                    text="Clear",
                                    font=("Segoe UI", 10, "bold"),
                                    bg="#6c757d",
                                    fg="#ffffff",
                                    relief="flat",
                                    cursor="hand2",
                                    width=8,
                                    command=self.clear_appeal_filter)
        clear_filter_btn.pack(side=tk.LEFT)
        
        # Help and guidance frame (minimalist style)
        help_frame = tk.Frame(appeals_frame, bg="#f8f9fa", relief="flat", bd=0)
        help_frame.pack(fill=tk.X, padx=40, pady=(0, 25))
        
        # Help title
        help_title = tk.Label(help_frame, text="💡 Quick Actions Guide", 
                             font=("Segoe UI", 11, "bold"), bg="#f8f9fa", fg="#2c3e50")
        help_title.pack(pady=(8, 5))
        
        # Help text (cleaner format)
        help_text = """⚡ Quick Process for fast decisions • Right-click for context menu • Double-click to view details • 
        Enter key for quick process • Status colors: Yellow=Pending, Blue=Investigating, Green=Approved, Red=Rejected"""
        
        help_label = tk.Label(help_frame, text=help_text, font=("Segoe UI", 9), 
                             bg="#f8f9fa", fg="#7f8c8d", wraplength=800, justify=tk.LEFT)
        help_label.pack(pady=(0, 8))
        
        # Appeal statistics frame (minimalist style)
        stats_frame = tk.Frame(appeals_frame, bg="#ffffff", relief="flat", bd=0)
        stats_frame.pack(fill=tk.X, padx=40, pady=(0, 25))
        
        # Statistics title
        tk.Label(stats_frame, text="📊 Appeal Statistics", font=("Segoe UI", 11, "bold"), 
                bg="#ffffff", fg="#2c3e50").pack(pady=(8, 5))
        
        # Create appeal statistics display
        self.create_appeal_statistics_display(stats_frame)
        
        # Appeals table
        self.create_appeals_table(appeals_frame)
    
    def create_appeals_table(self, parent):
        """Create the appeals data table"""
        # Table frame (minimalist style)
        table_frame = tk.Frame(parent, bg="#ffffff", relief="flat", bd=0)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=(0, 25))
        
        # Create Treeview with enhanced columns
        columns = ('ID', 'Student Name', 'Student ID', 'Violation ID', 'Appeal Date', 'Status', 'Submitted By', 'Priority', 'Days Pending')
        self.appeals_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define headings and column widths
        column_widths = {
            'ID': 80,
            'Student Name': 150,
            'Student ID': 100,
            'Violation ID': 100,
            'Appeal Date': 120,
            'Status': 140,
            'Submitted By': 120,
            'Priority': 80,
            'Days Pending': 100
        }
        
        for col in columns:
            self.appeals_tree.heading(col, text=col)
            self.appeals_tree.column(col, width=column_widths.get(col, 120), minwidth=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.appeals_tree.yview)
        self.appeals_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar
        self.appeals_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.appeals_tree.bind('<Double-1>', self.view_appeal_details)
        self.appeals_tree.bind('<Button-3>', self.show_appeal_context_menu)  # Right-click context menu
        self.appeals_tree.bind('<Return>', self.quick_process_selected_appeal)  # Enter key for quick process
        
        # Load appeals data
        self.load_appeals_data()
    
    def create_uniform_designs_tab(self):
        """Create the uniform designs management tab"""
        designs_frame = ttk.Frame(self.notebook)
        self.notebook.add(designs_frame, text="Uniform Designs")
        
        # Clean, minimalist header
        header_frame = tk.Frame(designs_frame, bg="#ffffff")
        header_frame.pack(fill=tk.X, pady=(25, 20))
        
        # Centered title with subtle styling
        title_frame = tk.Frame(header_frame, bg="#ffffff")
        title_frame.pack(expand=True)
        
        header_label = tk.Label(title_frame,
                               text="Uniform Design Management",
                               font=("Segoe UI", 18, "bold"),
                               bg="#ffffff",
                               fg="#2c3e50")
        header_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(title_frame,
                                 text="Manage and organize uniform designs by course",
                                 font=("Segoe UI", 10),
                                 bg="#ffffff",
                                 fg="#7f8c8d")
        subtitle_label.pack(pady=(5, 0))
        
        # Quick access buttons (minimalist style)
        quick_access_frame = tk.Frame(header_frame, bg="#ffffff")
        quick_access_frame.pack(side=tk.RIGHT, pady=10)
        
        # Course Management quick access
        course_mgmt_quick_btn = tk.Button(quick_access_frame,
                                         text="🎓 Course Files",
                                         font=("Segoe UI", 11, "bold"),
                                         bg="#9b59b6",
                                         fg="#ffffff",
                                         relief="flat",
                                         cursor="hand2",
                                         width=16,
                                         height=2,
                                         command=self.manage_course_files)
        course_mgmt_quick_btn.pack(side=tk.RIGHT, padx=(0, 15))
        
        # Export quick access
        export_quick_btn = tk.Button(quick_access_frame,
                                    text="📤 Export All",
                                    font=("Segoe UI", 11, "bold"),
                                    bg="#e74c3c",
                                    fg="#ffffff",
                                    relief="flat",
                                    cursor="hand2",
                                    width=14,
                                    height=2,
                                    command=self.export_designs_by_course)
        export_quick_btn.pack(side=tk.RIGHT)
        
        # Main controls frame
        controls_frame = tk.Frame(designs_frame, bg="#f8f9fa")
        controls_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Course statistics frame (minimalist style)
        stats_frame = tk.Frame(designs_frame, bg="#f8f9fa", relief="flat", bd=0)
        stats_frame.pack(fill=tk.X, padx=40, pady=(0, 25))
        
        # Statistics title
        tk.Label(stats_frame, text="📊 Course Statistics", font=("Segoe UI", 11, "bold"), 
                bg="#f8f9fa", fg="#2c3e50").pack(pady=(8, 5))
        
        # Create statistics display
        self.create_course_statistics(stats_frame)
        
        # Clean, organized button layout
        # Primary actions row
        primary_actions_frame = tk.Frame(controls_frame, bg="#f8f9fa")
        primary_actions_frame.pack(side=tk.LEFT, fill=tk.Y, pady=(0, 10))
        
        # Add design button (primary action)
        add_design_btn = tk.Button(primary_actions_frame,
                                  text="➕ Add New Design",
                                  font=("Segoe UI", 12, "bold"),
                                  bg="#27ae60",
                                  fg="#ffffff",
                                  relief="flat",
                                  cursor="hand2",
                                  width=20,
                                  height=2,
                                  command=self.add_uniform_design)
        add_design_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Browse designs button
        browse_btn = tk.Button(primary_actions_frame,
                              text="🔍 Browse Designs",
                              font=("Segoe UI", 12, "bold"),
                              bg="#3498db",
                              fg="#ffffff",
                              relief="flat",
                              cursor="hand2",
                              width=18,
                              height=2,
                              command=self.browse_designs)
        browse_btn.pack(side=tk.LEFT, padx=(0, 20))
        
        # Course Management button
        course_mgmt_btn = tk.Button(primary_actions_frame,
                                   text="🎓 Course Management",
                                   font=("Segoe UI", 12, "bold"),
                                   bg="#9b59b6",
                                   fg="#ffffff",
                                   relief="flat",
                                   cursor="hand2",
                                   width=20,
                                   height=2,
                                   command=self.manage_course_files)
        course_mgmt_btn.pack(side=tk.LEFT)
        
        # Secondary actions row
        secondary_actions_frame = tk.Frame(controls_frame, bg="#f8f9fa")
        secondary_actions_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(40, 0))
        
        # Refresh button
        refresh_btn = tk.Button(secondary_actions_frame,
                               text="🔄 Refresh",
                               font=("Segoe UI", 11),
                               bg="#95a5a6",
                               fg="#ffffff",
                               relief="flat",
                               cursor="hand2",
                               width=12,
                               command=self.refresh_designs_data)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Export button
        export_btn = tk.Button(secondary_actions_frame,
                              text="📤 Export by Course",
                              font=("Segoe UI", 11),
                              bg="#e74c3c",
                              fg="#ffffff",
                              relief="flat",
                              cursor="hand2",
                              width=16,
                              command=self.export_designs_by_course)
        export_btn.pack(side=tk.LEFT)
        
        # Center - Course filter controls (cleaner layout)
        filter_frame = tk.Frame(controls_frame, bg="#f8f9fa")
        filter_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(60, 0))
        
        # Course filter label
        tk.Label(filter_frame, text="🎓 Course Filter:", font=("Segoe UI", 10, "bold"), 
                bg="#f8f9fa").pack(side=tk.LEFT, padx=(0, 8))
        
        # Course filter dropdown
        self.course_filter_var = tk.StringVar(value="All Courses")
        self.course_filter_combo = ttk.Combobox(filter_frame, textvariable=self.course_filter_var, 
                                               font=("Segoe UI", 10), width=15)
        self.course_filter_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Apply filter button
        apply_filter_btn = tk.Button(filter_frame,
                                    text="Apply",
                                    font=("Segoe UI", 10, "bold"),
                                    bg="#007bff",
                                    fg="#ffffff",
                                    relief="flat",
                                    cursor="hand2",
                                    width=8,
                                    command=self.apply_course_filter)
        apply_filter_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        # Clear filter button
        clear_filter_btn = tk.Button(filter_frame,
                                    text="Clear",
                                    font=("Segoe UI", 10, "bold"),
                                    bg="#6c757d",
                                    fg="#ffffff",
                                    relief="flat",
                                    cursor="hand2",
                                    width=8,
                                    command=self.clear_course_filter)
        clear_filter_btn.pack(side=tk.LEFT)
        
        # Right side - Table action buttons (cleaned up)
        table_action_frame = tk.Frame(controls_frame, bg="#f8f9fa")
        table_action_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Edit button
        edit_btn = tk.Button(table_action_frame,
                            text="🖊️ Edit Selected",
                            font=("Segoe UI", 11, "bold"),
                            bg="#ffc107",
                            fg="#000000",
                            relief="flat",
                            cursor="hand2",
                            width=18,
                            command=lambda: self.edit_design(None))
        edit_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Delete button
        delete_btn = tk.Button(table_action_frame,
                              text="🗑️ Delete Selected",
                              font=("Segoe UI", 11, "bold"),
                              bg="#dc3545",
                              fg="#ffffff",
                              relief="flat",
                              cursor="hand2",
                              width=18,
                              command=lambda: self.delete_design(None))
        delete_btn.pack(side=tk.LEFT)
        
        # Help text for shortcuts
        help_frame = tk.Frame(designs_frame, bg="#e9ecef", relief="solid", bd=1)
        help_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        help_text = tk.Label(help_frame, 
                           text="💡 Quick Actions: Double-click to edit • Right-click for context menu • F2 to edit • Delete key to delete • Select multiple with Ctrl+Click",
                           font=("Segoe UI", 9), bg="#e9ecef", fg="#495057")
        help_text.pack(pady=8, padx=15)
        
        # Designs table
        self.create_designs_table(designs_frame)
    
    def create_designs_table(self, parent):
        """Create the uniform designs data table"""
        # Table frame
        table_frame = tk.Frame(parent, bg="#ffffff", relief="solid", bd=1)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Create Treeview with enhanced columns (enable extended selection for multiple items)
        columns = ('ID', 'Name', 'Course', 'Type', 'Colors', 'Status', 'Designer', 'Submitted Date', 'Image')
        self.designs_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15, selectmode='extended')
        
        # Define headings and column widths
        column_widths = {
            'ID': 80,
            'Name': 150,
            'Course': 120,
            'Type': 100,
            'Colors': 100,
            'Status': 120,
            'Designer': 120,
            'Submitted Date': 120,
            'Image': 80
        }
        
        for col in columns:
            self.designs_tree.heading(col, text=col)
            self.designs_tree.column(col, width=column_widths.get(col, 120), minwidth=80)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.designs_tree.yview)
        self.designs_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack table and scrollbar
        self.designs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind events
        self.designs_tree.bind('<Double-1>', self.edit_design)
        self.designs_tree.bind('<Button-3>', self.show_design_context_menu)  # Right-click
        self.designs_tree.bind('<Delete>', self.delete_design)  # Delete key
        self.designs_tree.bind('<F2>', self.edit_design)  # F2 key for edit
        
        # Load designs data
        self.load_designs_data()
        
        # Update course filter dropdown
        self.update_course_filter_options()
    
    def create_footer(self):
        """Create the dashboard footer"""
        footer_frame = tk.Frame(self.root, bg="#343a40", height=50)
        footer_frame.pack(fill=tk.X)
        footer_frame.pack_propagate(False)
        
        # Footer content with better layout
        footer_content = tk.Frame(footer_frame, bg="#343a40")
        footer_content.pack(expand=True, fill=tk.BOTH)
        
        # Left side - Copyright
        copyright_label = tk.Label(footer_content,
                                  text="© 2024 AI Uniform System",
                                  font=("Segoe UI", 10),
                                  fg="#ffffff",
                                  bg="#343a40")
        copyright_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Center - Dashboard info
        dashboard_label = tk.Label(footer_content,
                                  text="🎓 Guidance Dashboard - Student Uniform Management",
                                  font=("Segoe UI", 10, "bold"),
                                  fg="#ffffff",
                                  bg="#343a40")
        dashboard_label.pack(expand=True, pady=15)
        
        # Right side - Version/Status
        status_label = tk.Label(footer_content,
                               text="✅ System Online",
                               font=("Segoe UI", 9),
                               fg="#28a745",
                               bg="#343a40")
        status_label.pack(side=tk.RIGHT, padx=20, pady=15)
    
    # Data loading methods
    def load_violations_data(self):
        """Load violations data into the table"""
        # Clear existing items
        for item in self.violations_tree.get_children():
            self.violations_tree.delete(item)
        
        # Insert violations data
        for violation in self.violations:
            self.violations_tree.insert('', 'end', values=(
                violation.get('id', ''),
                violation.get('student_name', ''),
                violation.get('student_id', ''),
                violation.get('violation_type', ''),
                violation.get('date', ''),
                violation.get('status', ''),
                violation.get('reported_by', '')
            ))
    
    def load_appeals_data(self):
        """Load appeals data into the table with enhanced display"""
        # Clear existing items
        for item in self.appeals_tree.get_children():
            self.appeals_tree.delete(item)
        
        # Insert appeals data with enhanced information
        for appeal in self.appeals:
            # Calculate days pending
            days_pending = self.calculate_days_pending(appeal.get('appeal_date', ''))
            
            # Create item with enhanced data
            item = self.appeals_tree.insert('', 'end', values=(
                appeal.get('id', ''),
                appeal.get('student_name', ''),
                appeal.get('student_id', ''),
                appeal.get('violation_id', ''),
                appeal.get('appeal_date', ''),
                appeal.get('status', ''),
                appeal.get('submitted_by', ''),
                appeal.get('priority', 'Medium'),
                f"{days_pending} days"
            ))
            
            # Apply color coding based on status and priority
            status = appeal.get('status', '')
            priority = appeal.get('priority', 'Medium')
            
            # Status-based colors
            if status == 'Pending Review':
                self.appeals_tree.set(item, 'Status', '⏳ Pending Review')
                self.appeals_tree.item(item, tags=('pending',))
            elif status == 'Under Investigation':
                self.appeals_tree.set(item, 'Status', '🔍 Under Investigation')
                self.appeals_tree.item(item, tags=('investigating',))
            elif status == 'Approved':
                self.appeals_tree.set(item, 'Status', '✅ Approved')
                self.appeals_tree.item(item, tags=('approved',))
            elif status == 'Rejected':
                self.appeals_tree.set(item, 'Status', '❌ Rejected')
                self.appeals_tree.item(item, tags=('rejected',))
            elif status == 'Closed':
                self.appeals_tree.set(item, 'Status', '🔒 Closed')
                self.appeals_tree.item(item, tags=('closed',))
            
            # Priority-based colors
            if priority == 'High':
                self.appeals_tree.set(item, 'Priority', '🔴 High')
            elif priority == 'Medium':
                self.appeals_tree.set(item, 'Priority', '🟡 Medium')
            elif priority == 'Low':
                self.appeals_tree.set(item, 'Priority', '🟢 Low')
            
            # Days pending warning
            if days_pending > 14:
                self.appeals_tree.set(item, 'Days Pending', f"⚠️ {days_pending} days")
                self.appeals_tree.item(item, tags=('urgent',))
        
        # Configure tag colors
        self.appeals_tree.tag_configure('pending', background='#fff3cd', foreground='#856404')
        self.appeals_tree.tag_configure('investigating', background='#d1ecf1', foreground='#0c5460')
        self.appeals_tree.tag_configure('approved', background='#d4edda', foreground='#155724')
        self.appeals_tree.tag_configure('rejected', background='#f8d7da', foreground='#721c24')
        self.appeals_tree.tag_configure('closed', background='#e2e3e5', foreground='#383d41')
        self.appeals_tree.tag_configure('urgent', background='#f8d7da', foreground='#721c24')
    
    def load_designs_data(self):
        """Load uniform designs data into the table"""
        # Clear existing items
        for item in self.designs_tree.get_children():
            self.designs_tree.delete(item)
        
        # Insert designs data
        for design in self.uniform_designs:
            image_status = "📷 Yes" if design.get('has_image') else "❌ No"
            self.designs_tree.insert('', 'end', values=(
                design.get('id', ''),
                design.get('name', ''),
                design.get('course', ''),
                design.get('type', ''),
                design.get('colors', ''),
                design.get('status', ''),
                design.get('designer', ''),
                design.get('submitted_date', ''),
                image_status
            ))
        
        # Update course filter options after loading data
        if hasattr(self, 'course_filter_combo'):
            self.update_course_filter_options()
    
    # Action methods
    def add_violation(self):
        """Add a new violation"""
        # Create a simple form dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Violation")
        dialog.geometry("400x500")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"400x500+{x}+{y}")
        
        # Form fields
        tk.Label(dialog, text="Add New Violation", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=20)
        
        # Student Name
        tk.Label(dialog, text="Student Name:", font=("Segoe UI", 12), bg="#ffffff").pack(anchor=tk.W, padx=20)
        student_name_entry = tk.Entry(dialog, font=("Segoe UI", 12), width=30)
        student_name_entry.pack(padx=20, pady=(0, 15), fill=tk.X)
        
        # Student ID
        tk.Label(dialog, text="Student ID:", font=("Segoe UI", 12), bg="#ffffff").pack(anchor=tk.W, padx=20)
        student_id_entry = tk.Entry(dialog, font=("Segoe UI", 12), width=30)
        student_id_entry.pack(padx=20, pady=(0, 15), fill=tk.X)
        
        # Violation Type
        tk.Label(dialog, text="Violation Type:", font=("Segoe UI", 12), bg="#ffffff").pack(anchor=tk.W, padx=20)
        violation_types = ["Improper Uniform", "Missing ID", "Wrong Shoes", "Inappropriate Attire", "Other"]
        violation_type_var = tk.StringVar(value=violation_types[0])
        violation_type_combo = ttk.Combobox(dialog, textvariable=violation_type_var, values=violation_types, font=("Segoe UI", 12))
        violation_type_combo.pack(padx=20, pady=(0, 15), fill=tk.X)
        
        # Description
        tk.Label(dialog, text="Description:", font=("Segoe UI", 12), bg="#ffffff").pack(anchor=tk.W, padx=20)
        description_text = tk.Text(dialog, height=4, font=("Segoe UI", 12))
        description_text.pack(padx=20, pady=(0, 15), fill=tk.X)
        
        # Status
        tk.Label(dialog, text="Status:", font=("Segoe UI", 12), bg="#ffffff").pack(anchor=tk.W, padx=20)
        status_types = ["Pending", "Under Review", "Resolved", "Dismissed"]
        status_var = tk.StringVar(value=status_types[0])
        status_combo = ttk.Combobox(dialog, textvariable=status_var, values=status_types, font=("Segoe UI", 12))
        status_combo.pack(padx=20, pady=(0, 15), fill=tk.X)
        
        # Reported By
        tk.Label(dialog, text="Reported By:", font=("Segoe UI", 12), bg="#ffffff").pack(anchor=tk.W, padx=20)
        reported_by_entry = tk.Entry(dialog, font=("Segoe UI", 12), width=30)
        reported_by_entry.pack(padx=20, pady=(0, 20), fill=tk.X)
        
        def save_violation():
            """Save violation to Firebase"""
            try:
                # Get form data
                violation_data = {
                    'student_name': student_name_entry.get().strip(),
                    'student_id': student_id_entry.get().strip(),
                    'violation_type': violation_type_var.get(),
                    'description': description_text.get("1.0", tk.END).strip(),
                    'status': status_var.get(),
                    'reported_by': reported_by_entry.get().strip(),
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'reported_by_user': self.user_data['username']
                }
                
                # Validate required fields
                if not all([violation_data['student_name'], violation_data['student_id'], violation_data['description']]):
                    messagebox.showerror("Error", "Please fill in all required fields.")
                    return
                
                # Save to Firebase
                doc_id = add_to_firebase('violations', violation_data)
                if doc_id:
                    violation_data['id'] = doc_id
                    self.violations.append(violation_data)
                    self.load_violations_data()  # Refresh table
                    messagebox.showinfo("Success", f"Violation added successfully!\nDocument ID: {doc_id}")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save violation to Firebase.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save violation: {str(e)}")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg="#ffffff")
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(button_frame, text="Cancel", font=("Segoe UI", 12), bg="#6c757d", fg="#ffffff",
                 command=dialog.destroy).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="Save Violation", font=("Segoe UI", 12, "bold"), bg="#28a745", fg="#ffffff",
                 command=save_violation).pack(side=tk.RIGHT)
    
    def edit_violation(self, event):
        """Edit selected violation"""
        selection = self.violations_tree.selection()
        if selection:
            item = self.violations_tree.item(selection[0])
            values = item['values']
            messagebox.showinfo("Edit Violation", f"Edit Violation: {values[0]}\n\nThis would open an edit form for:\nStudent: {values[1]}\nViolation: {values[3]}\nStatus: {values[5]}")
    
    def search_violations(self):
        """Search violations in Firebase"""
        search_term = self.violation_search.get().strip()
        if not search_term:
            messagebox.showwarning("Search", "Please enter a search term.")
            return
        
        try:
            # Search in Firebase by student name
            search_results = search_in_firebase('violations', 'student_name', search_term)
            
            if search_results:
                # Clear current table
                for item in self.violations_tree.get_children():
                    self.violations_tree.delete(item)
                
                # Show search results
                for violation in search_results:
                    self.violations_tree.insert('', 'end', values=(
                        violation.get('id', ''),
                        violation.get('student_name', ''),
                        violation.get('student_id', ''),
                        violation.get('violation_type', ''),
                        violation.get('date', ''),
                        violation.get('status', ''),
                        violation.get('reported_by', '')
                    ))
                
                messagebox.showinfo("Search Results", f"Found {len(search_results)} violations for '{search_term}'")
            else:
                messagebox.showinfo("Search Results", f"No violations found for '{search_term}'")
                
        except Exception as e:
            messagebox.showerror("Search Error", f"Failed to search violations: {str(e)}")
            # Fallback to local search
            self.search_violations_local(search_term)
    
    def search_violations_local(self, search_term):
        """Fallback local search if Firebase fails"""
        local_results = []
        for violation in self.violations:
            if (search_term.lower() in violation.get('student_name', '').lower() or
                search_term.lower() in violation.get('student_id', '').lower() or
                search_term.lower() in violation.get('violation_type', '').lower()):
                local_results.append(violation)
        
        if local_results:
            # Clear current table
            for item in self.violations_tree.get_children():
                self.violations_tree.delete(item)
            
            # Show local search results
            for violation in local_results:
                self.violations_tree.insert('', 'end', values=(
                    violation.get('id', ''),
                    violation.get('student_name', ''),
                    violation.get('student_id', ''),
                    violation.get('violation_type', ''),
                    violation.get('date', ''),
                    violation.get('status', ''),
                    violation.get('reported_by', '')
                ))
            
            messagebox.showinfo("Local Search Results", f"Found {len(local_results)} violations for '{search_term}' (local search)")
        else:
            messagebox.showinfo("Search Results", f"No violations found for '{search_term}'")
    
    def quick_process_appeals(self):
        """Quick process appeals for fast decision making"""
        try:
            # Get pending appeals
            pending_appeals = [appeal for appeal in self.appeals if appeal.get('status') == 'Pending Review']
            
            if not pending_appeals:
                messagebox.showinfo("No Pending Appeals", "There are no pending appeals to process.")
                return
            
            # Create quick process dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Quick Process Appeals")
            dialog.geometry("900x700")
            dialog.configure(bg="#ffffff")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (900 // 2)
            y = (dialog.winfo_screenheight() // 2) - (700 // 2)
            dialog.geometry(f"900x700+{x}+{y}")
            
            # Main frame
            main_frame = tk.Frame(dialog, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text="Quick Process Appeals", 
                                  font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Create notebook for different views
            notebook = ttk.Notebook(main_frame)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            # Tab 1: Pending Appeals List
            pending_frame = ttk.Frame(notebook)
            notebook.add(pending_frame, text="Pending Appeals")
            self.create_pending_appeals_tab(pending_frame, pending_appeals, dialog)
            
            # Tab 2: Quick Decisions
            decisions_frame = ttk.Frame(notebook)
            notebook.add(decisions_frame, text="Quick Decisions")
            self.create_quick_decisions_tab(decisions_frame, pending_appeals, dialog)
            
            # Tab 3: Decision Templates
            templates_frame = ttk.Frame(notebook)
            notebook.add(templates_frame, text="Decision Templates")
            self.create_decision_templates_tab(templates_frame)
            
        except Exception as e:
            print(f"Error in quick process appeals: {e}")
            messagebox.showerror("Error", f"Failed to open quick process dialog: {str(e)}")
    
    def create_pending_appeals_tab(self, parent, pending_appeals, parent_dialog):
        """Create the pending appeals tab"""
        try:
            # Main frame
            main_frame = tk.Frame(parent, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text=f"Pending Appeals ({len(pending_appeals)})", 
                                  font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Create treeview for pending appeals
            columns = ('ID', 'Student Name', 'Student ID', 'Appeal Type', 'Priority', 'Days Pending', 'Action')
            appeals_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
            
            # Define column widths
            column_widths = {
                'ID': 80, 'Student Name': 150, 'Student ID': 100, 'Appeal Type': 120,
                'Priority': 80, 'Days Pending': 100, 'Action': 100
            }
            
            for col in columns:
                appeals_tree.heading(col, text=col)
                appeals_tree.column(col, width=column_widths.get(col, 120), minwidth=80)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=appeals_tree.yview)
            appeals_tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack tree and scrollbar
            appeals_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 20))
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 20))
            
            # Load pending appeals
            for appeal in pending_appeals:
                days_pending = self.calculate_days_pending(appeal.get('appeal_date', ''))
                appeals_tree.insert('', 'end', values=(
                    appeal.get('id', ''),
                    appeal.get('student_name', ''),
                    appeal.get('student_id', ''),
                    appeal.get('appeal_type', ''),
                    appeal.get('priority', 'Medium'),
                    f"{days_pending} days",
                    "Process"
                ))
            
            # Bind double-click to process appeal
            def process_selected_appeal(event):
                selection = appeals_tree.selection()
                if selection:
                    item = appeals_tree.item(selection[0])
                    values = item['values']
                    appeal_id = values[0]
                    
                    # Find the appeal data
                    appeal_data = None
                    for appeal in pending_appeals:
                        if appeal.get('id') == appeal_id:
                            appeal_data = appeal
                            break
                    
                    if appeal_data:
                        self.process_single_appeal_quick(appeal_data, parent_dialog)
            
            appeals_tree.bind('<Double-1>', process_selected_appeal)
            
        except Exception as e:
            print(f"Error creating pending appeals tab: {e}")
            tk.Label(parent, text=f"Error loading pending appeals: {str(e)}", 
                    font=("Segoe UI", 12), bg="#ffffff", fg="#dc3545").pack(pady=50)
    
    def create_quick_decisions_tab(self, parent, pending_appeals, parent_dialog):
        """Create the quick decisions tab"""
        try:
            # Main frame
            main_frame = tk.Frame(parent, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text="Quick Decision Making", 
                                  font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Decision options frame
            decision_frame = tk.LabelFrame(main_frame, text="Common Decisions", 
                                         font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            decision_frame.pack(fill=tk.X, pady=(0, 20))
            
            # Quick decision buttons
            decisions = [
                ("✅ Approve Medical Exemption", "Approved", "Medical documentation verified"),
                ("✅ Approve Financial Hardship", "Approved", "Financial documentation verified"),
                ("❌ Reject Insufficient Evidence", "Rejected", "Insufficient supporting documentation"),
                ("❌ Reject Policy Violation", "Rejected", "Violation confirmed, no grounds for appeal"),
                ("⏳ Request More Information", "Under Investigation", "Additional documentation required"),
                ("📋 Schedule Hearing", "Under Investigation", "Complex case requiring formal hearing")
            ]
            
            for i, (text, status, reason) in enumerate(decisions):
                row = i // 2
                col = i % 2
                
                if col == 0:
                    row_frame = tk.Frame(decision_frame, bg="#ffffff")
                    row_frame.pack(fill=tk.X, pady=5, padx=15)
                
                btn = tk.Button(row_frame, text=text, font=("Segoe UI", 10, "bold"),
                               bg="#28a745" if "Approve" in text else "#dc3545" if "Reject" in text else "#ffc107",
                               fg="#ffffff", relief="flat", cursor="hand2",
                               command=lambda s=status, r=reason: self.apply_quick_decision(s, r, pending_appeals, parent_dialog))
                btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
            
        except Exception as e:
            print(f"Error creating quick decisions tab: {e}")
            tk.Label(parent, text=f"Error loading quick decisions: {str(e)}", 
                    font=("Segoe UI", 12), bg="#ffffff", fg="#dc3545").pack(pady=50)
    
    def create_decision_templates_tab(self, parent):
        """Create the decision templates tab"""
        try:
            # Main frame
            main_frame = tk.Frame(parent, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text="Decision Templates", 
                                  font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Templates frame
            templates_frame = tk.LabelFrame(main_frame, text="Pre-defined Decision Reasons", 
                                          font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            templates_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            
            # Decision templates
            templates = [
                ("Medical Exemption - Approved", "Medical documentation has been verified and approved. Student is exempt from uniform requirements due to documented medical condition."),
                ("Financial Hardship - Approved", "Financial documentation has been verified. Student is granted temporary exemption from uniform requirements due to demonstrated financial hardship."),
                ("Religious Exemption - Approved", "Religious documentation has been verified. Student is exempt from uniform requirements due to documented religious beliefs."),
                ("Insufficient Evidence - Rejected", "The appeal lacks sufficient supporting documentation. Please provide additional evidence to support your claim."),
                ("Policy Violation Confirmed - Rejected", "The violation has been confirmed through investigation. The appeal does not meet the criteria for exemption."),
                ("Additional Information Required", "Additional documentation is required to process this appeal. Please submit the requested information within 14 days."),
                ("Complex Case - Hearing Required", "This case requires a formal hearing due to its complexity. You will be notified of the hearing date and time.")
            ]
            
            # Create template list
            template_listbox = tk.Listbox(templates_frame, font=("Segoe UI", 10), height=15)
            template_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            # Add templates to listbox
            for title, description in templates:
                template_listbox.insert(tk.END, title)
            
            # Template preview frame
            preview_frame = tk.LabelFrame(main_frame, text="Template Preview", 
                                        font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            preview_frame.pack(fill=tk.X, pady=(0, 20))
            
            # Preview text widget
            preview_text = tk.Text(preview_frame, height=6, font=("Segoe UI", 11), wrap=tk.WORD, bg="#f8f9fa")
            preview_text.pack(fill=tk.X, padx=15, pady=15)
            
            # Bind selection change to show preview
            def show_template_preview(event):
                selection = template_listbox.curselection()
                if selection:
                    index = selection[0]
                    title, description = templates[index]
                    preview_text.delete("1.0", tk.END)
                    preview_text.insert("1.0", f"{title}\n\n{description}")
            
            template_listbox.bind('<<ListboxSelect>>', show_template_preview)
            
        except Exception as e:
            print(f"Error creating decision templates tab: {e}")
            tk.Label(parent, text=f"Error loading decision templates: {str(e)}", 
                    font=("Segoe UI", 12), bg="#ffffff", fg="#dc3545").pack(pady=50)
    
    def apply_quick_decision(self, status, reason, pending_appeals, parent_dialog):
        """Apply a quick decision to selected appeals"""
        try:
            if not pending_appeals:
                messagebox.showwarning("Warning", "No pending appeals available.")
                return
            
            # Create selection dialog
            dialog = tk.Toplevel(parent_dialog)
            dialog.title("Select Appeals for Quick Decision")
            dialog.geometry("600x500")
            dialog.configure(bg="#ffffff")
            dialog.transient(parent_dialog)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
            y = (dialog.winfo_screenheight() // 2) - (500 // 2)
            dialog.geometry(f"600x500+{x}+{y}")
            
            # Main frame
            main_frame = tk.Frame(dialog, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text=f"Apply {status} Decision", 
                                  font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Decision info
            decision_info = tk.Label(main_frame, text=f"Status: {status}\nReason: {reason}", 
                                   font=("Segoe UI", 12), bg="#ffffff", fg="#495057")
            decision_info.pack(pady=(0, 20))
            
            # Appeals selection frame
            selection_frame = tk.LabelFrame(main_frame, text="Select Appeals to Process", 
                                          font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            selection_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            
            # Create appeals listbox with checkboxes
            appeals_listbox = tk.Listbox(selection_frame, font=("Segoe UI", 10), selectmode=tk.MULTIPLE, height=15)
            appeals_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            
            # Add appeals to listbox
            for appeal in pending_appeals:
                days_pending = self.calculate_days_pending(appeal.get('appeal_date', ''))
                list_item = f"{appeal.get('student_name', 'Unknown')} - {appeal.get('appeal_type', 'Unknown')} - {days_pending} days pending"
                appeals_listbox.insert(tk.END, list_item)
            
            # Process button
            process_btn = tk.Button(main_frame, text="Apply Decision", font=("Segoe UI", 12, "bold"),
                                   bg="#28a745", fg="#ffffff", relief="flat", cursor="hand2",
                                   command=lambda: self.process_quick_decision(status, reason, pending_appeals, appeals_listbox, dialog, parent_dialog))
            process_btn.pack(pady=20)
            
        except Exception as e:
            print(f"Error applying quick decision: {e}")
            messagebox.showerror("Error", f"Failed to apply quick decision: {str(e)}")
    
    def process_quick_decision(self, status, reason, pending_appeals, appeals_listbox, dialog, parent_dialog):
        """Process the quick decision for selected appeals"""
        try:
            selected_indices = appeals_listbox.curselection()
            if not selected_indices:
                messagebox.showwarning("Warning", "Please select appeals to process.")
                return
            
            selected_appeals = [pending_appeals[i] for i in selected_indices]
            
            # Confirm action
            confirm_msg = f"Are you sure you want to apply '{status}' status to {len(selected_appeals)} appeals?\n\nReason: {reason}"
            if not messagebox.askyesno("Confirm Decision", confirm_msg):
                return
            
            # Update appeals
            updated_count = 0
            for appeal in selected_appeals:
                try:
                    appeal.update({
                        'status': status,
                        'decision_reason': reason,
                        'review_date': datetime.now().strftime("%Y-%m-%d"),
                        'assigned_to': self.user_data['full_name'],
                        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'updated_by': self.user_data['username']
                    })
                    
                    # Update in Firebase
                    if appeal.get('id'):
                        update_in_firebase('appeals', appeal['id'], appeal)
                        updated_count += 1
                
                except Exception as e:
                    print(f"Error updating appeal {appeal.get('id', 'Unknown')}: {e}")
            
            # Show results and close dialogs
            messagebox.showinfo("Success", f"Successfully processed {updated_count} appeals with status: {status}")
            dialog.destroy()
            parent_dialog.destroy()
            
            # Refresh data
            self.load_appeals_data()
            
        except Exception as e:
            print(f"Error processing quick decision: {e}")
            messagebox.showerror("Error", f"Failed to process quick decision: {str(e)}")
    
    def process_single_appeal_quick(self, appeal_data, parent_dialog):
        """Process a single appeal quickly"""
        try:
            # Create quick process dialog
            dialog = tk.Toplevel(parent_dialog)
            dialog.title(f"Quick Process Appeal - {appeal_data.get('student_name', 'Unknown')}")
            dialog.geometry("700x600")
            dialog.configure(bg="#ffffff")
            dialog.transient(parent_dialog)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
            y = (dialog.winfo_screenheight() // 2) - (600 // 2)
            dialog.geometry(f"700x600+{x}+{y}")
            
            # Main frame
            main_frame = tk.Frame(dialog, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text=f"Quick Process Appeal - {appeal_data.get('student_name', 'Unknown')}", 
                                  font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Appeal summary
            summary_frame = tk.LabelFrame(main_frame, text="Appeal Summary", 
                                        font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            summary_frame.pack(fill=tk.X, pady=(0, 20))
            
            # Summary info
            summary_info = f"""
Student: {appeal_data.get('student_name', 'Unknown')}
Student ID: {appeal_data.get('student_id', 'Unknown')}
Appeal Type: {appeal_data.get('appeal_type', 'Unknown')}
Priority: {appeal_data.get('priority', 'Medium')}
Submitted: {appeal_data.get('appeal_date', 'Unknown')}
Days Pending: {self.calculate_days_pending(appeal_data.get('appeal_date', ''))}
            """
            
            summary_label = tk.Label(summary_frame, text=summary_info.strip(), 
                                   font=("Segoe UI", 11), bg="#ffffff", fg="#495057", justify=tk.LEFT)
            summary_label.pack(pady=15, padx=15)
            
            # Quick decision frame
            decision_frame = tk.LabelFrame(main_frame, text="Quick Decision", 
                                         font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            decision_frame.pack(fill=tk.X, pady=(0, 20))
            
            # Decision options
            decision_var = tk.StringVar(value="Under Investigation")
            decision_combo = ttk.Combobox(decision_frame, textvariable=decision_var, 
                                        values=["Pending Review", "Under Investigation", "Approved", "Rejected", "Closed"],
                                        font=("Segoe UI", 12), width=30)
            decision_combo.pack(pady=15)
            
            # Decision reason
            reason_label = tk.Label(decision_frame, text="Decision Reason:", 
                                  font=("Segoe UI", 11, "bold"), bg="#ffffff")
            reason_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
            
            reason_text = tk.Text(decision_frame, height=4, font=("Segoe UI", 11), wrap=tk.WORD)
            reason_text.pack(fill=tk.X, padx=15, pady=(0, 15))
            
            # Pre-filled reasons based on appeal type
            appeal_type = appeal_data.get('appeal_type', '')
            if 'Medical' in appeal_type:
                reason_text.insert("1.0", "Medical documentation verified and approved.")
            elif 'Financial' in appeal_type:
                reason_text.insert("1.0", "Financial documentation verified and approved.")
            elif 'Religious' in appeal_type:
                reason_text.insert("1.0", "Religious documentation verified and approved.")
            else:
                reason_text.insert("1.0", "Under investigation - additional documentation required.")
            
            # Process button
            process_btn = tk.Button(main_frame, text="Process Appeal", font=("Segoe UI", 12, "bold"),
                                   bg="#28a745", fg="#ffffff", relief="flat", cursor="hand2",
                                   command=lambda: self.finalize_appeal_decision(appeal_data, decision_var.get(), 
                                                                              reason_text.get("1.0", tk.END).strip(), 
                                                                              dialog, parent_dialog))
            process_btn.pack(pady=20)
            
        except Exception as e:
            print(f"Error processing single appeal: {e}")
            messagebox.showerror("Error", f"Failed to process appeal: {str(e)}")
    
    def finalize_appeal_decision(self, appeal_data, status, reason, dialog, parent_dialog):
        """Finalize the appeal decision"""
        try:
            # Update appeal data
            appeal_data.update({
                'status': status,
                'decision_reason': reason,
                'review_date': datetime.now().strftime("%Y-%m-%d"),
                'assigned_to': self.user_data['full_name'],
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'updated_by': self.user_data['username']
            })
            
            # Update in Firebase
            if appeal_data.get('id'):
                update_in_firebase('appeals', appeal_data['id'], appeal_data)
                print(f"✅ Appeal updated in Firebase: {appeal_data['id']}")
            
            # Refresh data
            self.load_appeals_data()
            
            # Show success message
            messagebox.showinfo("Success", f"Appeal processed successfully!\nStatus: {status}\nReason: {reason}")
            
            # Close dialogs
            dialog.destroy()
            parent_dialog.destroy()
            
        except Exception as e:
            print(f"Error finalizing appeal decision: {e}")
            messagebox.showerror("Error", f"Failed to finalize decision: {str(e)}")
    
    def process_appeals(self):
        """Process appeals with bulk operations"""
        # Create processing dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Process Appeals - Bulk Operations")
        dialog.geometry("800x600")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"800x600+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Process Appeals - Bulk Operations", 
                              font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Filter frame
        filter_frame = tk.LabelFrame(main_frame, text="Filter Appeals for Processing", 
                                   font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Filter controls
        filter_controls = tk.Frame(filter_frame, bg="#ffffff")
        filter_controls.pack(fill=tk.X, padx=15, pady=15)
        
        # Status filter
        tk.Label(filter_controls, text="Status:", font=("Segoe UI", 11), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 5))
        status_filter_var = tk.StringVar(value="Pending Review")
        status_filter_combo = ttk.Combobox(filter_controls, textvariable=status_filter_var, 
                                          values=["Pending Review", "Under Investigation", "All Statuses"],
                                          width=15, font=("Segoe UI", 11))
        status_filter_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        # Priority filter
        tk.Label(filter_controls, text="Priority:", font=("Segoe UI", 11), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 5))
        priority_filter_var = tk.StringVar(value="All Priorities")
        priority_filter_combo = ttk.Combobox(filter_controls, textvariable=priority_filter_var, 
                                            values=["All Priorities", "High", "Medium", "Low"],
                                            width=15, font=("Segoe UI", 11))
        priority_filter_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        # Apply filter button
        apply_filter_btn = tk.Button(filter_controls, text="Apply Filter", font=("Segoe UI", 10, "bold"),
                                    bg="#007bff", fg="#ffffff", relief="flat", cursor="hand2")
        apply_filter_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Bulk actions frame
        actions_frame = tk.LabelFrame(main_frame, text="Bulk Actions", 
                                    font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
        actions_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Action controls
        action_controls = tk.Frame(actions_frame, bg="#ffffff")
        action_controls.pack(fill=tk.X, padx=15, pady=15)
        
        # New status
        tk.Label(action_controls, text="New Status:", font=("Segoe UI", 11), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 5))
        new_status_var = tk.StringVar(value="Under Investigation")
        new_status_combo = ttk.Combobox(action_controls, textvariable=new_status_var, 
                                       values=["Pending Review", "Under Investigation", "Approved", "Rejected", "Closed"],
                                       width=15, font=("Segoe UI", 11))
        new_status_combo.pack(side=tk.LEFT, padx=(0, 15))
        
        # Assign to
        tk.Label(action_controls, text="Assign To:", font=("Segoe UI", 11), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 5))
        assign_var = tk.StringVar(value=self.user_data['full_name'])
        assign_entry = tk.Entry(action_controls, textvariable=assign_var, font=("Segoe UI", 11), width=20)
        assign_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        # Review date
        tk.Label(action_controls, text="Review Date:", font=("Segoe UI", 11), bg="#ffffff").pack(side=tk.LEFT, padx=(0, 5))
        review_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        review_date_entry = tk.Entry(action_controls, textvariable=review_date_var, font=("Segoe UI", 11), width=15)
        review_date_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        # Appeals list frame
        list_frame = tk.LabelFrame(main_frame, text="Appeals to Process", 
                                 font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create appeals list
        appeals_listbox = tk.Listbox(list_frame, font=("Segoe UI", 10), selectmode=tk.MULTIPLE)
        appeals_listbox.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        def load_filtered_appeals():
            """Load appeals based on filter criteria"""
            appeals_listbox.delete(0, tk.END)
            
            filtered_appeals = []
            for appeal in self.appeals:
                status_match = status_filter_var.get() == "All Statuses" or appeal.get('status') == status_filter_var.get()
                priority_match = priority_filter_var.get() == "All Priorities" or appeal.get('priority') == priority_filter_var.get()
                
                if status_match and priority_match:
                    filtered_appeals.append(appeal)
                    days_pending = self.calculate_days_pending(appeal.get('appeal_date', ''))
                    list_item = f"{appeal.get('student_name', 'Unknown')} - {appeal.get('status', 'Unknown')} - Priority: {appeal.get('priority', 'Medium')} - {days_pending} days pending"
                    appeals_listbox.insert(tk.END, list_item)
            
            return filtered_appeals
        
        def apply_bulk_action():
            """Apply bulk action to selected appeals"""
            try:
                selected_indices = appeals_listbox.curselection()
                if not selected_indices:
                    messagebox.showwarning("Warning", "Please select appeals to process.")
                    return
                
                filtered_appeals = load_filtered_appeals()
                selected_appeals = [filtered_appeals[i] for i in selected_indices]
                
                # Confirm action
                confirm_msg = f"Are you sure you want to update {len(selected_appeals)} appeals?\n\nNew Status: {new_status_var.get()}\nAssign To: {assign_var.get()}\nReview Date: {review_date_var.get()}"
                if not messagebox.askyesno("Confirm Bulk Action", confirm_msg):
                    return
                
                # Update appeals
                updated_count = 0
                for appeal in selected_appeals:
                    try:
                        appeal.update({
                            'status': new_status_var.get(),
                            'assigned_to': assign_var.get(),
                            'review_date': review_date_var.get(),
                            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            'updated_by': self.user_data['username']
                        })
                        
                        # Update in Firebase
                        if appeal.get('id'):
                            update_in_firebase('appeals', appeal['id'], appeal)
                            updated_count += 1
                    
                    except Exception as e:
                        print(f"Error updating appeal {appeal.get('id', 'Unknown')}: {e}")
                
                # Refresh data and show results
                self.load_appeals_data()
                messagebox.showinfo("Success", f"Successfully updated {updated_count} out of {len(selected_appeals)} appeals.")
                
                # Reload filtered appeals
                load_filtered_appeals()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply bulk action: {str(e)}")
        
        # Bind apply filter button
        apply_filter_btn.config(command=load_filtered_appeals)
        
        # Process button
        process_btn = tk.Button(main_frame, text="Apply Bulk Action", font=("Segoe UI", 12, "bold"),
                               bg="#28a745", fg="#ffffff", relief="flat", cursor="hand2",
                               command=apply_bulk_action)
        process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", font=("Segoe UI", 12, "bold"),
                             bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                             command=dialog.destroy)
        close_btn.pack(side=tk.RIGHT)
        
        # Load initial appeals
        load_filtered_appeals()
    
    def calculate_days_pending(self, appeal_date):
        """Calculate days since appeal was submitted"""
        try:
            if not appeal_date:
                return 0
            appeal_dt = datetime.strptime(appeal_date, "%Y-%m-%d")
            current_dt = datetime.now()
            delta = current_dt - appeal_dt
            return delta.days
        except Exception:
            return 0
    
    def show_appeal_context_menu(self, event):
        """Show context menu for appeals with quick actions"""
        # Select the item under the cursor
        item = self.appeals_tree.identify_row(event.y)
        if item:
            self.appeals_tree.selection_set(item)
            
            # Create context menu
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="⚡ Quick Process", command=lambda: self.quick_process_selected_appeal(event))
            context_menu.add_command(label="👁️ View Details", command=lambda: self.view_appeal_details(event))
            context_menu.add_separator()
            context_menu.add_command(label="✅ Approve", command=lambda: self.quick_approve_appeal(event))
            context_menu.add_command(label="❌ Reject", command=lambda: self.quick_reject_appeal(event))
            context_menu.add_command(label="⏳ Under Investigation", command=lambda: self.quick_investigate_appeal(event))
            context_menu.add_separator()
            context_menu.add_command(label="📝 Edit Appeal", command=lambda: self.edit_appeal_from_context(event))
            
            # Show context menu
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def quick_process_selected_appeal(self, event=None):
        """Quick process the selected appeal"""
        selection = self.appeals_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an appeal to process.")
            return
            
        # Get selected appeal
        item = self.appeals_tree.item(selection[0])
        values = item['values']
        appeal_id = values[0]
        
        # Find the appeal data
        appeal_data = None
        for appeal in self.appeals:
            if appeal.get('id') == appeal_id:
                appeal_data = appeal
                break
        
        if appeal_data:
            self.process_single_appeal_quick(appeal_data, self.root)
        else:
            messagebox.showerror("Error", "Appeal data not found.")
    
    def quick_approve_appeal(self, event):
        """Quick approve the selected appeal"""
        selection = self.appeals_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an appeal to approve.")
            return
            
        # Get selected appeal
        item = self.appeals_tree.item(selection[0])
        values = item['values']
        appeal_id = values[0]
        
        # Find the appeal data
        appeal_data = None
        for appeal in self.appeals:
            if appeal.get('id') == appeal_id:
                appeal_data = appeal
                break
        
        if appeal_data:
            self.quick_decision_with_reason(appeal_data, "Approved", "Appeal approved based on submitted documentation.")
        else:
            messagebox.showerror("Error", "Appeal data not found.")
    
    def quick_reject_appeal(self, event):
        """Quick reject the selected appeal"""
        selection = self.appeals_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an appeal to reject.")
            return
            
        # Get selected appeal
        item = self.appeals_tree.item(selection[0])
        values = item['values']
        appeal_id = values[0]
        
        # Find the appeal data
        appeal_data = None
        for appeal in self.appeals:
            if appeal.get('id') == appeal_id:
                appeal_data = appeal
                break
        
        if appeal_data:
            self.quick_decision_with_reason(appeal_data, "Rejected", "Appeal rejected - insufficient grounds for exemption.")
        else:
            messagebox.showerror("Error", "Appeal data not found.")
    
    def quick_investigate_appeal(self, event):
        """Quick set appeal to under investigation"""
        selection = self.appeals_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an appeal to investigate.")
            return
            
        # Get selected appeal
        item = self.appeals_tree.item(selection[0])
        values = item['values']
        appeal_id = values[0]
        
        # Find the appeal data
        appeal_data = None
        for appeal in self.appeals:
            if appeal.get('id') == appeal_id:
                appeal_data = appeal
                break
        
        if appeal_data:
            self.quick_decision_with_reason(appeal_data, "Under Investigation", "Appeal under investigation - additional documentation required.")
        else:
            messagebox.showerror("Error", "Appeal data not found.")
    
    def quick_decision_with_reason(self, appeal_data, status, reason):
        """Apply a quick decision with predefined reason"""
        try:
            # Update appeal data
            appeal_data.update({
                'status': status,
                'decision_reason': reason,
                'review_date': datetime.now().strftime("%Y-%m-%d"),
                'assigned_to': self.user_data['full_name'],
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'updated_by': self.user_data['username']
            })
            
            # Update in Firebase
            if appeal_data.get('id'):
                update_in_firebase('appeals', appeal_data['id'], appeal_data)
                print(f"✅ Appeal updated in Firebase: {appeal_data['id']}")
            
            # Refresh data
            self.load_appeals_data()
            
            # Show success message
            messagebox.showinfo("Success", f"Appeal processed successfully!\nStatus: {status}\nReason: {reason}")
            
        except Exception as e:
            print(f"Error applying quick decision: {e}")
            messagebox.showerror("Error", f"Failed to apply quick decision: {str(e)}")
    
    def edit_appeal_from_context(self, event):
        """Edit appeal from context menu"""
        selection = self.appeals_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select an appeal to edit.")
            return
            
        # Get selected appeal
        item = self.appeals_tree.item(selection[0])
        values = item['values']
        appeal_id = values[0]
        
        # Find the appeal data
        appeal_data = None
        for appeal in self.appeals:
            if appeal.get('id') == appeal_id:
                appeal_data = appeal
                break
        
        if appeal_data:
            self.edit_appeal(appeal_data, self.root)
        else:
            messagebox.showerror("Error", "Appeal data not found.")
    
    def view_appeal_details(self, event):
        """View appeal details with comprehensive information"""
        selection = self.appeals_tree.selection()
        if selection:
            item = self.appeals_tree.item(selection[0])
            values = item['values']
            appeal_id = values[0]
            
            # Find the appeal data
            appeal_data = None
            for appeal in self.appeals:
                if appeal.get('id') == appeal_id:
                    appeal_data = appeal
                    break
            
            if appeal_data:
                self.show_appeal_details_dialog(appeal_data)
            else:
                messagebox.showerror("Error", "Appeal data not found")
    
    def show_appeal_details_dialog(self, appeal_data):
        """Show comprehensive appeal details dialog"""
        # Create details dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Appeal Details - {appeal_data.get('student_name', 'Unknown')}")
        dialog.geometry("800x700")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f"800x700+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text=f"Appeal Details - {appeal_data.get('student_name', 'Unknown')}", 
                              font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(main_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Student Information Section
        student_frame = tk.LabelFrame(scrollable_frame, text="Student Information", 
                                    font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
        student_frame.pack(fill=tk.X, pady=(0, 15))
        
        student_info = [
            ("Student Name:", appeal_data.get('student_name', '')),
            ("Student ID:", appeal_data.get('student_id', '')),
            ("Violation ID:", appeal_data.get('violation_id', '')),
            ("Appeal Type:", appeal_data.get('appeal_type', 'Uniform Violation'))
        ]
        
        for i, (label, value) in enumerate(student_info):
            row_frame = tk.Frame(student_frame, bg="#ffffff")
            row_frame.pack(fill=tk.X, pady=5, padx=10)
            
            tk.Label(row_frame, text=label, font=("Segoe UI", 11, "bold"), 
                    bg="#ffffff", width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row_frame, text=value, font=("Segoe UI", 11), 
                    bg="#ffffff", anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))
        
        # Appeal Details Section
        appeal_frame = tk.LabelFrame(scrollable_frame, text="Appeal Details", 
                                   font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
        appeal_frame.pack(fill=tk.X, pady=(0, 15))
        
        appeal_info = [
            ("Appeal Date:", appeal_data.get('appeal_date', '')),
            ("Status:", appeal_data.get('status', '')),
            ("Priority:", appeal_data.get('priority', 'Medium')),
            ("Submitted By:", appeal_data.get('submitted_by', '')),
            ("Assigned To:", appeal_data.get('assigned_to', 'Not Assigned')),
            ("Review Date:", appeal_data.get('review_date', 'Not Set'))
        ]
        
        for i, (label, value) in enumerate(appeal_info):
            row_frame = tk.Frame(appeal_frame, bg="#ffffff")
            row_frame.pack(fill=tk.X, pady=5, padx=10)
            
            tk.Label(row_frame, text=label, font=("Segoe UI", 11, "bold"), 
                    bg="#ffffff", width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row_frame, text=value, font=("Segoe UI", 11), 
                    bg="#ffffff", anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))
        
        # Reason and Notes Section
        reason_frame = tk.LabelFrame(scrollable_frame, text="Appeal Reason & Notes", 
                                   font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
        reason_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Reason
        tk.Label(reason_frame, text="Reason:", font=("Segoe UI", 11, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, padx=10, pady=(10, 5))
        reason_text = tk.Text(reason_frame, height=3, font=("Segoe UI", 11), wrap=tk.WORD)
        reason_text.pack(fill=tk.X, padx=10, pady=(0, 10))
        reason_text.insert("1.0", appeal_data.get('reason', ''))
        reason_text.config(state=tk.DISABLED)
        
        # Notes
        if appeal_data.get('notes'):
            tk.Label(reason_frame, text="Notes:", font=("Segoe UI", 11, "bold"), 
                    bg="#ffffff").pack(anchor=tk.W, padx=10, pady=(10, 5))
            notes_text = tk.Text(reason_frame, height=3, font=("Segoe UI", 11), wrap=tk.WORD)
            notes_text.pack(fill=tk.X, padx=10, pady=(0, 10))
            notes_text.insert("1.0", appeal_data.get('notes', ''))
            notes_text.config(state=tk.DISABLED)
        
        # Evidence Documents Section
        if appeal_data.get('evidence_documents'):
            docs_frame = tk.LabelFrame(scrollable_frame, text="Evidence Documents", 
                                     font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            docs_frame.pack(fill=tk.X, pady=(0, 15))
            
            for doc in appeal_data.get('evidence_documents', []):
                doc_label = tk.Label(docs_frame, text=f"📎 {doc}", font=("Segoe UI", 11), 
                                   bg="#ffffff", fg="#007bff")
                doc_label.pack(anchor=tk.W, padx=10, pady=2)
        
        # Decision Section (if applicable)
        if appeal_data.get('decision_reason'):
            decision_frame = tk.LabelFrame(scrollable_frame, text="Decision", 
                                        font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            decision_frame.pack(fill=tk.X, pady=(0, 15))
            
            tk.Label(decision_frame, text="Decision Reason:", font=("Segoe UI", 11, "bold"), 
                    bg="#ffffff").pack(anchor=tk.W, padx=10, pady=(10, 5))
            decision_text = tk.Text(decision_frame, height=3, font=("Segoe UI", 11), wrap=tk.WORD)
            decision_text.pack(fill=tk.X, padx=10, pady=(0, 10))
            decision_text.insert("1.0", appeal_data.get('decision_reason', ''))
            decision_text.config(state=tk.DISABLED)
        
        # Action Buttons
        action_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        action_frame.pack(fill=tk.X, pady=20)
        
        # Process Appeal button
        process_btn = tk.Button(action_frame, text="Process Appeal", font=("Segoe UI", 12, "bold"),
                               bg="#ffc107", fg="#000000", relief="flat", cursor="hand2",
                               command=lambda: self.process_specific_appeal(appeal_data, dialog))
        process_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Edit Appeal button
        edit_btn = tk.Button(action_frame, text="Edit Appeal", font=("Segoe UI", 12, "bold"),
                            bg="#17a2b8", fg="#ffffff", relief="flat", cursor="hand2",
                            command=lambda: self.edit_appeal(appeal_data, dialog))
        edit_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        close_btn = tk.Button(action_frame, text="Close", font=("Segoe UI", 12, "bold"),
                             bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                             command=dialog.destroy)
        close_btn.pack(side=tk.RIGHT)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def add_uniform_design(self):
        """Add new uniform design with image upload"""
        # Create a comprehensive form dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Uniform Design")
        dialog.geometry("700x800")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (800 // 2)
        dialog.geometry(f"700x800+{x}+{y}")
        
        # Main form frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Add New Uniform Design", 
                              font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Create scrollable frame for form
        canvas = tk.Canvas(main_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields frame
        form_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Design Name
        tk.Label(form_frame, text="Design Name:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        design_name_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        design_name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Course
        tk.Label(form_frame, text="Course:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        course_var = tk.StringVar()
        course_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        course_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Design Type
        tk.Label(form_frame, text="Design Type:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        design_types = ["Polo Shirt", "T-Shirt", "Blouse", "Pants", "Skirt", "Dress", "Jacket", "Other"]
        design_type_var = tk.StringVar(value=design_types[0])
        design_type_combo = ttk.Combobox(form_frame, textvariable=design_type_var, 
                                        values=design_types, font=("Segoe UI", 12))
        design_type_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Colors
        tk.Label(form_frame, text="Colors:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        colors_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        colors_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Size Range
        tk.Label(form_frame, text="Size Range:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        size_range_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        size_range_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Image Upload Section
        tk.Label(form_frame, text="Design Image:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(20, 5))
        
        # Image upload frame
        image_frame = tk.Frame(form_frame, bg="#ffffff")
        image_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Variables for image handling
        image_path = tk.StringVar()
        image_preview_label = None
        
        def browse_image():
            """Browse and select image file"""
            from tkinter import filedialog
            file_types = [
                ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp'),
                ('PNG files', '*.png'),
                ('JPEG files', '*.jpg *.jpeg'),
                ('All files', '*.*')
            ]
            filename = filedialog.askopenfilename(
                title="Select Design Image",
                filetypes=file_types
            )
            if filename:
                image_path.set(filename)
                show_image_preview(filename)
        
        def show_image_preview(filepath):
            """Show image preview"""
            nonlocal image_preview_label
            try:
                from PIL import Image, ImageTk
                # Open and resize image for preview
                image = Image.open(filepath)
                # Resize to fit preview area (max 200x200)
                image.thumbnail((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                
                # Update or create preview label
                if image_preview_label:
                    image_preview_label.destroy()
                
                image_preview_label = tk.Label(image_frame, image=photo, bg="#f8f9fa", relief="solid", bd=1)
                image_preview_label.image = photo  # Keep a reference
                image_preview_label.pack(side=tk.RIGHT, padx=(10, 0))
                
                # Show file path (use os.path.basename for cross-platform compatibility)
                filename = os.path.basename(filepath)
                path_label.config(text=f"Selected: {filename}")
                
            except Exception as e:
                messagebox.showerror("Image Error", f"Failed to load image: {str(e)}")
                # Clear the path if image loading fails
                path_label.config(text="Image loading failed")
        
        # Browse button
        browse_btn = tk.Button(image_frame, text="Browse Image", font=("Segoe UI", 10, "bold"),
                              bg="#007bff", fg="#ffffff", relief="flat", cursor="hand2",
                              command=browse_image)
        browse_btn.pack(side=tk.LEFT)
        
        # File path label
        path_label = tk.Label(image_frame, text="No image selected", font=("Segoe UI", 10), 
                             bg="#ffffff", fg="#6c757d")
        path_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Progress label for annotation status
        progress_label = tk.Label(image_frame, text="", font=("Segoe UI", 10), 
                                 bg="#ffffff", fg="#28a745")
        progress_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Description
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(20, 5))
        description_text = tk.Text(form_frame, height=4, font=("Segoe UI", 12))
        description_text.pack(fill=tk.X, pady=(0, 15))
        
        # Status
        tk.Label(form_frame, text="Status:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        status_types = ["Under Review", "Approved", "Rejected", "In Production", "Discontinued"]
        status_var = tk.StringVar(value=status_types[0])
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, 
                                   values=status_types, font=("Segoe UI", 12))
        status_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Designer/Submitter
        tk.Label(form_frame, text="Designer/Submitter:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        designer_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        designer_entry.pack(fill=tk.X, pady=(0, 15))
        
        def save_design():
            """Save uniform design to Firebase with automatic annotation and uniqueness detection"""
            try:
                # Get form data (base fields first)
                design_data = {
                    'name': design_name_entry.get().strip(),
                    'course': course_entry.get().strip(),
                    'type': design_type_var.get(),
                    'colors': colors_entry.get().strip(),
                    'size_range': size_range_entry.get().strip(),
                    'description': description_text.get("1.0", tk.END).strip(),
                    'status': status_var.get(),
                    'designer': designer_entry.get().strip(),
                    'submitted_date': datetime.now().strftime("%Y-%m-%d"),
                    'submitted_by': self.user_data['username'],
                    'submitted_by_name': self.user_data['full_name'],
                    'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'has_image': False,
                    'image_url': None,
                    'image_storage_path': None,
                }
                local_image_path = image_path.get()
                if local_image_path:
                    design_data['image_path_local'] = local_image_path
                    design_data['has_image'] = True
                
                # Validate required fields
                if not all([design_data['name'], design_data['course'], design_data['type'], design_data['colors']]):
                    messagebox.showerror("Error", "Please fill in all required fields (Name, Course, Type, Colors).")
                    return
                
                # AUTOMATIC ANNOTATION AND UNIQUENESS DETECTION
                annotation_data = None
                if local_image_path:
                    try:
                        # Import and use the uniform annotator
                        from uniform_annotation import UniformAnnotator
                        
                        # Show annotation progress
                        progress_label.config(text="🔍 Analyzing uniform design...")
                        dialog.update()
                        
                        # Initialize annotator and process image
                        annotator = UniformAnnotator()
                        annotation_data = annotator.annotate_uniform(local_image_path)
                        
                        if not annotation_data.get('error'):
                            # Create annotated image
                            annotated_path = annotator.create_annotated_image(
                                local_image_path, annotation_data
                            )
                            
                            # Add annotation data to design
                            design_data['annotation_data'] = annotation_data
                            design_data['annotated_image_path'] = annotated_path
                            design_data['uniqueness_signature'] = annotation_data.get('uniqueness_signature')
                            design_data['detection_count'] = annotation_data.get('detection_results', {}).get('total_detections', 0)
                            
                            # Check for similar existing uniforms
                            similar_uniforms = self._find_similar_existing_uniforms(annotation_data)
                            if similar_uniforms:
                                design_data['similar_uniforms'] = similar_uniforms
                                design_data['similarity_warning'] = True
                            
                            progress_label.config(text="✅ Analysis complete! Uniform annotated and uniqueness detected.")
                        else:
                            progress_label.config(text="⚠️ Analysis completed with warnings. Check details below.")
                            
                    except Exception as e:
                        logger.error(f"❌ Automatic annotation failed: {e}")
                        progress_label.config(text="⚠️ Automatic annotation failed. Proceeding without annotation.")
                        # Continue without annotation - non-fatal error
                
                # Create Firestore document first to obtain ID
                doc_id = add_to_firebase('uniform_designs', design_data)
                if not doc_id:
                    messagebox.showerror("Error", "Failed to save design to Firebase.")
                    return
                
                design_data['id'] = doc_id
                
                # If an image was selected, try to upload it to Firebase Storage
                if local_image_path:
                    try:
                        filename = os.path.basename(local_image_path)
                        destination = f"uniform_designs/{doc_id}/{filename}"
                        image_url = upload_to_storage(local_image_path, destination, True)
                        if image_url:
                            # Successfully uploaded to Storage
                            update_in_firebase('uniform_designs', doc_id, {
                                'image_url': image_url,
                                'image_storage_path': destination,
                                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            })
                            design_data['image_url'] = image_url
                            design_data['image_storage_path'] = destination
                        else:
                            # Storage upload failed (likely due to billing plan)
                            print("⚠️ Image will be stored locally only. Upgrade to Blaze plan for cloud storage.")
                    except Exception as e:
                        # Non-fatal; keep document without image URL
                        print(f"⚠️ Image upload failed: {e}")
                
                # Add to local list and refresh table
                self.uniform_designs.append(design_data)
                self.load_designs_data()
                
                # Success message with annotation details
                success_lines = [f"Uniform design added successfully!", f"Document ID: {doc_id}"]
                if design_data.get('image_url'):
                    success_lines.append("✅ Image uploaded to Firebase Storage")
                elif design_data.get('image_path_local'):
                    success_lines.append("📁 Image saved locally (upgrade to Blaze plan for cloud storage)")
                
                if annotation_data and not annotation_data.get('error'):
                    success_lines.append("🔍 Automatic annotation completed")
                    success_lines.append(f"📊 Detected {design_data.get('detection_count', 0)} uniform elements")
                    if design_data.get('similarity_warning'):
                        success_lines.append("⚠️ Similar uniforms detected - check for duplicates")
                
                messagebox.showinfo("Success", "\n".join(success_lines))
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save design: {str(e)}")
        
        # Buttons frame
        button_frame = tk.Frame(form_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, pady=20)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", font=("Segoe UI", 12), 
                              bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                              command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save button
        save_btn = tk.Button(button_frame, text="Save Design", font=("Segoe UI", 12, "bold"), 
                            bg="#28a745", fg="#ffffff", relief="flat", cursor="hand2",
                            command=save_design)
        save_btn.pack(side=tk.RIGHT)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Set focus to first field
        design_name_entry.focus()
    
    def _find_similar_existing_uniforms(self, annotation_data: Dict) -> List[Dict]:
        """Find existing uniforms similar to the new one being uploaded"""
        try:
            from uniform_annotation import UniformAnnotator
            
            if not annotation_data or annotation_data.get('error'):
                return []
            
            # Get uniqueness signature from new uniform
            new_signature = annotation_data.get('uniqueness_signature')
            if not new_signature:
                return []
            
            # Initialize annotator for comparison
            annotator = UniformAnnotator()
            similar_uniforms = []
            
            # Compare with existing uniforms that have annotations
            for existing_design in self.uniform_designs:
                if not existing_design.get('annotation_data'):
                    continue
                
                try:
                    # Compare the two uniforms
                    similarity = annotator.compare_uniforms(
                        annotation_data, 
                        existing_design['annotation_data']
                    )
                    
                    if not similarity.get('error') and similarity.get('overall_similarity', 0) > 0.7:
                        similar_uniforms.append({
                            'design_id': existing_design.get('id'),
                            'design_name': existing_design.get('name'),
                            'similarity_score': similarity.get('overall_similarity', 0),
                            'similarity_details': similarity,
                            'existing_design': existing_design
                        })
                        
                except Exception as e:
                    logger.error(f"❌ Failed to compare with existing uniform: {e}")
                    continue
            
            # Sort by similarity (highest first)
            similar_uniforms.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            return similar_uniforms[:5]  # Return top 5 most similar
            
        except Exception as e:
            logger.error(f"❌ Failed to find similar uniforms: {e}")
            return []
    
    def view_uniform_annotations(self):
        """View detailed annotations and uniqueness analysis for all uniforms"""
        # Create a comprehensive annotation viewer dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Uniform Annotations & Uniqueness Analysis")
        dialog.geometry("1200x800")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (1200 // 2)
        y = (dialog.winfo_screenheight() // 2) - (800 // 2)
        dialog.geometry(f"1200x800+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="🔍 Uniform Annotations & Uniqueness Analysis", 
                              font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Annotations Overview
        annotations_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(annotations_frame, text="📊 Annotations Overview")
        
        # Annotations overview content
        self._create_annotations_overview(annotations_frame)
        
        # Tab 2: Similarity Analysis
        similarity_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(similarity_frame, text="🔗 Similarity Analysis")
        
        # Similarity analysis content
        self._create_similarity_analysis(similarity_frame)
        
        # Tab 3: Detection Details
        detection_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(detection_frame, text="🎯 Detection Details")
        
        # Detection details content
        self._create_detection_details(detection_frame)
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", font=("Segoe UI", 12, "bold"),
                             bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                             command=dialog.destroy)
        close_btn.pack(pady=20)
    
    def _create_annotations_overview(self, parent_frame):
        """Create annotations overview tab content"""
        # Create scrollable frame
        canvas = tk.Canvas(parent_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="solid", bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_labels = ["Design Name", "Course", "Type", "Annotation Status", "Detections", "Uniqueness"]
        for i, label in enumerate(header_labels):
            tk.Label(header_frame, text=label, font=("Segoe UI", 11, "bold"), 
                    bg="#f8f9fa", fg="#1877f2").grid(row=0, column=i, padx=10, pady=10, sticky="ew")
        
        # Configure column weights
        for i in range(len(header_labels)):
            header_frame.grid_columnconfigure(i, weight=1)
        
        # Add uniform data
        row = 1
        for design in self.uniform_designs:
            if design.get('annotation_data'):
                # Design info
                tk.Label(scrollable_frame, text=design.get('name', 'N/A'), 
                        font=("Segoe UI", 10), bg="#ffffff").grid(row=row, column=0, padx=5, pady=5, sticky="w")
                tk.Label(scrollable_frame, text=design.get('course', 'N/A'), 
                        font=("Segoe UI", 10), bg="#ffffff").grid(row=row, column=1, padx=5, pady=5, sticky="w")
                tk.Label(scrollable_frame, text=design.get('type', 'N/A'), 
                        font=("Segoe UI", 10), bg="#ffffff").grid(row=row, column=2, padx=5, pady=5, sticky="w")
                
                # Annotation status
                status_text = "✅ Annotated"
                status_color = "#28a745"
                tk.Label(scrollable_frame, text=status_text, font=("Segoe UI", 10), 
                        bg="#ffffff", fg=status_color).grid(row=row, column=3, padx=5, pady=5, sticky="w")
                
                # Detection count
                detection_count = design.get('detection_count', 0)
                tk.Label(scrollable_frame, text=str(detection_count), font=("Segoe UI", 10), 
                        bg="#ffffff").grid(row=row, column=4, padx=5, pady=5, sticky="w")
                
                # Uniqueness signature (shortened)
                uniqueness = design.get('uniqueness_signature', 'N/A')
                if uniqueness != 'N/A':
                    uniqueness = uniqueness[:8] + "..."
                tk.Label(scrollable_frame, text=uniqueness, font=("Segoe UI", 10), 
                        bg="#ffffff", fg="#6c757d").grid(row=row, column=5, padx=5, pady=5, sticky="w")
                
                row += 1
            else:
                # No annotation data
                tk.Label(scrollable_frame, text=design.get('name', 'N/A'), 
                        font=("Segoe UI", 10), bg="#ffffff").grid(row=row, column=0, padx=5, pady=5, sticky="w")
                tk.Label(scrollable_frame, text=design.get('course', 'N/A'), 
                        font=("Segoe UI", 10), bg="#ffffff").grid(row=row, column=1, padx=5, pady=5, sticky="w")
                tk.Label(scrollable_frame, text=design.get('type', 'N/A'), 
                        font=("Segoe UI", 10), bg="#ffffff").grid(row=row, column=2, padx=5, pady=5, sticky="w")
                
                # No annotation
                tk.Label(scrollable_frame, text="❌ No Annotation", font=("Segoe UI", 10), 
                        bg="#ffffff", fg="#dc3545").grid(row=row, column=3, padx=5, pady=5, sticky="w")
                tk.Label(scrollable_frame, text="N/A", font=("Segoe UI", 10), 
                        bg="#ffffff").grid(row=row, column=4, padx=5, pady=5, sticky="w")
                tk.Label(scrollable_frame, text="N/A", font=("Segoe UI", 10), 
                        bg="#ffffff").grid(row=row, column=5, padx=5, pady=5, sticky="w")
                
                row += 1
        
        # Configure grid columns
        for i in range(6):
            scrollable_frame.grid_columnconfigure(i, weight=1)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_similarity_analysis(self, parent_frame):
        """Create similarity analysis tab content"""
        # Create scrollable frame
        canvas = tk.Canvas(parent_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="solid", bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_labels = ["Design Name", "Course", "Similarity Score", "Color Similarity", "Texture Similarity", "Edge Similarity"]
        for i, label in enumerate(header_labels):
            tk.Label(header_frame, text=label, font=("Segoe UI", 11, "bold"), 
                    bg="#f8f9fa", fg="#1877f2").grid(row=0, column=i, padx=10, pady=10, sticky="ew")
        
        # Configure column weights
        for i in range(len(header_labels)):
            header_frame.grid_columnconfigure(i, weight=1)
        
        # Add similarity data
        row = 1
        for design in self.uniform_designs:
            if design.get('similar_uniforms'):
                for similar in design['similar_uniforms']:
                    # Design info
                    tk.Label(scrollable_frame, text=design.get('name', 'N/A'), 
                            font=("Segoe UI", 10), bg="#ffffff").grid(row=row, column=0, padx=5, pady=5, sticky="w")
                    tk.Label(scrollable_frame, text=design.get('course', 'N/A'), 
                            font=("Segoe UI", 10), bg="#ffffff").grid(row=row, column=1, padx=5, pady=5, sticky="w")
                    
                    # Similarity scores
                    overall_score = similar.get('similarity_score', 0)
                    tk.Label(scrollable_frame, text=f"{overall_score:.3f}", font=("Segoe UI", 10), 
                            bg="#ffffff", fg="#dc3545" if overall_score > 0.8 else "#ffc107").grid(row=row, column=2, padx=5, pady=5, sticky="w")
                    
                    similarity_details = similar.get('similarity_details', {})
                    color_sim = similarity_details.get('color_similarity', 0)
                    texture_sim = similarity_details.get('texture_similarity', 0)
                    edge_sim = similarity_details.get('edge_similarity', 0)
                    
                    tk.Label(scrollable_frame, text=f"{color_sim:.3f}", font=("Segoe UI", 10), 
                            bg="#ffffff").grid(row=row, column=3, padx=5, pady=5, sticky="w")
                    tk.Label(scrollable_frame, text=f"{texture_sim:.3f}", font=("Segoe UI", 10), 
                            bg="#ffffff").grid(row=row, column=4, padx=5, pady=5, sticky="w")
                    tk.Label(scrollable_frame, text=f"{edge_sim:.3f}", font=("Segoe UI", 10), 
                            bg="#ffffff").grid(row=row, column=5, padx=5, pady=5, sticky="w")
                    
                    row += 1
        
        # Configure grid columns
        for i in range(6):
            scrollable_frame.grid_columnconfigure(i, weight=1)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_detection_details(self, parent_frame):
        """Create detection details tab content"""
        # Create scrollable frame
        canvas = tk.Canvas(parent_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="solid", bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_labels = ["Design Name", "Detected Elements", "Confidence", "Bounding Box", "Area"]
        for i, label in enumerate(header_labels):
            tk.Label(header_frame, text=label, font=("Segoe UI", 11, "bold"), 
                    bg="#f8f9fa", fg="#1877f2").grid(row=0, column=i, padx=10, pady=10, sticky="ew")
        
        # Configure column weights
        for i in range(len(header_labels)):
            header_frame.grid_columnconfigure(i, weight=1)
        
        # Add detection data
        row = 1
        for design in self.uniform_designs:
            if design.get('annotation_data'):
                annotation = design['annotation_data']
                detections = annotation.get('detection_results', {}).get('detections', [])
                
                for detection in detections:
                    # Design name
                    tk.Label(scrollable_frame, text=design.get('name', 'N/A'), 
                            font=("Segoe UI", 10), bg="#ffffff").grid(row=row, column=0, padx=5, pady=5, sticky="w")
                    
                    # Detected element
                    class_name = detection.get('class_name', 'Unknown')
                    tk.Label(scrollable_frame, text=class_name, font=("Segoe UI", 10), 
                            bg="#ffffff").grid(row=row, column=1, padx=5, pady=5, sticky="w")
                    
                    # Confidence
                    confidence = detection.get('confidence', 0)
                    tk.Label(scrollable_frame, text=f"{confidence:.3f}", font=("Segoe UI", 10), 
                            bg="#ffffff").grid(row=row, column=2, padx=5, pady=5, sticky="w")
                    
                    # Bounding box
                    bbox = detection.get('bbox', {})
                    bbox_text = f"({bbox.get('x1', 0):.0f}, {bbox.get('y1', 0):.0f}) - ({bbox.get('x2', 0):.0f}, {bbox.get('y2', 0):.0f})"
                    tk.Label(scrollable_frame, text=bbox_text, font=("Segoe UI", 10), 
                            bg="#ffffff", fg="#6c757d").grid(row=row, column=3, padx=5, pady=5, sticky="w")
                    
                    # Area
                    area = detection.get('area', 0)
                    tk.Label(scrollable_frame, text=f"{area:.0f}", font=("Segoe UI", 10), 
                            bg="#ffffff").grid(row=row, column=4, padx=5, pady=5, sticky="w")
                    
                    row += 1
        
        # Configure grid columns
        for i in range(5):
            scrollable_frame.grid_columnconfigure(i, weight=1)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def browse_designs(self):
        """Browse uniform designs with detailed view"""
        # Create a detailed browse dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Browse Uniform Designs")
        dialog.geometry("1000x700")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (1000 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f"1000x700+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Browse Uniform Designs", 
                              font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Filter frame
        filter_frame = tk.Frame(main_frame, bg="#f8f9fa", relief="solid", bd=1)
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Filter controls
        tk.Label(filter_frame, text="Filters:", font=("Segoe UI", 12, "bold"), 
                bg="#f8f9fa").pack(side=tk.LEFT, padx=20, pady=10)
        
        # Status filter
        tk.Label(filter_frame, text="Status:", font=("Segoe UI", 10), bg="#f8f9fa").pack(side=tk.LEFT, padx=(20, 5))
        status_filter_var = tk.StringVar(value="All")
        status_filter_combo = ttk.Combobox(filter_frame, textvariable=status_filter_var, 
                                          values=["All", "Under Review", "Approved", "Rejected", "In Production", "Discontinued"],
                                          width=15, font=("Segoe UI", 10))
        status_filter_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        # Type filter
        tk.Label(filter_frame, text="Type:", font=("Segoe UI", 10), bg="#f8f9fa").pack(side=tk.LEFT, padx=(0, 5))
        type_filter_var = tk.StringVar(value="All")
        type_filter_combo = ttk.Combobox(filter_frame, textvariable=type_filter_var, 
                                        values=["All", "Polo Shirt", "T-Shirt", "Blouse", "Pants", "Skirt", "Dress", "Jacket", "Other"],
                                        width=15, font=("Segoe UI", 10))
        type_filter_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        # Course filter
        tk.Label(filter_frame, text="Course:", font=("Segoe UI", 10), bg="#f8f9fa").pack(side=tk.LEFT, padx=(0, 5))
        course_filter_var = tk.StringVar(value="All")
        course_filter_combo = ttk.Combobox(filter_frame, textvariable=course_filter_var, 
                                          values=["All"] + self.get_unique_courses(),
                                          width=15, font=("Segoe UI", 10))
        course_filter_combo.pack(side=tk.LEFT, padx=(0, 20))
        
        # Apply filters button
        apply_filter_btn = tk.Button(filter_frame, text="Apply Filters", font=("Segoe UI", 10, "bold"),
                                    bg="#007bff", fg="#ffffff", relief="flat", cursor="hand2")
        apply_filter_btn.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # View Annotations button
        view_annotations_btn = tk.Button(filter_frame, text="🔍 View Annotations", font=("Segoe UI", 10, "bold"),
                                        bg="#28a745", fg="#ffffff", relief="flat", cursor="hand2",
                                        command=self.view_uniform_annotations)
        view_annotations_btn.pack(side=tk.RIGHT, padx=(0, 10), pady=10)
        
        # Designs display frame
        designs_frame = tk.Frame(main_frame, bg="#ffffff")
        designs_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create detailed designs tree
        columns = ('ID', 'Name', 'Course', 'Type', 'Colors', 'Status', 'Designer', 'Submitted Date', 'Image')
        designs_tree = ttk.Treeview(designs_frame, columns=columns, show='headings', height=20)
        
        # Define column widths
        column_widths = {
            'ID': 80, 'Name': 150, 'Course': 120, 'Type': 100, 'Colors': 100,
            'Status': 120, 'Designer': 120, 'Submitted Date': 120, 'Image': 80
        }
        
        for col in columns:
            designs_tree.heading(col, text=col)
            designs_tree.column(col, width=column_widths.get(col, 120), minwidth=80)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(designs_frame, orient=tk.VERTICAL, command=designs_tree.yview)
        h_scrollbar = ttk.Scrollbar(designs_frame, orient=tk.HORIZONTAL, command=designs_tree.xview)
        designs_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack tree and scrollbars
        designs_tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        def load_filtered_designs():
            """Load designs with applied filters"""
            # Clear existing items
            for item in designs_tree.get_children():
                designs_tree.delete(item)
            
            # Apply filters
            filtered_designs = []
            for design in self.uniform_designs:
                status_match = status_filter_var.get() == "All" or design.get('status', '') == status_filter_var.get()
                type_match = type_filter_var.get() == "All" or design.get('type', '') == type_filter_var.get()
                course_match = course_filter_var.get() == "All" or design.get('course', '') == course_filter_var.get()
                
                if status_match and type_match and course_match:
                    filtered_designs.append(design)
            
            # Insert filtered designs
            for design in filtered_designs:
                image_status = "📷 Yes" if design.get('has_image') else "❌ No"
                designs_tree.insert('', 'end', values=(
                    design.get('id', ''),
                    design.get('name', ''),
                    design.get('course', ''),
                    design.get('type', ''),
                    design.get('colors', ''),
                    design.get('status', ''),
                    design.get('designer', ''),
                    design.get('submitted_date', ''),
                    image_status
                ))
            
            # Update title with count
            title_label.config(text=f"Browse Uniform Designs ({len(filtered_designs)} designs)")
        
        # Bind apply filters button
        apply_filter_btn.config(command=load_filtered_designs)
        
        # Load initial designs
        load_filtered_designs()
        
        # Bind double-click to view details
        def view_design_details(event):
            selection = designs_tree.selection()
            if selection:
                item = designs_tree.item(selection[0])
                values = item['values']
                design_id = values[0]
                
                # Find the design data
                design_data = None
                for design in self.uniform_designs:
                    if design.get('id') == design_id:
                        design_data = design
                        break
                
                if design_data:
                    self.show_design_details(design_data)
        
        designs_tree.bind('<Double-1>', view_design_details)
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", font=("Segoe UI", 12, "bold"),
                             bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                             command=dialog.destroy)
        close_btn.pack(pady=20)
    
    def show_design_details(self, design_data):
        """Show detailed view of a specific design"""
        # Create details dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Design Details - {design_data.get('name', 'Unknown')}")
        dialog.geometry("600x500")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text=design_data.get('name', 'Unknown Design'), 
                              font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Image display (if exists)
        if design_data.get('has_image') and (design_data.get('image_path') or design_data.get('image_path_local')):
            try:
                from PIL import Image, ImageTk
                # Create image frame
                image_display_frame = tk.Frame(main_frame, bg="#ffffff")
                image_display_frame.pack(fill=tk.X, pady=(0, 20))
                
                # Image label
                tk.Label(image_display_frame, text="Design Image:", font=("Segoe UI", 12, "bold"), 
                        bg="#ffffff").pack(anchor=tk.W, pady=(0, 10))
                
                # Load and display image from local path
                image = None
                path = design_data.get('image_path') or design_data.get('image_path_local')
                if path and os.path.exists(path):
                    try:
                        image = Image.open(path)
                        # Resize to fit display (max 300x300)
                        image.thumbnail((300, 300), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        
                        # Image display label
                        img_label = tk.Label(image_display_frame, image=photo, bg="#f8f9fa", relief="solid", bd=2)
                        img_label.image = photo  # Keep a reference
                        img_label.pack(pady=(0, 10))
                        
                        # Image path info
                        filename = os.path.basename(path)
                        tk.Label(image_display_frame, text=f"Image: {filename}", 
                                font=("Segoe UI", 10), bg="#ffffff", fg="#6c757d").pack()
                    except Exception as e:
                        raise RuntimeError(f"Failed to load image: {str(e)}")
                else:
                    raise RuntimeError("Image file not found")
                
            except Exception as e:
                # Show error if image can't be loaded
                error_label = tk.Label(main_frame, text=f"⚠️ Image could not be loaded: {str(e)}", 
                                     font=("Segoe UI", 10), bg="#ffffff", fg="#dc3545")
                error_label.pack(pady=(0, 20))
        
        # Details frame
        details_frame = tk.Frame(main_frame, bg="#ffffff")
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create details display
        details = [
            ("Course:", design_data.get('course', '')),
            ("Design Type:", design_data.get('type', '')),
            ("Colors:", design_data.get('colors', '')),
            ("Size Range:", design_data.get('size_range', '')),
            ("Status:", design_data.get('status', '')),
            ("Designer:", design_data.get('designer', '')),
            ("Submitted Date:", design_data.get('submitted_date', '')),
            ("Submitted By:", design_data.get('submitted_by_name', '')),
            ("Last Updated:", design_data.get('last_updated', ''))
        ]
        
        for i, (label, value) in enumerate(details):
            row_frame = tk.Frame(details_frame, bg="#ffffff")
            row_frame.pack(fill=tk.X, pady=5)
            
            tk.Label(row_frame, text=label, font=("Segoe UI", 11, "bold"), 
                    bg="#ffffff", width=15, anchor=tk.W).pack(side=tk.LEFT)
            tk.Label(row_frame, text=value, font=("Segoe UI", 11), 
                    bg="#ffffff", anchor=tk.W).pack(side=tk.LEFT, padx=(10, 0))
        
        # Description
        if design_data.get('description'):
            tk.Label(details_frame, text="Description:", font=("Segoe UI", 11, "bold"), 
                    bg="#ffffff", anchor=tk.W).pack(anchor=tk.W, pady=(20, 5))
            desc_text = tk.Text(details_frame, height=4, font=("Segoe UI", 11), wrap=tk.WORD)
            desc_text.pack(fill=tk.X, pady=(0, 10))
            desc_text.insert("1.0", design_data.get('description', ''))
            desc_text.config(state=tk.DISABLED)
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#ffffff")
        buttons_frame.pack(pady=20)
        
        # Annotation button (if annotation exists)
        if design_data.get('annotation_data'):
            annotation_btn = tk.Button(buttons_frame, text="🔍 View Annotation", font=("Segoe UI", 12, "bold"),
                                      bg="#28a745", fg="#ffffff", relief="flat", cursor="hand2",
                                      command=lambda: self.view_design_annotation(design_data))
            annotation_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Close button
        close_btn = tk.Button(buttons_frame, text="Close", font=("Segoe UI", 12, "bold"),
                             bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                             command=dialog.destroy)
        close_btn.pack(side=tk.LEFT)
    
    def view_design_annotation(self, design_data):
        """View detailed annotation and uniqueness analysis for a specific design"""
        if not design_data.get('annotation_data'):
            messagebox.showinfo("No Annotation", "This design has no annotation data.")
            return
        
        # Create annotation details dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Annotation Details - {design_data.get('name', 'Unknown')}")
        dialog.geometry("800x600")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"800x600+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text=f"🔍 Annotation Analysis - {design_data.get('name', 'Unknown')}", 
                              font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        annotation_data = design_data['annotation_data']
        
        # Tab 1: Detection Results
        detection_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(detection_frame, text="🎯 Detection Results")
        
        # Detection results content
        self._create_detection_results_tab(detection_frame, annotation_data)
        
        # Tab 2: Visual Features
        features_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(features_frame, text="🎨 Visual Features")
        
        # Visual features content
        self._create_visual_features_tab(features_frame, annotation_data)
        
        # Tab 3: Uniqueness Analysis
        uniqueness_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(uniqueness_frame, text="🔐 Uniqueness Analysis")
        
        # Uniqueness analysis content
        self._create_uniqueness_tab(uniqueness_frame, design_data)
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", font=("Segoe UI", 12, "bold"),
                             bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                             command=dialog.destroy)
        close_btn.pack(pady=20)
    
    def _create_detection_results_tab(self, parent_frame, annotation_data):
        """Create detection results tab content"""
        # Create scrollable frame
        canvas = tk.Canvas(parent_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header_frame = tk.Frame(scrollable_frame, bg="#f8f9fa", relief="solid", bd=1)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        header_labels = ["Element", "Confidence", "Bounding Box", "Area", "Class ID"]
        for i, label in enumerate(header_labels):
            tk.Label(header_frame, text=label, font=("Segoe UI", 11, "bold"), 
                    bg="#f8f9fa", fg="#1877f2").grid(row=0, column=i, padx=10, pady=10, sticky="ew")
        
        # Configure column weights
        for i in range(len(header_labels)):
            header_frame.grid_columnconfigure(i, weight=1)
        
        # Add detection data
        detections = annotation_data.get('detection_results', {}).get('detections', [])
        row = 1
        for detection in detections:
            # Element name
            class_name = detection.get('class_name', 'Unknown')
            tk.Label(scrollable_frame, text=class_name, font=("Segoe UI", 10), 
                    bg="#ffffff").grid(row=row, column=0, padx=5, pady=5, sticky="w")
            
            # Confidence
            confidence = detection.get('confidence', 0)
            tk.Label(scrollable_frame, text=f"{confidence:.3f}", font=("Segoe UI", 10), 
                    bg="#ffffff").grid(row=row, column=1, padx=5, pady=5, sticky="w")
            
            # Bounding box
            bbox = detection.get('bbox', {})
            bbox_text = f"({bbox.get('x1', 0):.0f}, {bbox.get('y1', 0):.0f}) - ({bbox.get('x2', 0):.0f}, {bbox.get('y2', 0):.0f})"
            tk.Label(scrollable_frame, text=bbox_text, font=("Segoe UI", 10), 
                    bg="#ffffff", fg="#6c757d").grid(row=row, column=2, padx=5, pady=5, sticky="w")
            
            # Area
            area = detection.get('area', 0)
            tk.Label(scrollable_frame, text=f"{area:.0f}", font=("Segoe UI", 10), 
                    bg="#ffffff").grid(row=row, column=3, padx=5, pady=5, sticky="w")
            
            # Class ID
            class_id = detection.get('class_id', 'N/A')
            tk.Label(scrollable_frame, text=str(class_id), font=("Segoe UI", 10), 
                    bg="#ffffff").grid(row=row, column=4, padx=5, pady=5, sticky="w")
            
            row += 1
        
        # Configure grid columns
        for i in range(5):
            scrollable_frame.grid_columnconfigure(i, weight=1)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_visual_features_tab(self, parent_frame, annotation_data):
        """Create visual features tab content"""
        # Create scrollable frame
        canvas = tk.Canvas(parent_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Visual features content
        features = annotation_data.get('visual_features', {})
        
        # Color features
        color_frame = tk.LabelFrame(scrollable_frame, text="🎨 Color Features", font=("Segoe UI", 12, "bold"), 
                                   bg="#ffffff", fg="#1877f2")
        color_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        if 'color_features' in features and not features['color_features'].get('error'):
            color_data = features['color_features']
            
            # Mean colors
            mean_bgr = color_data.get('mean_bgr', [])
            if mean_bgr:
                tk.Label(color_frame, text=f"Mean BGR: ({mean_bgr[0]:.1f}, {mean_bgr[1]:.1f}, {mean_bgr[2]:.1f})", 
                        font=("Segoe UI", 10), bg="#ffffff").pack(anchor=tk.W, padx=10, pady=5)
            
            # Dominant colors
            dominant_colors = color_data.get('dominant_colors', [])
            if dominant_colors:
                tk.Label(color_frame, text="Dominant Colors:", font=("Segoe UI", 10, "bold"), 
                        bg="#ffffff").pack(anchor=tk.W, padx=10, pady=(10, 5))
                for i, color in enumerate(dominant_colors[:3]):  # Show top 3
                    tk.Label(color_frame, text=f"  Color {i+1}: RGB({color[2]}, {color[1]}, {color[0]})", 
                            font=("Segoe UI", 10), bg="#ffffff").pack(anchor=tk.W, padx=20, pady=2)
        
        # Texture features
        texture_frame = tk.LabelFrame(scrollable_frame, text="🧵 Texture Features", font=("Segoe UI", 12, "bold"), 
                                     bg="#ffffff", fg="#1877f2")
        texture_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        if 'texture_features' in features and not features['texture_features'].get('error'):
            texture_data = features['texture_features']
            
            # LBP histogram
            lbp_hist = texture_data.get('lbp_histogram', [])
            if lbp_hist:
                tk.Label(texture_frame, text=f"LBP Histogram: {len(lbp_hist)} bins", 
                        font=("Segoe UI", 10), bg="#ffffff").pack(anchor=tk.W, padx=10, pady=5)
            
            # GLCM properties
            glcm_props = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation']
            for prop in glcm_props:
                values = texture_data.get(f'glcm_{prop}', [])
                if values:
                    avg_value = sum(values) / len(values)
                    tk.Label(texture_frame, text=f"{prop.title()}: {avg_value:.3f}", 
                            font=("Segoe UI", 10), bg="#ffffff").pack(anchor=tk.W, padx=10, pady=2)
        
        # Edge features
        edge_frame = tk.LabelFrame(scrollable_frame, text="📐 Edge Features", font=("Segoe UI", 12, "bold"), 
                                  bg="#ffffff", fg="#1877f2")
        edge_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        if 'edge_features' in features and not features['edge_features'].get('error'):
            edge_data = features['edge_features']
            
            edge_props = ['edge_density', 'gradient_magnitude_mean', 'gradient_magnitude_std']
            for prop in edge_props:
                value = edge_data.get(prop, 0)
                tk.Label(edge_frame, text=f"{prop.replace('_', ' ').title()}: {value:.3f}", 
                        font=("Segoe UI", 10), bg="#ffffff").pack(anchor=tk.W, padx=10, pady=2)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_uniqueness_tab(self, parent_frame, design_data):
        """Create uniqueness analysis tab content"""
        # Create scrollable frame
        canvas = tk.Canvas(parent_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Uniqueness signature
        uniqueness_frame = tk.LabelFrame(scrollable_frame, text="🔐 Uniqueness Signature", font=("Segoe UI", 12, "bold"), 
                                        bg="#ffffff", fg="#1877f2")
        uniqueness_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        signature = design_data.get('uniqueness_signature', 'N/A')
        if signature != 'N/A':
            tk.Label(uniqueness_frame, text=f"Signature: {signature}", font=("Segoe UI", 10), 
                    bg="#ffffff", fg="#6c757d").pack(anchor=tk.W, padx=10, pady=10)
            tk.Label(uniqueness_frame, text="This signature uniquely identifies this uniform design", 
                    font=("Segoe UI", 9), bg="#ffffff", fg="#6c757d").pack(anchor=tk.W, padx=10, pady=(0, 10))
        
        # Similar uniforms
        similar_frame = tk.LabelFrame(scrollable_frame, text="🔗 Similar Uniforms", font=("Segoe UI", 12, "bold"), 
                                     bg="#ffffff", fg="#1877f2")
        similar_frame.pack(fill=tk.X, pady=(0, 20), padx=10)
        
        similar_uniforms = design_data.get('similar_uniforms', [])
        if similar_uniforms:
            tk.Label(similar_frame, text=f"Found {len(similar_uniforms)} similar uniforms:", 
                    font=("Segoe UI", 10, "bold"), bg="#ffffff").pack(anchor=tk.W, padx=10, pady=10)
            
            for similar in similar_uniforms:
                similar_info = tk.Frame(similar_frame, bg="#f8f9fa", relief="solid", bd=1)
                similar_info.pack(fill=tk.X, pady=5, padx=10)
                
                tk.Label(similar_info, text=f"Design: {similar.get('design_name', 'Unknown')}", 
                        font=("Segoe UI", 10, "bold"), bg="#f8f9fa").pack(anchor=tk.W, padx=10, pady=5)
                tk.Label(similar_info, text=f"Similarity Score: {similar.get('similarity_score', 0):.3f}", 
                        font=("Segoe UI", 10), bg="#f8f9fa").pack(anchor=tk.W, padx=20, pady=2)
                
                similarity_details = similar.get('similarity_details', {})
                if similarity_details:
                    tk.Label(similar_info, text=f"Color: {similarity_details.get('color_similarity', 0):.3f}, "
                            f"Texture: {similarity_details.get('texture_similarity', 0):.3f}, "
                            f"Edge: {similarity_details.get('edge_similarity', 0):.3f}", 
                            font=("Segoe UI", 9), bg="#f8f9fa", fg="#6c757d").pack(anchor=tk.W, padx=20, pady=2)
        else:
            tk.Label(similar_frame, text="No similar uniforms found. This design appears to be unique.", 
                    font=("Segoe UI", 10), bg="#ffffff", fg="#28a745").pack(anchor=tk.W, padx=10, pady=10)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_design_context_menu(self, event):
        """Show context menu for uniform designs"""
        # Select the item under the cursor
        item = self.designs_tree.identify_row(event.y)
        if item:
            self.designs_tree.selection_set(item)
            
            # Create context menu
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="🖊️ Edit Design", command=lambda: self.edit_design(event))
            context_menu.add_command(label="👁️ View Details", command=lambda: self.view_design_details(event))
            context_menu.add_separator()
            context_menu.add_command(label="📋 Duplicate Design", command=lambda: self.duplicate_design(event))
            context_menu.add_separator()
            context_menu.add_command(label="🗑️ Delete Design", command=lambda: self.delete_design(event))
            
            # Show context menu
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def edit_design(self, event):
        """Edit uniform design with comprehensive form"""
        selection = self.designs_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a design to edit.")
            return
            
        # Get selected design
        item = self.designs_tree.item(selection[0])
        values = item['values']
        design_id = values[0]
        
        # Find the design data
        design_data = None
        for design in self.uniform_designs:
            if design.get('id') == design_id:
                design_data = design
                break
        
        if not design_data:
            messagebox.showerror("Error", "Design data not found.")
            return
        
        # Create edit dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Edit Design - {design_data.get('name', 'Unknown')}")
        dialog.geometry("700x800")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (800 // 2)
        dialog.geometry(f"700x800+{x}+{y}")
        
        # Main form frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text=f"Edit Design - {design_data.get('name', 'Unknown')}", 
                              font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Create scrollable frame for form
        canvas = tk.Canvas(main_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields frame
        form_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Design Name
        tk.Label(form_frame, text="Design Name:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        design_name_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        design_name_entry.pack(fill=tk.X, pady=(0, 15))
        design_name_entry.insert(0, design_data.get('name', ''))
        
        # Course
        tk.Label(form_frame, text="Course:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        course_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        course_entry.pack(fill=tk.X, pady=(0, 15))
        course_entry.insert(0, design_data.get('course', ''))
        
        # Design Type
        tk.Label(form_frame, text="Design Type:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        design_types = ["Polo Shirt", "T-Shirt", "Blouse", "Pants", "Skirt", "Dress", "Jacket", "Other"]
        design_type_var = tk.StringVar(value=design_data.get('type', design_types[0]))
        design_type_combo = ttk.Combobox(form_frame, textvariable=design_type_var, 
                                        values=design_types, font=("Segoe UI", 12))
        design_type_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Colors
        tk.Label(form_frame, text="Colors:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        colors_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        colors_entry.pack(fill=tk.X, pady=(0, 15))
        colors_entry.insert(0, design_data.get('colors', ''))
        
        # Size Range
        tk.Label(form_frame, text="Size Range:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        size_range_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        size_range_entry.pack(fill=tk.X, pady=(0, 15))
        size_range_entry.insert(0, design_data.get('size_range', ''))
        
        # Description
        tk.Label(form_frame, text="Description:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(20, 5))
        description_text = tk.Text(form_frame, height=4, font=("Segoe UI", 12), wrap=tk.WORD)
        description_text.pack(fill=tk.X, pady=(0, 15))
        description_text.insert("1.0", design_data.get('description', ''))
        
        # Status
        tk.Label(form_frame, text="Status:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        status_types = ["Under Review", "Approved", "Rejected", "In Production", "Discontinued"]
        status_var = tk.StringVar(value=design_data.get('status', status_types[0]))
        status_combo = ttk.Combobox(form_frame, textvariable=status_var, 
                                   values=status_types, font=("Segoe UI", 12))
        status_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Designer/Submitter
        tk.Label(form_frame, text="Designer/Submitter:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        designer_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        designer_entry.pack(fill=tk.X, pady=(0, 15))
        designer_entry.insert(0, design_data.get('designer', ''))
        
        def save_changes():
            """Save changes to the design"""
            try:
                # Update design data
                updated_design = {
                    **design_data,  # Keep existing data
                    'name': design_name_entry.get().strip(),
                    'course': course_entry.get().strip(),
                    'type': design_type_var.get(),
                    'colors': colors_entry.get().strip(),
                    'size_range': size_range_entry.get().strip(),
                    'description': description_text.get("1.0", tk.END).strip(),
                    'status': status_var.get(),
                    'designer': designer_entry.get().strip(),
                    'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_by': self.user_data['username']
                }
                
                # Validate required fields
                if not all([updated_design['name'], updated_design['course'], 
                           updated_design['type'], updated_design['colors']]):
                    messagebox.showerror("Error", "Please fill in all required fields (Name, Course, Type, Colors).")
                    return
                
                # Update in Firebase
                if design_data.get('id'):
                    update_in_firebase('uniform_designs', design_data['id'], updated_design)
                    print(f"✅ Design updated in Firebase: {design_data['id']}")
                
                # Update local data
                for i, design in enumerate(self.uniform_designs):
                    if design.get('id') == design_data['id']:
                        self.uniform_designs[i] = updated_design
                        break
                
                # Refresh data and UI
                self.load_designs_data()
                self.update_course_filter_options()
                
                messagebox.showinfo("Success", "Design updated successfully!")
                dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update design: {str(e)}")
        
        # Buttons frame
        button_frame = tk.Frame(form_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, pady=20)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", font=("Segoe UI", 12), 
                              bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                              command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save button
        save_btn = tk.Button(button_frame, text="Save Changes", font=("Segoe UI", 12, "bold"), 
                            bg="#28a745", fg="#ffffff", relief="flat", cursor="hand2",
                            command=save_changes)
        save_btn.pack(side=tk.RIGHT)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Set focus to first field
        design_name_entry.focus()
    
    def delete_design(self, event=None):
        """Delete uniform design(s) with confirmation"""
        try:
            print(f"🔍 Delete function called")
            
            # Get current selection
            selection = self.designs_tree.selection()
            print(f"🔍 Current selection: {selection}")
            
            # Validate selection
            if not selection:
                print("🔍 No selection found")
                if event is None or not hasattr(event, 'y'):
                    messagebox.showwarning("Warning", "Please select one or more designs to delete.")
                return
            
            # Process selections and find corresponding design data
            selected_designs = []
            for item_id in selection:
                try:
                    item = self.designs_tree.item(item_id)
                    values = item['values']
                    design_id = values[0]
                    design_name = values[1]
                    print(f"🔍 Processing design: ID={design_id}, Name={design_name}")
                    
                    # Find the design data
                    for i, design in enumerate(self.uniform_designs):
                        if design.get('id') == design_id:
                            selected_designs.append((design, i, design_name))
                            print(f"🔍 Found design at index {i}")
                            break
                            
                except Exception as e:
                    print(f"🔍 Error processing selection item {item_id}: {e}")
                    continue
            
            print(f"🔍 Total valid selected designs: {len(selected_designs)}")
            
            if not selected_designs:
                messagebox.showerror("Error", "Selected designs not found. Please refresh and try again.")
                return
            
            # Show confirmation dialog
            self._show_delete_confirmation_dialog(selected_designs)
            
        except Exception as e:
            print(f"❌ Error in delete_design: {e}")
            messagebox.showerror("Error", f"An error occurred while preparing to delete: {str(e)}")
    
    def _show_delete_confirmation_dialog(self, selected_designs):
        """Show the delete confirmation dialog"""
        try:
            is_multiple = len(selected_designs) > 1
            
            # Simple confirmation using messagebox first
            design_names = [design[2] for design in selected_designs]
            if is_multiple:
                message = f"Are you sure you want to delete {len(selected_designs)} designs?\n\n" + "\n".join([f"• {name}" for name in design_names[:5]])
                if len(design_names) > 5:
                    message += f"\n... and {len(design_names) - 5} more"
            else:
                message = f"Are you sure you want to delete '{design_names[0]}'?"
            
            message += "\n\n⚠️ This action cannot be undone!"
            
            result = messagebox.askyesno("Confirm Delete", message)
            
            if result:
                self._perform_delete(selected_designs)
                
        except Exception as e:
            print(f"❌ Error in _show_delete_confirmation_dialog: {e}")
            messagebox.showerror("Error", f"Failed to show delete confirmation: {str(e)}")
    
    def _perform_delete(self, selected_designs):
        """Actually perform the delete operation"""
        try:
            deleted_count = 0
            failed_count = 0
            
            print(f"🔍 Starting deletion of {len(selected_designs)} designs")
            
            # Sort by index in reverse order to avoid index shifting issues
            selected_designs.sort(key=lambda x: x[1], reverse=True)
            print(f"🔍 Sorted indices: {[x[1] for x in selected_designs]}")
            
            for design_data, design_index, design_name in selected_designs:
                try:
                    print(f"🔍 Deleting design: {design_name} (ID: {design_data.get('id')}) at index {design_index}")
                    
                    # Delete from Firebase
                    if design_data.get('id'):
                        print(f"🔍 Calling delete_from_firebase for ID: {design_data['id']}")
                        result = delete_from_firebase('uniform_designs', design_data['id'])
                        print(f"🔍 Firebase delete result: {result}")
                        if result:
                            print(f"✅ Design deleted from Firebase: {design_data['id']}")
                        else:
                            print(f"❌ Firebase delete failed for: {design_data['id']}")
                    
                    # Remove from local data
                    if design_index is not None and design_index < len(self.uniform_designs):
                        print(f"🔍 Removing from local data at index {design_index}")
                        removed_design = self.uniform_designs.pop(design_index)
                        print(f"🔍 Removed design: {removed_design.get('name', 'Unknown')}")
                    
                    deleted_count += 1
                    print(f"🔍 Successfully processed design: {design_name}")
                    
                except Exception as e:
                    print(f"❌ Failed to delete design {design_name}: {e}")
                    failed_count += 1
            
            print(f"🔍 Deletion complete. Deleted: {deleted_count}, Failed: {failed_count}")
            
            # Refresh data and UI
            print("🔍 Refreshing data and UI")
            self.load_designs_data()
            self.update_course_filter_options()
            
            # Show result message
            if len(selected_designs) > 1:
                if failed_count == 0:
                    messagebox.showinfo("Success", f"All {deleted_count} designs have been deleted successfully.")
                else:
                    messagebox.showwarning("Partial Success", f"{deleted_count} designs deleted successfully.\n{failed_count} designs failed to delete.")
            else:
                if deleted_count > 0:
                    messagebox.showinfo("Success", f"Design '{selected_designs[0][2]}' has been deleted successfully.")
                else:
                    messagebox.showerror("Error", "Failed to delete the design.")
                    
        except Exception as e:
            print(f"❌ Error in _perform_delete: {e}")
            messagebox.showerror("Error", f"Failed to delete design(s): {str(e)}")
    
    def view_design_details(self, event):
        """View design details (uses existing show_design_details method)"""
        selection = self.designs_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a design to view.")
            return
            
        # Get selected design
        item = self.designs_tree.item(selection[0])
        values = item['values']
        design_id = values[0]
        
        # Find the design data
        design_data = None
        for design in self.uniform_designs:
            if design.get('id') == design_id:
                design_data = design
                break
        
        if design_data:
            self.show_design_details(design_data)
        else:
            messagebox.showerror("Error", "Design data not found.")
    
    def duplicate_design(self, event):
        """Duplicate uniform design"""
        selection = self.designs_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a design to duplicate.")
            return
            
        # Get selected design
        item = self.designs_tree.item(selection[0])
        values = item['values']
        design_id = values[0]
        
        # Find the design data
        design_data = None
        for design in self.uniform_designs:
            if design.get('id') == design_id:
                design_data = design
                break
        
        if not design_data:
            messagebox.showerror("Error", "Design data not found.")
            return
        
        try:
            # Create duplicate with modified name
            duplicate_design = {
                **design_data,  # Copy all existing data
                'name': f"{design_data.get('name', '')} (Copy)",
                'status': 'Under Review',  # Reset status
                'submitted_date': datetime.now().strftime("%Y-%m-%d"),
                'submitted_by': self.user_data['username'],
                'submitted_by_name': self.user_data['full_name'],
                'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Remove ID so Firebase creates a new one
            if 'id' in duplicate_design:
                del duplicate_design['id']
            
            # Save to Firebase
            doc_id = add_to_firebase('uniform_designs', duplicate_design)
            if doc_id:
                duplicate_design['id'] = doc_id
                self.uniform_designs.append(duplicate_design)
                
                # Refresh data and UI
                self.load_designs_data()
                self.update_course_filter_options()
                
                messagebox.showinfo("Success", f"Design duplicated successfully!\nNew Design ID: {doc_id}")
            else:
                messagebox.showerror("Error", "Failed to save duplicate design to Firebase.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to duplicate design: {str(e)}")
    
    def get_unique_courses(self):
        """Get list of unique courses from designs"""
        try:
            courses = set()
            for design in self.uniform_designs:
                if design.get('course'):
                    courses.add(design.get('course'))
            return sorted(list(courses))
        except Exception as e:
            print(f"Error getting unique courses: {e}")
            return []
    
    def update_course_filter_options(self):
        """Update the course filter dropdown with available courses"""
        try:
            # Get unique courses from designs
            course_list = self.get_unique_courses()
            
            # Update combobox values
            self.course_filter_combo['values'] = ['All Courses'] + course_list
            
        except Exception as e:
            print(f"Error updating course filter options: {e}")
    
    def apply_course_filter(self):
        """Apply course filter to the designs table"""
        try:
            selected_course = self.course_filter_var.get()
            
            if selected_course == "All Courses":
                # Show all designs
                self.load_designs_data()
            else:
                # Filter designs by selected course
                filtered_designs = [design for design in self.uniform_designs 
                                  if design.get('course') == selected_course]
                
                # Clear existing items
                for item in self.designs_tree.get_children():
                    self.designs_tree.delete(item)
                
                # Insert filtered designs data
                for design in filtered_designs:
                    image_status = "📷 Yes" if design.get('has_image') else "❌ No"
                    self.designs_tree.insert('', 'end', values=(
                        design.get('id', ''),
                        design.get('name', ''),
                        design.get('course', ''),
                        design.get('type', ''),
                        design.get('colors', ''),
                        design.get('status', ''),
                        design.get('designer', ''),
                        design.get('submitted_date', ''),
                        image_status
                    ))
                
                # Update status
                print(f"✅ Filtered designs by course: {selected_course} ({len(filtered_designs)} designs)")
                
        except Exception as e:
            print(f"Error applying course filter: {e}")
            messagebox.showerror("Filter Error", f"Failed to apply filter: {str(e)}")
    
    def create_course_statistics(self, parent):
        """Create course statistics display"""
        try:
            # Get course statistics
            course_stats = {}
            for design in self.uniform_designs:
                course = design.get('course', 'Unknown Course')
                if course not in course_stats:
                    course_stats[course] = {'total': 0, 'approved': 0, 'pending': 0}
                
                course_stats[course]['total'] += 1
                status = design.get('status', 'Unknown')
                if status == 'Approved':
                    course_stats[course]['approved'] += 1
                elif status in ['Under Review', 'Pending']:
                    course_stats[course]['pending'] += 1
            
            # Create statistics display
            stats_container = tk.Frame(parent, bg="#e9ecef")
            stats_container.pack(fill=tk.X, padx=20, pady=(0, 10))
            
            # Create course stat boxes
            for i, (course, stats) in enumerate(course_stats.items()):
                if i > 0 and i % 3 == 0:  # New row every 3 courses
                    stats_container = tk.Frame(parent, bg="#e9ecef")
                    stats_container.pack(fill=tk.X, padx=20, pady=(0, 10))
                
                # Course stat box
                stat_box = tk.Frame(stats_container, bg="#ffffff", relief="solid", bd=1)
                stat_box.pack(side=tk.LEFT, padx=(0, 10), pady=5, fill=tk.X, expand=True)
                
                # Course name
                tk.Label(stat_box, text=course, font=("Segoe UI", 10, "bold"), 
                        bg="#ffffff", fg="#1877f2").pack(pady=(8, 5))
                
                # Statistics
                tk.Label(stat_box, text=f"Total: {stats['total']}", 
                        font=("Segoe UI", 9), bg="#ffffff").pack()
                tk.Label(stat_box, text=f"Approved: {stats['approved']}", 
                        font=("Segoe UI", 9), bg="#28a745").pack()
                tk.Label(stat_box, text=f"Pending: {stats['pending']}", 
                        font=("Segoe UI", 9), bg="#ffc107").pack()
                
        except Exception as e:
            print(f"Error creating course statistics: {e}")
    
    def export_designs_by_course(self):
        """Export designs organized by course with enhanced file management"""
        try:
            from tkinter import filedialog
            import csv
            import os
            from datetime import datetime
            
            # Create a directory for course exports if it doesn't exist
            export_dir = "course_exports"
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
            
            # Ask user for save location (default to course_exports directory)
            filename = filedialog.asksaveasfilename(
                title="Export Designs by Course",
                initialdir=export_dir,
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            # Organize designs by course
            course_designs = {}
            for design in self.uniform_designs:
                course = design.get('course', 'Unknown Course')
                if course not in course_designs:
                    course_designs[course] = []
                course_designs[course].append(design)
            
            # Write to CSV with enhanced information
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Course', 'Design ID', 'Name', 'Type', 'Colors', 'Size Range', 
                             'Status', 'Designer', 'Submitted Date', 'Description', 'Image Status', 'Last Updated']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for course, designs in course_designs.items():
                    # Add course header row
                    writer.writerow({
                        'Course': f"=== {course.upper()} ===",
                        'Design ID': f"Total Designs: {len(designs)}",
                        'Name': '',
                        'Type': '',
                        'Colors': '',
                        'Size Range': '',
                        'Status': '',
                        'Designer': '',
                        'Submitted Date': '',
                        'Description': '',
                        'Image Status': '',
                        'Last Updated': ''
                    })
                    
                    # Add designs for this course
                    for design in designs:
                        image_status = "Yes" if design.get('has_image') else "No"
                        writer.writerow({
                            'Course': course,
                            'Design ID': design.get('id', ''),
                            'Name': design.get('name', ''),
                            'Type': design.get('type', ''),
                            'Colors': design.get('colors', ''),
                            'Size Range': design.get('size_range', ''),
                            'Status': design.get('status', ''),
                            'Designer': design.get('designer', ''),
                            'Submitted Date': design.get('submitted_date', ''),
                            'Description': design.get('description', ''),
                            'Image Status': image_status,
                            'Last Updated': design.get('last_updated', '')
                        })
                    
                    # Add separator row
                    writer.writerow({
                        'Course': '',
                        'Design ID': '',
                        'Name': '',
                        'Type': '',
                        'Colors': '',
                        'Size Range': '',
                        'Status': '',
                        'Designer': '',
                        'Submitted Date': '',
                        'Description': '',
                        'Image Status': '',
                        'Last Updated': ''
                    })
            
            # Also create a summary report
            summary_filename = os.path.join(export_dir, f"course_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(summary_filename, 'w', encoding='utf-8') as summary_file:
                summary_file.write("UNIFORM DESIGNS BY COURSE - SUMMARY REPORT\n")
                summary_file.write("=" * 50 + "\n\n")
                summary_file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                summary_file.write(f"Total Designs: {len(self.uniform_designs)}\n")
                summary_file.write(f"Total Courses: {len(course_designs)}\n\n")
                
                for course, designs in course_designs.items():
                    summary_file.write(f"COURSE: {course}\n")
                    summary_file.write("-" * 30 + "\n")
                    summary_file.write(f"Total Designs: {len(designs)}\n")
                    
                    # Count by status
                    status_counts = {}
                    for design in designs:
                        status = design.get('status', 'Unknown')
                        status_counts[status] = status_counts.get(status, 0) + 1
                    
                    for status, count in status_counts.items():
                        summary_file.write(f"  {status}: {count}\n")
                    
                    summary_file.write("\n")
            
            messagebox.showinfo("Export Success", 
                              f"Designs exported successfully!\n\n"
                              f"Main File: {filename}\n"
                              f"Summary Report: {summary_filename}\n\n"
                              f"Total designs: {len(self.uniform_designs)}\n"
                              f"Courses: {len(course_designs)}")
            
        except Exception as e:
            print(f"Error exporting designs: {e}")
            messagebox.showerror("Export Error", f"Failed to export designs: {str(e)}")
    
    def manage_course_files(self):
        """Manage uniform design files by course with enhanced functionality"""
        try:
            # Create course management dialog
            dialog = tk.Toplevel(self.root)
            dialog.title("Course Files Management")
            dialog.geometry("1000x700")
            dialog.configure(bg="#ffffff")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (1000 // 2)
            y = (dialog.winfo_screenheight() // 2) - (700 // 2)
            dialog.geometry(f"1000x700+{x}+{y}")
            
            # Main frame
            main_frame = tk.Frame(dialog, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text="Course Files Management", 
                                  font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Create notebook for different views
            notebook = ttk.Notebook(main_frame)
            notebook.pack(fill=tk.BOTH, expand=True)
            
            # Tab 1: Course Overview
            overview_frame = ttk.Frame(notebook)
            notebook.add(overview_frame, text="Course Overview")
            self.create_course_overview_tab(overview_frame)
            
            # Tab 2: Add New Design to Course
            add_design_frame = ttk.Frame(notebook)
            notebook.add(add_design_frame, text="Add Design to Course")
            self.create_add_design_to_course_tab(add_design_frame)
            
            # Tab 3: View Course Files
            view_files_frame = ttk.Frame(notebook)
            notebook.add(view_files_frame, text="View Course Files")
            self.create_view_course_files_tab(view_files_frame)
            
            # Close button
            close_btn = tk.Button(main_frame, text="Close", font=("Segoe UI", 12, "bold"),
                                 bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                                 command=dialog.destroy)
            close_btn.pack(pady=20)
            
        except Exception as e:
            print(f"Error creating course management dialog: {e}")
            messagebox.showerror("Error", f"Failed to create course management dialog: {str(e)}")
    
    def create_course_overview_tab(self, parent):
        """Create the course overview tab"""
        try:
            # Get course statistics
            course_stats = {}
            for design in self.uniform_designs:
                course = design.get('course', 'Unknown Course')
                if course not in course_stats:
                    course_stats[course] = {
                        'total': 0, 'approved': 0, 'pending': 0, 'rejected': 0,
                        'latest_design': None, 'oldest_design': None
                    }
                
                course_stats[course]['total'] += 1
                status = design.get('status', 'Unknown')
                if status == 'Approved':
                    course_stats[course]['approved'] += 1
                elif status in ['Under Review', 'Pending']:
                    course_stats[course]['pending'] += 1
                elif status == 'Rejected':
                    course_stats[course]['rejected'] += 1
                
                # Track latest and oldest designs
                submitted_date = design.get('submitted_date', '')
                if submitted_date:
                    try:
                        date_obj = datetime.strptime(submitted_date, "%Y-%m-%d")
                        if (course_stats[course]['latest_design'] is None or 
                            date_obj > course_stats[course]['latest_design']):
                            course_stats[course]['latest_design'] = date_obj
                        if (course_stats[course]['oldest_design'] is None or 
                            date_obj < course_stats[course]['oldest_design']):
                            course_stats[course]['oldest_design'] = date_obj
                    except:
                        pass
            
            # Create overview display
            overview_frame = tk.Frame(parent, bg="#f8f9fa")
            overview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # Create scrollable frame
            canvas = tk.Canvas(overview_frame, bg="#f8f9fa")
            scrollbar = ttk.Scrollbar(overview_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#f8f9fa")
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Display course statistics
            for i, (course, stats) in enumerate(course_stats.items()):
                # Course header
                course_header = tk.Frame(scrollable_frame, bg="#ffffff", relief="solid", bd=1)
                course_header.pack(fill=tk.X, pady=(0, 10), padx=10)
                
                # Course name
                tk.Label(course_header, text=course, font=("Segoe UI", 14, "bold"), 
                        bg="#ffffff", fg="#1877f2").pack(anchor=tk.W, padx=15, pady=(10, 5))
                
                # Statistics row
                stats_row = tk.Frame(course_header, bg="#ffffff")
                stats_row.pack(fill=tk.X, padx=15, pady=(0, 10))
                
                # Total designs
                tk.Label(stats_row, text=f"Total: {stats['total']}", 
                        font=("Segoe UI", 11, "bold"), bg="#ffffff", fg="#495057").pack(side=tk.LEFT, padx=(0, 20))
                
                # Status breakdown
                tk.Label(stats_row, text=f"Approved: {stats['approved']}", 
                        font=("Segoe UI", 11), bg="#28a745", fg="#ffffff").pack(side=tk.LEFT, padx=(0, 15))
                tk.Label(stats_row, text=f"Pending: {stats['pending']}", 
                        font=("Segoe UI", 11), bg="#ffc107", fg="#000000").pack(side=tk.LEFT, padx=(0, 15))
                tk.Label(stats_row, text=f"Rejected: {stats['rejected']}", 
                        font=("Segoe UI", 11), bg="#dc3545", fg="#ffffff").pack(side=tk.LEFT, padx=(0, 15))
                
                # Date range
                if stats['latest_design'] and stats['oldest_design']:
                    date_range = f"Date Range: {stats['oldest_design'].strftime('%Y-%m-%d')} to {stats['latest_design'].strftime('%Y-%m-%d')}"
                    tk.Label(stats_row, text=date_range, font=("Segoe UI", 10), 
                            bg="#ffffff", fg="#6c757d").pack(side=tk.RIGHT)
            
            # Pack canvas and scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
        except Exception as e:
            print(f"Error creating course overview tab: {e}")
            tk.Label(parent, text=f"Error loading course overview: {str(e)}", 
                    font=("Segoe UI", 12), bg="#ffffff", fg="#dc3545").pack(pady=50)
    
    def create_add_design_to_course_tab(self, parent):
        """Create the add design to course tab"""
        try:
            # Main frame
            main_frame = tk.Frame(parent, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text="Add New Design to Existing Course", 
                                  font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Course selection
            course_frame = tk.Frame(main_frame, bg="#ffffff")
            course_frame.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(course_frame, text="Select Course:", font=("Segoe UI", 12, "bold"), 
                    bg="#ffffff").pack(side=tk.LEFT, padx=(0, 10))
            
            # Get unique courses
            courses = self.get_unique_courses()
            if not courses:
                tk.Label(course_frame, text="No courses available. Please add designs first.", 
                        font=("Segoe UI", 11), bg="#ffffff", fg="#6c757d").pack(side=tk.LEFT)
                return
            
            course_var = tk.StringVar(value=courses[0])
            course_combo = ttk.Combobox(course_frame, textvariable=course_var, 
                                       values=courses, font=("Segoe UI", 12), width=30)
            course_combo.pack(side=tk.LEFT, padx=(0, 20))
            
            # Show existing designs for selected course
            existing_designs_frame = tk.LabelFrame(main_frame, text="Existing Designs in Selected Course", 
                                                 font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            existing_designs_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            
            # Create treeview for existing designs
            columns = ('ID', 'Name', 'Type', 'Colors', 'Status', 'Designer', 'Submitted Date')
            existing_tree = ttk.Treeview(existing_designs_frame, columns=columns, show='headings', height=8)
            
            # Define column widths
            column_widths = {
                'ID': 80, 'Name': 150, 'Type': 100, 'Colors': 100,
                'Status': 120, 'Designer': 120, 'Submitted Date': 120
            }
            
            for col in columns:
                existing_tree.heading(col, text=col)
                existing_tree.column(col, width=column_widths.get(col, 120), minwidth=80)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(existing_designs_frame, orient=tk.VERTICAL, command=existing_tree.yview)
            existing_tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack tree and scrollbar
            existing_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
            
            def load_course_designs():
                """Load designs for selected course"""
                selected_course = course_var.get()
                
                # Clear existing items
                for item in existing_tree.get_children():
                    existing_tree.delete(item)
                
                # Load designs for selected course
                course_designs = [design for design in self.uniform_designs 
                                if design.get('course') == selected_course]
                
                for design in course_designs:
                    existing_tree.insert('', 'end', values=(
                        design.get('id', ''),
                        design.get('name', ''),
                        design.get('type', ''),
                        design.get('colors', ''),
                        design.get('status', ''),
                        design.get('designer', ''),
                        design.get('submitted_date', '')
                    ))
                
                # Update title
                existing_designs_frame.config(text=f"Existing Designs in {selected_course} ({len(course_designs)} designs)")
            
            # Bind course selection change
            course_combo.bind('<<ComboboxSelected>>', lambda e: load_course_designs())
            
            # Load initial designs
            load_course_designs()
            
            # Add new design button
            add_btn = tk.Button(main_frame, text="➕ Add New Design to This Course", 
                               font=("Segoe UI", 12, "bold"), bg="#28a745", fg="#ffffff",
                               relief="flat", cursor="hand2", command=lambda: self.add_design_to_specific_course(course_var.get()))
            add_btn.pack(pady=20)
            
        except Exception as e:
            print(f"Error creating add design to course tab: {e}")
            tk.Label(parent, text=f"Error loading add design tab: {str(e)}", 
                    font=("Segoe UI", 12), bg="#ffffff", fg="#dc3545").pack(pady=50)
    
    def create_view_course_files_tab(self, parent):
        """Create the view course files tab"""
        try:
            # Main frame
            main_frame = tk.Frame(parent, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text="View Course Files", 
                                  font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Course selection
            course_frame = tk.Frame(main_frame, bg="#ffffff")
            course_frame.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(course_frame, text="Select Course:", font=("Segoe UI", 12, "bold"), 
                    bg="#ffffff").pack(side=tk.LEFT, padx=(0, 10))
            
            # Get unique courses
            courses = self.get_unique_courses()
            if not courses:
                tk.Label(course_frame, text="No courses available.", 
                        font=("Segoe UI", 11), bg="#ffffff", fg="#6c757d").pack(side=tk.LEFT)
                return
            
            course_var = tk.StringVar(value=courses[0])
            course_combo = ttk.Combobox(course_frame, textvariable=course_var, 
                                       values=courses, font=("Segoe UI", 12), width=30)
            course_combo.pack(side=tk.LEFT, padx=(0, 20))
            
            # View button
            view_btn = tk.Button(course_frame, text="View Course File", 
                                font=("Segoe UI", 11, "bold"), bg="#007bff", fg="#ffffff",
                                relief="flat", cursor="hand2", command=lambda: self.view_course_file(course_var.get()))
            view_btn.pack(side=tk.LEFT, padx=(0, 20))
            
            # Export button
            export_btn = tk.Button(course_frame, text="Export Course File", 
                                  font=("Segoe UI", 11, "bold"), bg="#6f42c1", fg="#ffffff",
                                  relief="flat", cursor="hand2", command=lambda: self.export_single_course(course_var.get()))
            export_btn.pack(side=tk.LEFT)
            
            # Course file display
            file_display_frame = tk.LabelFrame(main_frame, text="Course File Contents", 
                                             font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            file_display_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            
            # Create text widget for file display
            file_text = tk.Text(file_display_frame, font=("Consolas", 10), wrap=tk.WORD, bg="#f8f9fa")
            file_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            def load_course_file():
                """Load and display course file contents"""
                selected_course = course_var.get()
                
                # Clear text widget
                file_text.delete("1.0", tk.END)
                
                # Get designs for selected course
                course_designs = [design for design in self.uniform_designs 
                                if design.get('course') == selected_course]
                
                if not course_designs:
                    file_text.insert(tk.END, f"No designs found for {selected_course}")
                    return
                
                # Format course file content
                content = f"COURSE: {selected_course.upper()}\n"
                content += "=" * 50 + "\n\n"
                content += f"Total Designs: {len(course_designs)}\n"
                content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                
                # Group by status
                status_groups = {}
                for design in course_designs:
                    status = design.get('status', 'Unknown')
                    if status not in status_groups:
                        status_groups[status] = []
                    status_groups[status].append(design)
                
                for status, designs in status_groups.items():
                    content += f"\n{status.upper()} DESIGNS ({len(designs)}):\n"
                    content += "-" * 30 + "\n"
                    
                    for design in designs:
                        content += f"\nDesign ID: {design.get('id', 'N/A')}\n"
                        content += f"Name: {design.get('name', 'N/A')}\n"
                        content += f"Type: {design.get('type', 'N/A')}\n"
                        content += f"Colors: {design.get('colors', 'N/A')}\n"
                        content += f"Size Range: {design.get('size_range', 'N/A')}\n"
                        content += f"Designer: {design.get('designer', 'N/A')}\n"
                        content += f"Submitted: {design.get('submitted_date', 'N/A')}\n"
                        content += f"Image: {'Yes' if design.get('has_image') else 'No'}\n"
                        
                        if design.get('description'):
                            content += f"Description: {design.get('description', '')}\n"
                        
                        content += "-" * 20 + "\n"
                
                file_text.insert(tk.END, content)
            
            # Bind course selection change
            course_combo.bind('<<ComboboxSelected>>', lambda e: load_course_file())
            
            # Load initial course file
            load_course_file()
            
        except Exception as e:
            print(f"Error creating view course files tab: {e}")
            tk.Label(parent, text=f"Error loading view course files tab: {str(e)}", 
                    font=("Segoe UI", 12), bg="#ffffff", fg="#dc3545").pack(pady=50)
    
    def add_design_to_specific_course(self, course_name):
        """Add a new design to a specific course"""
        try:
            # Create a simplified form for adding design to specific course
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Add Design to {course_name}")
            dialog.geometry("600x700")
            dialog.configure(bg="#ffffff")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
            y = (dialog.winfo_screenheight() // 2) - (700 // 2)
            dialog.geometry(f"600x700+{x}+{y}")
            
            # Main frame
            main_frame = tk.Frame(dialog, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text=f"Add New Design to {course_name}", 
                                  font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Course info
            course_info = tk.Label(main_frame, text=f"Course: {course_name}", 
                                 font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#495057")
            course_info.pack(pady=(0, 20))
            
            # Form fields
            # Design Name
            tk.Label(main_frame, text="Design Name:", font=("Segoe UI", 12, "bold"), 
                    bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
            design_name_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=50)
            design_name_entry.pack(fill=tk.X, pady=(0, 15))
            
            # Design Type
            tk.Label(main_frame, text="Design Type:", font=("Segoe UI", 12, "bold"), 
                    bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
            design_types = ["Polo Shirt", "T-Shirt", "Blouse", "Pants", "Skirt", "Dress", "Jacket", "Other"]
            design_type_var = tk.StringVar(value=design_types[0])
            design_type_combo = ttk.Combobox(main_frame, textvariable=design_type_var, 
                                            values=design_types, font=("Segoe UI", 12))
            design_type_combo.pack(fill=tk.X, pady=(0, 15))
            
            # Colors
            tk.Label(main_frame, text="Colors:", font=("Segoe UI", 12, "bold"), 
                    bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
            colors_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=50)
            colors_entry.pack(fill=tk.X, pady=(0, 15))
            
            # Size Range
            tk.Label(main_frame, text="Size Range:", font=("Segoe UI", 12, "bold"), 
                    bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
            size_range_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=50)
            size_range_entry.pack(fill=tk.X, pady=(0, 15))
            
            # Description
            tk.Label(main_frame, text="Description:", font=("Segoe UI", 12, "bold"), 
                    bg="#ffffff").pack(anchor=tk.W, pady=(20, 5))
            description_text = tk.Text(main_frame, height=4, font=("Segoe UI", 12), wrap=tk.WORD)
            description_text.pack(fill=tk.X, pady=(0, 15))
            
            # Status
            tk.Label(main_frame, text="Status:", font=("Segoe UI", 12, "bold"), 
                    bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
            status_types = ["Under Review", "Approved", "Rejected", "In Production", "Discontinued"]
            status_var = tk.StringVar(value=status_types[0])
            status_combo = ttk.Combobox(main_frame, textvariable=status_var, 
                                       values=status_types, font=("Segoe UI", 12))
            status_combo.pack(fill=tk.X, pady=(0, 15))
            
            # Designer/Submitter
            tk.Label(main_frame, text="Designer/Submitter:", font=("Segoe UI", 12, "bold"), 
                    bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
            designer_entry = tk.Entry(main_frame, font=("Segoe UI", 12), width=50)
            designer_entry.pack(fill=tk.X, pady=(0, 15))
            
            def save_design():
                """Save design to specific course"""
                try:
                    # Get form data
                    design_data = {
                        'name': design_name_entry.get().strip(),
                        'course': course_name,  # Use the selected course
                        'type': design_type_var.get(),
                        'colors': colors_entry.get().strip(),
                        'size_range': size_range_entry.get().strip(),
                        'description': description_text.get("1.0", tk.END).strip(),
                        'status': status_var.get(),
                        'designer': designer_entry.get().strip(),
                        'submitted_date': datetime.now().strftime("%Y-%m-%d"),
                        'submitted_by': self.user_data['username'],
                        'submitted_by_name': self.user_data['full_name'],
                        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'has_image': False,
                        'image_url': None,
                        'image_storage_path': None,
                    }
                    
                    # Validate required fields
                    if not all([design_data['name'], design_data['type'], design_data['colors']]):
                        messagebox.showerror("Error", "Please fill in all required fields (Name, Type, Colors).")
                        return
                    
                    # Save to Firebase
                    doc_id = add_to_firebase('uniform_designs', design_data)
                    if not doc_id:
                        messagebox.showerror("Error", "Failed to save design to Firebase.")
                        return
                    
                    design_data['id'] = doc_id
                    
                    # Add to local list and refresh
                    self.uniform_designs.append(design_data)
                    self.load_designs_data()
                    self.update_course_filter_options()
                    
                    messagebox.showinfo("Success", f"Design added to {course_name} successfully!\nDesign ID: {doc_id}")
                    dialog.destroy()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save design: {str(e)}")
            
            # Buttons frame
            button_frame = tk.Frame(main_frame, bg="#ffffff")
            button_frame.pack(fill=tk.X, pady=20)
            
            # Cancel button
            cancel_btn = tk.Button(button_frame, text="Cancel", font=("Segoe UI", 12), 
                                  bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                                  command=dialog.destroy)
            cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            # Save button
            save_btn = tk.Button(button_frame, text="Save Design", font=("Segoe UI", 12, "bold"), 
                                bg="#28a745", fg="#ffffff", relief="flat", cursor="hand2",
                                command=save_design)
            save_btn.pack(side=tk.RIGHT)
            
        except Exception as e:
            print(f"Error creating add design to course dialog: {e}")
            messagebox.showerror("Error", f"Failed to create dialog: {str(e)}")
    
    def view_course_file(self, course_name):
        """View a specific course file"""
        try:
            # Get designs for the course
            course_designs = [design for design in self.uniform_designs 
                            if design.get('course') == course_name]
            
            if not course_designs:
                messagebox.showinfo("Course File", f"No designs found for {course_name}")
                return
            
            # Create course file viewer
            dialog = tk.Toplevel(self.root)
            dialog.title(f"Course File - {course_name}")
            dialog.geometry("800x600")
            dialog.configure(bg="#ffffff")
            dialog.transient(self.root)
            dialog.grab_set()
            
            # Center the dialog
            dialog.update_idletasks()
            x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
            y = (dialog.winfo_screenheight() // 2) - (600 // 2)
            dialog.geometry(f"800x600+{x}+{y}")
            
            # Main frame
            main_frame = tk.Frame(dialog, bg="#ffffff")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            
            # Title
            title_label = tk.Label(main_frame, text=f"Course File: {course_name}", 
                                  font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
            title_label.pack(pady=(0, 20))
            
            # Course summary
            summary_frame = tk.Frame(main_frame, bg="#e9ecef", relief="solid", bd=1)
            summary_frame.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(summary_frame, text=f"Total Designs: {len(course_designs)}", 
                    font=("Segoe UI", 12, "bold"), bg="#e9ecef", fg="#495057").pack(pady=10)
            
            # Create treeview for designs
            columns = ('ID', 'Name', 'Type', 'Colors', 'Status', 'Designer', 'Submitted Date', 'Image')
            designs_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
            
            # Define column widths
            column_widths = {
                'ID': 80, 'Name': 150, 'Type': 100, 'Colors': 100,
                'Status': 120, 'Designer': 120, 'Submitted Date': 120, 'Image': 80
            }
            
            for col in columns:
                designs_tree.heading(col, text=col)
                designs_tree.column(col, width=column_widths.get(col, 120), minwidth=80)
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=designs_tree.yview)
            designs_tree.configure(yscrollcommand=scrollbar.set)
            
            # Pack tree and scrollbar
            designs_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=(0, 20))
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 20))
            
            # Load designs data
            for design in course_designs:
                image_status = "📷 Yes" if design.get('has_image') else "❌ No"
                designs_tree.insert('', 'end', values=(
                    design.get('id', ''),
                    design.get('name', ''),
                    design.get('type', ''),
                    design.get('colors', ''),
                    design.get('status', ''),
                    design.get('designer', ''),
                    design.get('submitted_date', ''),
                    image_status
                ))
            
            # Action buttons
            action_frame = tk.Frame(main_frame, bg="#ffffff")
            action_frame.pack(fill=tk.X)
            
            # Add new design button
            add_btn = tk.Button(action_frame, text="➕ Add New Design", 
                               font=("Segoe UI", 11, "bold"), bg="#28a745", fg="#ffffff",
                               relief="flat", cursor="hand2", command=lambda: self.add_design_to_specific_course(course_name))
            add_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            # Export course button
            export_btn = tk.Button(action_frame, text="📤 Export Course File", 
                                  font=("Segoe UI", 11, "bold"), bg="#6f42c1", fg="#ffffff",
                                  relief="flat", cursor="hand2", command=lambda: self.export_single_course(course_name))
            export_btn.pack(side=tk.LEFT, padx=(0, 10))
            
            # Close button
            close_btn = tk.Button(action_frame, text="Close", font=("Segoe UI", 11, "bold"),
                                 bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                                 command=dialog.destroy)
            close_btn.pack(side=tk.RIGHT)
            
        except Exception as e:
            print(f"Error viewing course file: {e}")
            messagebox.showerror("Error", f"Failed to view course file: {str(e)}")
    
    def export_single_course(self, course_name):
        """Export a single course file"""
        try:
            from tkinter import filedialog
            import csv
            import os
            from datetime import datetime
            
            # Get designs for the course
            course_designs = [design for design in self.uniform_designs 
                            if design.get('course') == course_name]
            
            if not course_designs:
                messagebox.showwarning("Export", f"No designs found for {course_name}")
                return
            
            # Ask user for save location
            filename = filedialog.asksaveasfilename(
                title=f"Export {course_name} Course File",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            # Write to CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Design ID', 'Name', 'Type', 'Colors', 'Size Range', 
                             'Status', 'Designer', 'Submitted Date', 'Description', 'Image Status', 'Last Updated']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                # Add course header
                writer.writerow({
                    'Design ID': f"COURSE: {course_name.upper()}",
                    'Name': f"Total Designs: {len(course_designs)}",
                    'Type': f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    'Colors': '',
                    'Size Range': '',
                    'Status': '',
                    'Designer': '',
                    'Submitted Date': '',
                    'Description': '',
                    'Image Status': '',
                    'Last Updated': ''
                })
                
                # Add designs
                for design in course_designs:
                    image_status = "Yes" if design.get('has_image') else "No"
                    writer.writerow({
                        'Design ID': design.get('id', ''),
                        'Name': design.get('name', ''),
                        'Type': design.get('type', ''),
                        'Colors': design.get('colors', ''),
                        'Size Range': design.get('size_range', ''),
                        'Status': design.get('status', ''),
                        'Designer': design.get('designer', ''),
                        'Submitted Date': design.get('submitted_date', ''),
                        'Description': design.get('description', ''),
                        'Image Status': image_status,
                        'Last Updated': design.get('last_updated', '')
                    })
            
            messagebox.showinfo("Export Success", 
                              f"{course_name} course file exported successfully!\n\n"
                              f"File: {filename}\n"
                              f"Total designs: {len(course_designs)}")
            
        except Exception as e:
            print(f"Error exporting single course: {e}")
            messagebox.showerror("Export Error", f"Failed to export course file: {str(e)}")
    
    def create_appeal_statistics_display(self, parent):
        """Create appeal statistics display"""
        try:
            # Get appeal statistics
            appeal_stats = {
                'total': len(self.appeals),
                'pending_review': 0,
                'under_investigation': 0,
                'approved': 0,
                'rejected': 0,
                'closed': 0,
                'high_priority': 0,
                'medium_priority': 0,
                'low_priority': 0
            }
            
            for appeal in self.appeals:
                status = appeal.get('status', '')
                priority = appeal.get('priority', 'Medium')
                
                if status == 'Pending Review':
                    appeal_stats['pending_review'] += 1
                elif status == 'Under Investigation':
                    appeal_stats['under_investigation'] += 1
                elif status == 'Approved':
                    appeal_stats['approved'] += 1
                elif status == 'Rejected':
                    appeal_stats['rejected'] += 1
                elif status == 'Closed':
                    appeal_stats['closed'] += 1
                
                if priority == 'High':
                    appeal_stats['high_priority'] += 1
                elif priority == 'Medium':
                    appeal_stats['medium_priority'] += 1
                elif priority == 'Low':
                    appeal_stats['low_priority'] += 1
            
            # Create statistics display
            stats_container = tk.Frame(parent, bg="#e9ecef")
            stats_container.pack(fill=tk.X, padx=20, pady=(0, 10))
            
            # Status statistics
            status_frame = tk.Frame(stats_container, bg="#ffffff", relief="solid", bd=1)
            status_frame.pack(side=tk.LEFT, padx=(0, 10), pady=5, fill=tk.X, expand=True)
            
            tk.Label(status_frame, text="Status Breakdown", font=("Segoe UI", 10, "bold"), 
                    bg="#ffffff", fg="#1877f2").pack(pady=(8, 5))
            
            status_stats = [
                ("Pending Review", appeal_stats['pending_review'], "#ffc107"),
                ("Under Investigation", appeal_stats['under_investigation'], "#17a2b8"),
                ("Approved", appeal_stats['approved'], "#28a745"),
                ("Rejected", appeal_stats['rejected'], "#dc3545"),
                ("Closed", appeal_stats['closed'], "#6c757d")
            ]
            
            for status_name, count, color in status_stats:
                if count > 0:
                    tk.Label(status_frame, text=f"{status_name}: {count}", 
                            font=("Segoe UI", 9), bg=color, fg="#ffffff").pack(pady=1)
            
            # Priority statistics
            priority_frame = tk.Frame(stats_container, bg="#ffffff", relief="solid", bd=1)
            priority_frame.pack(side=tk.LEFT, padx=(0, 10), pady=5, fill=tk.X, expand=True)
            
            tk.Label(priority_frame, text="Priority Breakdown", font=("Segoe UI", 10, "bold"), 
                    bg="#ffffff", fg="#1877f2").pack(pady=(8, 5))
            
            priority_stats = [
                ("High Priority", appeal_stats['high_priority'], "#dc3545"),
                ("Medium Priority", appeal_stats['medium_priority'], "#ffc107"),
                ("Low Priority", appeal_stats['low_priority'], "#28a745")
            ]
            
            for priority_name, count, color in priority_stats:
                if count > 0:
                    tk.Label(priority_frame, text=f"{priority_name}: {count}", 
                            font=("Segoe UI", 9), bg=color, fg="#ffffff").pack(pady=1)
            
            # Total appeals
            total_frame = tk.Frame(stats_container, bg="#ffffff", relief="solid", bd=1)
            total_frame.pack(side=tk.LEFT, padx=(0, 10), pady=5, fill=tk.X, expand=True)
            
            tk.Label(total_frame, text="Total Appeals", font=("Segoe UI", 10, "bold"), 
                    bg="#ffffff", fg="#1877f2").pack(pady=(8, 5))
            tk.Label(total_frame, text=f"Total: {appeal_stats['total']}", 
                    font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#495057").pack()
            
        except Exception as e:
            print(f"Error creating appeal statistics: {e}")
    
    def add_new_appeal(self):
        """Add new appeal with comprehensive form"""
        # Create appeal form dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Appeal")
        dialog.geometry("700x800")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (700 // 2)
        y = (dialog.winfo_screenheight() // 2) - (800 // 2)
        dialog.geometry(f"700x800+{x}+{y}")
        
        # Main form frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Add New Appeal", 
                              font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Create scrollable frame for form
        canvas = tk.Canvas(main_frame, bg="#ffffff")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Form fields frame
        form_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Student Information
        tk.Label(form_frame, text="Student Information", font=("Segoe UI", 14, "bold"), 
                bg="#ffffff", fg="#1877f2").pack(anchor=tk.W, pady=(0, 10))
        
        # Student Name
        tk.Label(form_frame, text="Student Name:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        student_name_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        student_name_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Student ID
        tk.Label(form_frame, text="Student ID:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        student_id_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        student_id_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Violation ID
        tk.Label(form_frame, text="Violation ID:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        violation_id_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=50)
        violation_id_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Appeal Type
        tk.Label(form_frame, text="Appeal Type:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        appeal_types = ["Uniform Violation", "Medical Exemption", "Financial Hardship", "Religious Exemption", "Other"]
        appeal_type_var = tk.StringVar(value=appeal_types[0])
        appeal_type_combo = ttk.Combobox(form_frame, textvariable=appeal_type_var, 
                                        values=appeal_types, font=("Segoe UI", 12))
        appeal_type_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Priority
        tk.Label(form_frame, text="Priority:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(form_frame, textvariable=priority_var, 
                                     values=["Low", "Medium", "High"], font=("Segoe UI", 12))
        priority_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Submitted By
        tk.Label(form_frame, text="Submitted By:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        submitted_by_var = tk.StringVar(value="Student")
        submitted_by_combo = ttk.Combobox(form_frame, textvariable=submitted_by_var, 
                                         values=["Student", "Parent", "Guardian", "Teacher", "Other"], font=("Segoe UI", 12))
        submitted_by_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Appeal Reason
        tk.Label(form_frame, text="Appeal Reason:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(20, 5))
        reason_text = tk.Text(form_frame, height=4, font=("Segoe UI", 12), wrap=tk.WORD)
        reason_text.pack(fill=tk.X, pady=(0, 15))
        
        # Additional Notes
        tk.Label(form_frame, text="Additional Notes:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        notes_text = tk.Text(form_frame, height=3, font=("Segoe UI", 12), wrap=tk.WORD)
        notes_text.pack(fill=tk.X, pady=(0, 15))
        
        def save_appeal():
            """Save appeal to Firebase"""
            try:
                # Get form data
                appeal_data = {
                    'student_name': student_name_entry.get().strip(),
                    'student_id': student_id_entry.get().strip(),
                    'violation_id': violation_id_entry.get().strip(),
                    'appeal_date': datetime.now().strftime("%Y-%m-%d"),
                    'appeal_type': appeal_type_var.get(),
                    'priority': priority_var.get(),
                    'submitted_by': submitted_by_var.get(),
                    'reason': reason_text.get("1.0", tk.END).strip(),
                    'notes': notes_text.get("1.0", tk.END).strip(),
                    'status': 'Pending Review',
                    'evidence_documents': [],
                    'assigned_to': '',
                    'review_date': '',
                    'decision_reason': '',
                    'submitted_by_user': self.user_data['username'],
                    'submitted_by_name': self.user_data['full_name'],
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Validate required fields
                if not all([appeal_data['student_name'], appeal_data['student_id'], 
                           appeal_data['violation_id'], appeal_data['reason']]):
                    messagebox.showerror("Error", "Please fill in all required fields.")
                    return
                
                # Save to Firebase
                doc_id = add_to_firebase('appeals', appeal_data)
                if doc_id:
                    appeal_data['id'] = doc_id
                    self.appeals.append(appeal_data)
                    self.load_appeals_data()
                    
                    messagebox.showinfo("Success", f"Appeal added successfully!\nAppeal ID: {doc_id}")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save appeal to Firebase.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save appeal: {str(e)}")
        
        # Buttons frame
        button_frame = tk.Frame(form_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, pady=20)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", font=("Segoe UI", 12), 
                              bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                              command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save button
        save_btn = tk.Button(button_frame, text="Save Appeal", font=("Segoe UI", 12, "bold"), 
                            bg="#28a745", fg="#ffffff", relief="flat", cursor="hand2",
                            command=save_appeal)
        save_btn.pack(side=tk.RIGHT)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Set focus to first field
        student_name_entry.focus()
    
    def process_specific_appeal(self, appeal_data, parent_dialog):
        """Process a specific appeal with decision options"""
        # Create processing dialog
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Process Appeal - {appeal_data.get('student_name', 'Unknown')}")
        dialog.geometry("600x500")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text=f"Process Appeal - {appeal_data.get('student_name', 'Unknown')}", 
                              font=("Segoe UI", 16, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Current status
        current_status = tk.Label(main_frame, text=f"Current Status: {appeal_data.get('status', 'Unknown')}", 
                                font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#6c757d")
        current_status.pack(pady=(0, 20))
        
        # New status
        tk.Label(main_frame, text="New Status:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        status_var = tk.StringVar(value="Under Investigation")
        status_combo = ttk.Combobox(main_frame, textvariable=status_var, 
                                   values=["Pending Review", "Under Investigation", "Approved", "Rejected", "Closed"],
                                   font=("Segoe UI", 12))
        status_combo.pack(fill=tk.X, pady=(0, 15))
        
        # Assign to
        tk.Label(main_frame, text="Assign To:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        assign_var = tk.StringVar(value=self.user_data['full_name'])
        assign_entry = tk.Entry(main_frame, textvariable=assign_var, font=("Segoe UI", 12), width=50)
        assign_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Review date
        tk.Label(main_frame, text="Review Date:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        review_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        review_date_entry = tk.Entry(main_frame, textvariable=review_date_var, font=("Segoe UI", 12), width=50)
        review_date_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Decision reason
        tk.Label(main_frame, text="Decision/Notes:", font=("Segoe UI", 12, "bold"), 
                bg="#ffffff").pack(anchor=tk.W, pady=(0, 5))
        decision_text = tk.Text(main_frame, height=4, font=("Segoe UI", 12), wrap=tk.WORD)
        decision_text.pack(fill=tk.X, pady=(0, 15))
        
        def update_appeal():
            """Update appeal with new information"""
            try:
                # Update appeal data
                appeal_data.update({
                    'status': status_var.get(),
                    'assigned_to': assign_var.get(),
                    'review_date': review_date_var.get(),
                    'decision_reason': decision_text.get("1.0", tk.END).strip(),
                    'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'updated_by': self.user_data['username']
                })
                
                # Update in Firebase
                if appeal_data.get('id'):
                    update_in_firebase('appeals', appeal_data['id'], appeal_data)
                    print(f"✅ Appeal updated in Firebase: {appeal_data['id']}")
                
                # Refresh data
                self.load_appeals_data()
                
                messagebox.showinfo("Success", "Appeal updated successfully!")
                dialog.destroy()
                parent_dialog.destroy()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update appeal: {str(e)}")
        
        # Buttons frame
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(fill=tk.X, pady=20)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", font=("Segoe UI", 12), 
                              bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                              command=dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Update button
        update_btn = tk.Button(button_frame, text="Update Appeal", font=("Segoe UI", 12, "bold"), 
                              bg="#28a745", fg="#ffffff", relief="flat", cursor="hand2",
                              command=update_appeal)
        update_btn.pack(side=tk.RIGHT)
    
    def edit_appeal(self, appeal_data, parent_dialog):
        """Edit appeal information"""
        messagebox.showinfo("Edit Appeal", "Edit appeal functionality will be implemented here.\n\nThis would allow editing of appeal details.")
    
    def show_appeal_statistics(self):
        """Show detailed appeal statistics"""
        # Create statistics dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Appeal Statistics")
        dialog.geometry("800x600")
        dialog.configure(bg="#ffffff")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (dialog.winfo_screenheight() // 2) - (600 // 2)
        dialog.geometry(f"800x600+{x}+{y}")
        
        # Main frame
        main_frame = tk.Frame(dialog, bg="#ffffff")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Appeal Statistics & Analytics", 
                              font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#1877f2")
        title_label.pack(pady=(0, 20))
        
        # Create comprehensive statistics
        self.create_detailed_appeal_statistics(main_frame)
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", font=("Segoe UI", 12, "bold"),
                             bg="#6c757d", fg="#ffffff", relief="flat", cursor="hand2",
                             command=dialog.destroy)
        close_btn.pack(side=tk.BOTTOM, pady=20)
    
    def create_detailed_appeal_statistics(self, parent):
        """Create detailed appeal statistics"""
        try:
            # Calculate comprehensive statistics
            total_appeals = len(self.appeals)
            if total_appeals == 0:
                tk.Label(parent, text="No appeals data available", 
                        font=("Segoe UI", 12), bg="#ffffff", fg="#6c757d").pack(pady=50)
                return
            
            # Status breakdown
            status_stats = {}
            priority_stats = {}
            type_stats = {}
            monthly_stats = {}
            
            for appeal in self.appeals:
                # Status
                status = appeal.get('status', 'Unknown')
                status_stats[status] = status_stats.get(status, 0) + 1
                
                # Priority
                priority = appeal.get('priority', 'Medium')
                priority_stats[priority] = priority_stats.get(priority, 0) + 1
                
                # Type
                appeal_type = appeal.get('appeal_type', 'Unknown')
                type_stats[appeal_type] = type_stats.get(appeal_type, 0) + 1
                
                # Monthly
                try:
                    appeal_date = datetime.strptime(appeal.get('appeal_date', ''), "%Y-%m-%d")
                    month_key = appeal_date.strftime("%B %Y")
                    monthly_stats[month_key] = monthly_stats.get(month_key, 0) + 1
                except:
                    pass
            
            # Create statistics display
            stats_container = tk.Frame(parent, bg="#ffffff")
            stats_container.pack(fill=tk.BOTH, expand=True)
            
            # Top row - Summary
            summary_frame = tk.Frame(stats_container, bg="#e9ecef", relief="solid", bd=1)
            summary_frame.pack(fill=tk.X, pady=(0, 20))
            
            tk.Label(summary_frame, text=f"Total Appeals: {total_appeals}", 
                    font=("Segoe UI", 16, "bold"), bg="#e9ecef", fg="#495057").pack(pady=10)
            
            # Status breakdown
            status_frame = tk.LabelFrame(stats_container, text="Status Breakdown", 
                                       font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            status_frame.pack(fill=tk.X, pady=(0, 15))
            
            for status, count in status_stats.items():
                percentage = (count / total_appeals) * 100
                row_frame = tk.Frame(status_frame, bg="#ffffff")
                row_frame.pack(fill=tk.X, pady=2, padx=10)
                
                tk.Label(row_frame, text=f"{status}:", font=("Segoe UI", 11, "bold"), 
                        bg="#ffffff", width=20, anchor=tk.W).pack(side=tk.LEFT)
                tk.Label(row_frame, text=f"{count} ({percentage:.1f}%)", 
                        font=("Segoe UI", 11), bg="#ffffff").pack(side=tk.LEFT, padx=(10, 0))
            
            # Priority and Type breakdown
            breakdown_frame = tk.Frame(stats_container, bg="#ffffff")
            breakdown_frame.pack(fill=tk.X, pady=(0, 15))
            
            # Priority
            priority_frame = tk.LabelFrame(breakdown_frame, text="Priority Breakdown", 
                                         font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            priority_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
            
            for priority, count in priority_stats.items():
                row_frame = tk.Frame(priority_frame, bg="#ffffff")
                row_frame.pack(fill=tk.X, pady=2, padx=10)
                
                tk.Label(row_frame, text=f"{priority}:", font=("Segoe UI", 11, "bold"), 
                        bg="#ffffff", width=15, anchor=tk.W).pack(side=tk.LEFT)
                tk.Label(row_frame, text=str(count), font=("Segoe UI", 11), 
                        bg="#ffffff").pack(side=tk.LEFT, padx=(10, 0))
            
            # Type
            type_frame = tk.LabelFrame(breakdown_frame, text="Appeal Type Breakdown", 
                                     font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
            type_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
            
            for appeal_type, count in type_stats.items():
                row_frame = tk.Frame(type_frame, bg="#ffffff")
                row_frame.pack(fill=tk.X, pady=2, padx=10)
                
                tk.Label(row_frame, text=f"{appeal_type}:", font=("Segoe UI", 11, "bold"), 
                        bg="#ffffff", width=20, anchor=tk.W).pack(side=tk.LEFT)
                tk.Label(row_frame, text=str(count), font=("Segoe UI", 11), 
                        bg="#ffffff").pack(side=tk.LEFT, padx=(10, 0))
            
            # Monthly trend
            if monthly_stats:
                monthly_frame = tk.LabelFrame(stats_container, text="Monthly Trend", 
                                            font=("Segoe UI", 12, "bold"), bg="#ffffff", fg="#1877f2")
                monthly_frame.pack(fill=tk.X, pady=(0, 15))
                
                # Sort months chronologically
                sorted_months = sorted(monthly_stats.keys(), 
                                     key=lambda x: datetime.strptime(x, "%B %Y"))
                
                for month in sorted_months:
                    count = monthly_stats[month]
                    row_frame = tk.Frame(monthly_frame, bg="#ffffff")
                    row_frame.pack(fill=tk.X, pady=2, padx=10)
                    
                    tk.Label(row_frame, text=f"{month}:", font=("Segoe UI", 11, "bold"), 
                            bg="#ffffff", width=15, anchor=tk.W).pack(side=tk.LEFT)
                    tk.Label(row_frame, text=str(count), font=("Segoe UI", 11), 
                            bg="#ffffff").pack(side=tk.LEFT, padx=(10, 0))
            
        except Exception as e:
            print(f"Error creating detailed appeal statistics: {e}")
            tk.Label(parent, text=f"Error loading statistics: {str(e)}", 
                    font=("Segoe UI", 12), bg="#ffffff", fg="#dc3545").pack(pady=50)
    
    def export_appeals(self):
        """Export appeals to CSV"""
        try:
            from tkinter import filedialog
            import csv
            
            # Ask user for save location
            filename = filedialog.asksaveasfilename(
                title="Export Appeals",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if not filename:
                return
            
            # Write to CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Appeal ID', 'Student Name', 'Student ID', 'Violation ID', 'Appeal Date', 
                             'Appeal Type', 'Priority', 'Status', 'Submitted By', 'Reason', 'Notes', 
                             'Assigned To', 'Review Date', 'Decision Reason']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for appeal in self.appeals:
                    writer.writerow({
                        'Appeal ID': appeal.get('id', ''),
                        'Student Name': appeal.get('student_name', ''),
                        'Student ID': appeal.get('student_id', ''),
                        'Violation ID': appeal.get('violation_id', ''),
                        'Appeal Date': appeal.get('appeal_date', ''),
                        'Appeal Type': appeal.get('appeal_type', ''),
                        'Priority': appeal.get('priority', ''),
                        'Status': appeal.get('status', ''),
                        'Submitted By': appeal.get('submitted_by', ''),
                        'Reason': appeal.get('reason', ''),
                        'Notes': appeal.get('notes', ''),
                        'Assigned To': appeal.get('assigned_to', ''),
                        'Review Date': appeal.get('review_date', ''),
                        'Decision Reason': appeal.get('decision_reason', '')
                    })
            
            messagebox.showinfo("Export Success", 
                              f"Appeals exported successfully to:\n{filename}\n\n"
                              f"Total appeals: {len(self.appeals)}")
            
        except Exception as e:
            print(f"Error exporting appeals: {e}")
            messagebox.showerror("Export Error", f"Failed to export appeals: {str(e)}")
    
    def apply_appeal_filter(self):
        """Apply status filter to appeals"""
        try:
            selected_status = self.appeal_status_filter.get()
            
            if selected_status == "All Statuses":
                self.load_appeals_data()
            else:
                # Filter appeals by selected status
                filtered_appeals = [appeal for appeal in self.appeals 
                                  if appeal.get('status') == selected_status]
                
                # Clear existing items
                for item in self.appeals_tree.get_children():
                    self.appeals_tree.delete(item)
                
                # Insert filtered appeals data
                for appeal in filtered_appeals:
                    days_pending = self.calculate_days_pending(appeal.get('appeal_date', ''))
                    
                    self.appeals_tree.insert('', 'end', values=(
                        appeal.get('id', ''),
                        appeal.get('student_name', ''),
                        appeal.get('student_id', ''),
                        appeal.get('violation_id', ''),
                        appeal.get('appeal_date', ''),
                        appeal.get('status', ''),
                        appeal.get('submitted_by', ''),
                        appeal.get('priority', 'Medium'),
                        f"{days_pending} days"
                    ))
                
                print(f"✅ Filtered appeals by status: {selected_status} ({len(filtered_appeals)} appeals)")
                
        except Exception as e:
            print(f"Error applying appeal filter: {e}")
            messagebox.showerror("Filter Error", f"Failed to apply filter: {str(e)}")
    
    def clear_appeal_filter(self):
        """Clear the appeal filter and show all appeals"""
        try:
            self.appeal_status_filter.set("All Statuses")
            self.load_appeals_data()
            print("✅ Appeal filter cleared")
        except Exception as e:
            print(f"Error clearing appeal filter: {e}")
    
    def refresh_designs_data(self):
        """Refresh designs data and statistics"""
        try:
            # Reload data from Firebase
            firebase_designs = get_from_firebase('uniform_designs')
            if firebase_designs:
                self.uniform_designs = firebase_designs
                print(f"✅ Refreshed {len(self.uniform_designs)} designs from Firebase")
            
            # Update table and filters
            self.load_designs_data()
            self.update_course_filter_options()
            
            # Refresh statistics (recreate the statistics frame)
            for widget in self.notebook.winfo_children():
                if "Uniform Designs" in widget.winfo_name():
                    # Find and recreate statistics
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame) and child.winfo_children():
                            for grandchild in child.winfo_children():
                                if isinstance(grandchild, tk.Frame) and grandchild.winfo_children():
                                    # This is likely the stats frame
                                    grandchild.destroy()
                                    self.create_course_statistics(child)
                                    break
                            break
                    break
            
            print("✅ Designs data refreshed successfully")
            
        except Exception as e:
            print(f"Error refreshing designs data: {e}")
            messagebox.showerror("Refresh Error", f"Failed to refresh data: {str(e)}")
    
    def clear_course_filter(self):
        """Clear the course filter and show all designs"""
        try:
            self.course_filter_var.set("All Courses")
            self.load_designs_data()
            print("✅ Course filter cleared")
        except Exception as e:
            print(f"Error clearing course filter: {e}")
    
    def logout(self):
        """Logout from dashboard"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            try:
                # Close the dashboard window completely
                self.root.destroy()
                # If this is a Toplevel, the parent (login) will handle the return
                # If this is the main Tk, exit the application
                if isinstance(self.root, tk.Tk):
                    self.root.quit()
            except Exception as e:
                print(f"Error during logout: {e}")
                # Force close if normal close fails
                try:
                    self.root.destroy()
                except:
                    pass
    
    def run(self):
        """Start the dashboard"""
        # Avoid nested Tk mainloops if running as Toplevel
        if isinstance(self.root, tk.Tk):
            self.root.mainloop()
        else:
            self.root.wait_window()

# Test function
if __name__ == "__main__":
    # Sample user data for testing
    test_user = {
        'username': 'guidance1',
        'full_name': 'Mrs. Sarah Johnson',
        'role': 'Guidance Counselor',
        'status': 'ACTIVE'
    }
    
    dashboard = GuidanceDashboard(test_user)
    dashboard.run()
