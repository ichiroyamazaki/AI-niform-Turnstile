from flask import Flask, render_template, request, redirect, url_for, session, flash
import hashlib
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Load users from users.txt
def load_users():
    users = {}
    try:
        with open('users.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split(',')
                    if len(parts) >= 4:
                        username, password_hash, user_type, name = parts[:4]
                        users[username] = {
                            'password_hash': password_hash,
                            'type': user_type,
                            'name': name,
                            'status': parts[4] if len(parts) > 4 else 'ACTIVE'
                        }
    except FileNotFoundError:
        print("users.txt not found")
    return users

# Hash password for comparison
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authentication function
def authenticate_user(username, password):
    users = load_users()
    if username in users:
        user = users[username]
        if user['status'] == 'ACTIVE' and user['password_hash'] == hash_password(password):
            return user
    return None

@app.route('/')
def index():
    if 'user' in session:
        if session['user']['type'] == 'guidance':
            return redirect('/guidance-dashboard')
        else:
            return redirect('/admin-dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = authenticate_user(username, password)
        if user:
            session['user'] = {
                'username': username,
                'type': user['type'],
                'name': user['name']
            }
            
            # Log successful login
            log_access(username, 'LOGIN_SUCCESS')
            
            if user['type'] == 'guidance':
                return redirect('/guidance-dashboard')
            else:
                return redirect('/admin-dashboard')
        else:
            # Log failed login attempt
            log_access(username, 'LOGIN_FAILED')
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        log_access(session['user']['username'], 'LOGOUT')
        session.pop('user', None)
    return redirect('/login')

@app.route('/guidance-dashboard')
def guidance_dashboard():
    if 'user' not in session or session['user']['type'] != 'guidance':
        return redirect('/login')
    
    # Load data from Firebase or create sample data
    try:
        from firebase_config import get_from_firebase, add_to_firebase
        violations = get_from_firebase('violations') or []
        appeals = get_from_firebase('appeals') or []
        designs = get_from_firebase('uniform_designs') or []
        
        # If no data exists, create sample data
        if not violations:
            sample_violations = create_sample_violations()
            for violation in sample_violations:
                add_to_firebase('violations', violation)
            violations = sample_violations
            
        if not appeals:
            sample_appeals = create_sample_appeals()
            for appeal in sample_appeals:
                add_to_firebase('appeals', appeal)
            appeals = sample_appeals
            
        if not designs:
            sample_designs = create_sample_designs()
            for design in sample_designs:
                add_to_firebase('uniform_designs', design)
            designs = sample_designs
            
    except Exception as e:
        print(f"Error loading data: {e}")
        violations = create_sample_violations()
        appeals = create_sample_appeals()
        designs = create_sample_designs()
    
    # Calculate statistics
    stats = {
        'total_violations': len(violations),
        'pending_violations': len([v for v in violations if v.get('status') == 'Pending']),
        'total_appeals': len(appeals),
        'pending_appeals': len([a for a in appeals if a.get('status') == 'Pending Review']),
        'total_designs': len(designs),
        'approved_designs': len([d for d in designs if d.get('status') == 'Approved'])
    }
    
    # Sort appeals: approved ones at the bottom, others by priority
    def sort_appeals(appeal):
        if appeal.get('status') == 'Approved':
            return (1, 0)  # Approved appeals go to bottom
        else:
            # Sort by priority: High=3, Medium=2, Low=1, Urgent=4
            priority_order = {'Urgent': 4, 'High': 3, 'Medium': 2, 'Low': 1}
            priority = appeal.get('priority', 'Low')
            return (0, priority_order.get(priority, 1))
    
    sorted_appeals = sorted(appeals, key=sort_appeals, reverse=True)
    
    return render_template('guidance_dashboard.html', 
                         user=session['user'], 
                         violations=violations[:10],
                         appeals=sorted_appeals[:10],
                         designs=designs[:10],
                         stats=stats)

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'user' not in session or session['user']['type'] != 'admin':
        return redirect('/login')
    return render_template('admin_dashboard.html', user=session['user'])

# API Routes for CRUD Operations
@app.route('/api/violations', methods=['POST'])
def add_violation():
    if 'user' not in session or session['user']['type'] != 'guidance':
        return {'error': 'Unauthorized'}, 401
    
    try:
        from firebase_config import add_to_firebase
        data = request.get_json()
        
        # Add current date and user info
        data['date'] = datetime.now().strftime('%Y-%m-%d')
        data['status'] = 'Pending'
        data['created_by'] = session['user']['username']
        
        doc_id = add_to_firebase('violations', data)
        return {'success': True, 'id': doc_id}, 201
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/violations/<violation_id>', methods=['PUT'])
def update_violation(violation_id):
    if 'user' not in session or session['user']['type'] != 'guidance':
        return {'error': 'Unauthorized'}, 401
    
    try:
        from firebase_config import update_in_firebase
        data = request.get_json()
        data['updated_by'] = session['user']['username']
        data['updated_at'] = datetime.now().isoformat()
        
        success = update_in_firebase('violations', violation_id, data)
        return {'success': success}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/violations/<violation_id>', methods=['DELETE'])
def delete_violation(violation_id):
    if 'user' not in session or session['user']['type'] != 'guidance':
        return {'error': 'Unauthorized'}, 401
    
    try:
        from firebase_config import delete_from_firebase
        success = delete_from_firebase('violations', violation_id)
        return {'success': success}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/appeals', methods=['POST'])
def add_appeal():
    if 'user' not in session or session['user']['type'] != 'guidance':
        return {'error': 'Unauthorized'}, 401
    
    try:
        from firebase_config import add_to_firebase
        data = request.get_json()
        
        # Add current date and user info
        data['date'] = datetime.now().strftime('%Y-%m-%d')
        data['status'] = 'Pending Review'
        data['created_by'] = session['user']['username']
        
        doc_id = add_to_firebase('appeals', data)
        return {'success': True, 'id': doc_id}, 201
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/appeals/<appeal_id>', methods=['PUT'])
def update_appeal(appeal_id):
    if 'user' not in session or session['user']['type'] != 'guidance':
        return {'error': 'Unauthorized'}, 401
    
    try:
        from firebase_config import update_in_firebase
        data = request.get_json()
        data['updated_by'] = session['user']['username']
        data['updated_at'] = datetime.now().isoformat()
        
        success = update_in_firebase('appeals', appeal_id, data)
        return {'success': success}, 200
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/designs', methods=['POST'])
def add_design():
    if 'user' not in session or session['user']['type'] != 'guidance':
        return {'error': 'Unauthorized'}, 401
    
    try:
        from firebase_config import add_to_firebase
        data = request.get_json()
        
        # Add current date and user info
        data['created_date'] = datetime.now().strftime('%Y-%m-%d')
        data['created_by'] = session['user']['username']
        
        doc_id = add_to_firebase('uniform_designs', data)
        return {'success': True, 'id': doc_id}, 201
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/api/designs/<design_id>', methods=['PUT'])
def update_design(design_id):
    if 'user' not in session or session['user']['type'] != 'guidance':
        return {'error': 'Unauthorized'}, 401
    
    try:
        from firebase_config import update_in_firebase
        data = request.get_json()
        data['updated_by'] = session['user']['username']
        data['updated_at'] = datetime.now().isoformat()
        
        success = update_in_firebase('uniform_designs', design_id, data)
        return {'success': success}, 200
    except Exception as e:
        return {'error': str(e)}, 500

def log_access(username, action):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {username} - {action}\n"
    
    try:
        with open('access_log.txt', 'a') as file:
            file.write(log_entry)
    except Exception as e:
        print(f"Error logging access: {e}")

def create_sample_violations():
    """Create sample violations data"""
    return [
        {
            'id': 'violation_001',
            'student_name': 'John Smith',
            'student_id': '2024-001',
            'violation_type': 'Inappropriate Attire',
            'date': '2024-01-15',
            'description': 'Wearing non-regulation shoes with incorrect color',
            'status': 'Pending',
            'reported_by': 'Security Guard',
            'location': 'Main Gate',
            'severity': 'Medium'
        },
        {
            'id': 'violation_002',
            'student_name': 'Sarah Johnson',
            'student_id': '2024-002',
            'violation_type': 'Missing Components',
            'date': '2024-01-14',
            'description': 'Student not wearing school ID badge',
            'status': 'Resolved',
            'reported_by': 'Teacher',
            'location': 'Classroom 101',
            'severity': 'Low'
        },
        {
            'id': 'violation_003',
            'student_name': 'Mike Davis',
            'student_id': '2024-003',
            'violation_type': 'Color Violation',
            'date': '2024-01-13',
            'description': 'Wearing non-uniform shirt',
            'status': 'Under Review',
            'reported_by': 'Guidance Counselor',
            'location': 'Cafeteria',
            'severity': 'High'
        }
    ]

def create_sample_appeals():
    """Create sample appeals data"""
    return [
        {
            'id': 'appeal_001',
            'student_name': 'Emma Wilson',
            'student_id': '2024-004',
            'appeal_type': 'Violation Appeal',
            'date': '2024-01-12',
            'reason': 'Appealing violation for wearing non-regulation shoes due to medical condition',
            'status': 'Pending Review',
            'submitted_by': 'Emma Wilson',
            'violation_id': 'V-001',
            'priority': 'High'
        },
        {
            'id': 'appeal_002',
            'student_name': 'Alex Brown',
            'student_id': '2024-005',
            'appeal_type': 'Policy Appeal',
            'date': '2024-01-11',
            'reason': 'Requesting clarification on new uniform policy',
            'status': 'Under Investigation',
            'submitted_by': 'Alex Brown',
            'violation_id': 'V-002',
            'priority': 'Medium'
        },
        {
            'id': 'appeal_003',
            'student_name': 'Maria Garcia',
            'student_id': '2024-006',
            'appeal_type': 'Design Appeal',
            'date': '2024-01-10',
            'reason': 'Appealing rejection of uniform design submission',
            'status': 'Approved',
            'submitted_by': 'Maria Garcia',
            'violation_id': 'V-003',
            'priority': 'Low'
        }
    ]

def create_sample_designs():
    """Create sample uniform designs data"""
    return [
        {
            'id': 'design_001',
            'name': 'Standard School Uniform',
            'type': 'Formal',
            'status': 'Approved',
            'created_date': '2024-01-10',
            'description': 'Standard formal uniform design for all students - includes white shirt, navy pants, black shoes, and school tie',
            'components': ['White Shirt', 'Navy Pants', 'Black Shoes', 'School Tie', 'ID Badge'],
            'grade_level': 'All Grades',
            'notes': 'Mandatory for all school days except PE classes'
        },
        {
            'id': 'design_002',
            'name': 'PE Uniform Design',
            'type': 'Sports',
            'status': 'Pending Review',
            'created_date': '2024-01-09',
            'description': 'Physical Education uniform design - comfortable and durable for sports activities',
            'components': ['School T-shirt', 'Athletic Shorts', 'White Socks', 'Sneakers'],
            'grade_level': 'All Grades',
            'notes': 'Required for all physical education classes'
        },
        {
            'id': 'design_003',
            'name': 'Winter Uniform Variant',
            'type': 'Winter',
            'status': 'Active',
            'created_date': '2024-01-08',
            'description': 'Winter version of the standard uniform with additional layers for cold weather',
            'components': ['White Shirt', 'Navy Pants', 'School Sweater', 'Winter Jacket', 'Black Shoes'],
            'grade_level': 'All Grades',
            'notes': 'Optional during winter months when temperature drops below 15°C'
        },
        {
            'id': 'design_004',
            'name': 'Graduation Ceremony Attire',
            'type': 'Special',
            'status': 'Approved',
            'created_date': '2024-01-07',
            'description': 'Special uniform design for graduation ceremonies and formal events',
            'components': ['White Dress Shirt', 'Navy Blazer', 'Dress Pants', 'Dress Shoes', 'Graduation Cap'],
            'grade_level': 'High School',
            'notes': 'Required for graduation ceremonies and special school events'
        },
        {
            'id': 'design_005',
            'name': 'Summer Uniform Design',
            'type': 'Summer',
            'status': 'Draft',
            'created_date': '2024-01-06',
            'description': 'Lightweight summer uniform design for hot weather months',
            'components': ['Polo Shirt', 'Khaki Shorts', 'White Socks', 'Canvas Shoes'],
            'grade_level': 'Elementary',
            'notes': 'Under development for implementation in summer months'
        },
        {
            'id': 'design_006',
            'name': 'Band Uniform Design',
            'type': 'Special',
            'status': 'Rejected',
            'created_date': '2024-01-05',
            'description': 'Special uniform design for school band members',
            'components': ['Band Jacket', 'White Shirt', 'Black Pants', 'Black Shoes', 'Band Cap'],
            'grade_level': 'All Grades',
            'notes': 'Rejected due to budget constraints - needs revision'
        }
    ]

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

