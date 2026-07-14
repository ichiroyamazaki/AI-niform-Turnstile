from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
import hashlib
from firebase_config import (
    get_from_firebase,
    search_in_firebase,
    add_to_firebase,
    update_in_firebase,
    delete_from_firebase,
)
from cloudinary_config import upload_image_to_cloudinary
import tempfile
import os
import time
import random
import json


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def analyze_design_uniqueness(design_data):
    """
    Analyze the uniqueness of a uniform design based on various factors.
    This is a simulated analysis - in a real implementation, you would use
    computer vision and machine learning models.
    """
    try:
        # Simulate uniqueness analysis based on design characteristics
        uniqueness_score = random.randint(60, 95)  # Simulated score 60-95%
        
        # Analyze different aspects
        color_uniqueness = analyze_color_uniqueness(design_data.get('colors', ''))
        pattern_uniqueness = analyze_pattern_uniqueness(design_data.get('type', ''))
        style_uniqueness = analyze_style_uniqueness(design_data.get('description', ''))
        
        # Generate uniqueness annotations
        annotations = []
        
        # Color analysis
        if color_uniqueness['score'] > 80:
            annotations.append({
                'aspect': 'Color Scheme',
                'score': color_uniqueness['score'],
                'comment': color_uniqueness['comment'],
                'uniqueness': 'High'
            })
        elif color_uniqueness['score'] > 60:
            annotations.append({
                'aspect': 'Color Scheme',
                'score': color_uniqueness['score'],
                'comment': color_uniqueness['comment'],
                'uniqueness': 'Medium'
            })
        else:
            annotations.append({
                'aspect': 'Color Scheme',
                'score': color_uniqueness['score'],
                'comment': color_uniqueness['comment'],
                'uniqueness': 'Low'
            })
        
        # Pattern analysis
        if pattern_uniqueness['score'] > 80:
            annotations.append({
                'aspect': 'Design Pattern',
                'score': pattern_uniqueness['score'],
                'comment': pattern_uniqueness['comment'],
                'uniqueness': 'High'
            })
        elif pattern_uniqueness['score'] > 60:
            annotations.append({
                'aspect': 'Design Pattern',
                'score': pattern_uniqueness['score'],
                'comment': pattern_uniqueness['comment'],
                'uniqueness': 'Medium'
            })
        else:
            annotations.append({
                'aspect': 'Design Pattern',
                'score': pattern_uniqueness['score'],
                'comment': pattern_uniqueness['comment'],
                'uniqueness': 'Low'
            })
        
        # Style analysis
        if style_uniqueness['score'] > 80:
            annotations.append({
                'aspect': 'Style Innovation',
                'score': style_uniqueness['score'],
                'comment': style_uniqueness['comment'],
                'uniqueness': 'High'
            })
        elif style_uniqueness['score'] > 60:
            annotations.append({
                'aspect': 'Style Innovation',
                'score': style_uniqueness['score'],
                'comment': style_uniqueness['comment'],
                'uniqueness': 'Medium'
            })
        else:
            annotations.append({
                'aspect': 'Style Innovation',
                'score': style_uniqueness['score'],
                'comment': style_uniqueness['comment'],
                'uniqueness': 'Low'
            })
        
        # Overall uniqueness assessment
        overall_score = sum(ann['score'] for ann in annotations) // len(annotations)
        
        if overall_score > 85:
            overall_assessment = "Highly Unique"
            recommendation = "This design stands out significantly and is recommended for approval."
        elif overall_score > 70:
            overall_assessment = "Moderately Unique"
            recommendation = "This design has good uniqueness but could benefit from minor enhancements."
        elif overall_score > 55:
            overall_assessment = "Somewhat Unique"
            recommendation = "Consider adding more distinctive elements to improve uniqueness."
        else:
            overall_assessment = "Low Uniqueness"
            recommendation = "This design may be too similar to existing uniforms. Consider redesigning."
        
        return {
            'overall_score': overall_score,
            'overall_assessment': overall_assessment,
            'recommendation': recommendation,
            'annotations': annotations,
            'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'unique_features': generate_unique_features(design_data)
        }
        
    except Exception as e:
        print(f"Error in uniqueness analysis: {e}")
        return {
            'overall_score': 50,
            'overall_assessment': 'Analysis Failed',
            'recommendation': 'Unable to analyze uniqueness. Please try again.',
            'annotations': [],
            'analysis_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'unique_features': []
        }


def analyze_color_uniqueness(colors):
    """Analyze color scheme uniqueness"""
    if not colors:
        return {'score': 30, 'comment': 'No color information provided'}
    
    color_keywords = ['unique', 'vibrant', 'distinctive', 'bold', 'creative', 'innovative']
    color_score = 50
    
    # Check for unique color combinations
    if any(keyword in colors.lower() for keyword in color_keywords):
        color_score += 25
    
    # Check for specific color combinations
    if 'gradient' in colors.lower():
        color_score += 15
    if 'metallic' in colors.lower():
        color_score += 10
    if len(colors.split()) > 3:  # Multiple colors
        color_score += 10
    
    return {
        'score': min(color_score, 100),
        'comment': f"Color scheme analysis: {colors}. {'Excellent color diversity' if color_score > 80 else 'Good color choices' if color_score > 60 else 'Consider more distinctive colors'}"
    }


def analyze_pattern_uniqueness(design_type):
    """Analyze design pattern uniqueness"""
    if not design_type:
        return {'score': 30, 'comment': 'No design type specified'}
    
    pattern_score = 60  # Base score
    
    # Different types have different uniqueness potential
    if design_type.lower() in ['complete set', 'blouse']:
        pattern_score += 20
    elif design_type.lower() in ['shirt', 'pants']:
        pattern_score += 10
    elif design_type.lower() == 'skirt':
        pattern_score += 15
    
    return {
        'score': min(pattern_score, 100),
        'comment': f"Design type '{design_type}' shows {'high' if pattern_score > 80 else 'moderate' if pattern_score > 60 else 'basic'} uniqueness potential"
    }


def analyze_style_uniqueness(description):
    """Analyze style innovation uniqueness"""
    if not description:
        return {'score': 40, 'comment': 'No description provided for style analysis'}
    
    style_keywords = ['modern', 'innovative', 'unique', 'distinctive', 'creative', 'elegant', 'sophisticated']
    style_score = 50
    
    # Check for style-related keywords
    keyword_count = sum(1 for keyword in style_keywords if keyword in description.lower())
    style_score += keyword_count * 8
    
    # Check description length (more detailed descriptions often indicate more thought)
    if len(description) > 100:
        style_score += 10
    if len(description) > 200:
        style_score += 5
    
    return {
        'score': min(style_score, 100),
        'comment': f"Style analysis: {'Excellent innovation' if style_score > 80 else 'Good style elements' if style_score > 60 else 'Basic style approach'}"
    }


def generate_unique_features(design_data):
    """Generate list of unique features identified in the design"""
    features = []
    
    # Color features
    if design_data.get('colors'):
        if 'gradient' in design_data['colors'].lower():
            features.append("Gradient color transition")
        if 'metallic' in design_data['colors'].lower():
            features.append("Metallic finish elements")
        if len(design_data['colors'].split()) > 2:
            features.append("Multi-color combination")
    
    # Type features
    if design_data.get('type'):
        if design_data['type'].lower() == 'complete set':
            features.append("Coordinated complete uniform set")
        elif design_data['type'].lower() == 'blouse':
            features.append("Professional blouse design")
    
    # Description features
    if design_data.get('description'):
        desc = design_data['description'].lower()
        if 'modern' in desc:
            features.append("Modern design approach")
        if 'elegant' in desc:
            features.append("Elegant styling")
        if 'innovative' in desc:
            features.append("Innovative design elements")
    
    # Default features if none identified
    if not features:
        features = ["Standard uniform design", "Functional design elements"]
    
    return features


def update_violation_in_firebase(violation_id, data):
    """Update violation in Firebase"""
    try:
        return update_in_firebase("violations", violation_id, data)
    except Exception as e:
        print(f"Error updating violation: {e}")
        return False


def delete_violation_from_firebase(violation_id):
    """Delete violation from Firebase"""
    try:
        return delete_from_firebase("violations", violation_id)
    except Exception as e:
        print(f"Error deleting violation: {e}")
        return False


def update_appeal_in_firebase(appeal_id, data):
    """Update appeal in Firebase"""
    try:
        return update_in_firebase("appeals", appeal_id, data)
    except Exception as e:
        print(f"Error updating appeal: {e}")
        return False


def delete_appeal_from_firebase(appeal_id):
    """Delete appeal from Firebase"""
    try:
        return delete_from_firebase("appeals", appeal_id)
    except Exception as e:
        print(f"Error deleting appeal: {e}")
        return False


def update_design_in_firebase(design_id, data):
    """Update design in Firebase"""
    try:
        return update_in_firebase("uniform_designs", design_id, data)
    except Exception as e:
        print(f"Error updating design: {e}")
        return False


def delete_design_from_firebase(design_id):
    """Delete design from Firebase"""
    try:
        return delete_from_firebase("uniform_designs", design_id)
    except Exception as e:
        print(f"Error deleting design: {e}")
        return False


app = Flask(__name__)
app.secret_key = "replace-this-with-a-secure-secret-key"
app.permanent_session_lifetime = timedelta(hours=8)


@app.context_processor
def inject_globals():
    return {"app_name": "AI-niform"}


@app.route("/")
def root():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter both username and password", "error")
            return render_template("login.html")

        # Try to find user by username in Firestore
        user_records = search_in_firebase("users", "username", username) or []
        user = user_records[0] if user_records else None

        if not user:
            flash("Invalid username or password", "error")
            return render_template("login.html")

        # Verify password
        if hash_password(password) != user.get("password_hash"):
            flash("Invalid username or password", "error")
            return render_template("login.html")

        if (user.get("status") or "ACTIVE") != "ACTIVE":
            flash("Account is deactivated. Please contact administrator.", "error")
            return render_template("login.html")

        # Login OK → put minimal user in session
        session.permanent = True
        session["user"] = {
            "id": user.get("id"),
            "username": user.get("username"),
            "name": user.get("full_name") or user.get("username"),
            "role": user.get("role", "Guidance Counselor"),
        }
        flash("Welcome back!", "success")
        return redirect(url_for("dashboard"))

    # GET
    return render_template("login.html")


def require_login():
    if "user" not in session:
        return False
    return True


@app.route("/dashboard")
def dashboard():
    if not require_login():
        return redirect(url_for("login"))

    user = session.get("user")

    # Fetch real data from Firebase collections
    try:
        violations = get_from_firebase("violations", 20) or []
    except Exception as e:
        print(f"Error fetching violations: {e}")
        violations = []

    try:
        appeals = get_from_firebase("appeals", 20) or []
    except Exception as e:
        print(f"Error fetching appeals: {e}")
        appeals = []

    try:
        designs = get_from_firebase("uniform_designs", 20) or []
    except Exception as e:
        print(f"Error fetching designs: {e}")
        designs = []

    # Calculate real statistics
    total_violations = len(violations)
    pending_violations = len([v for v in violations if v.get('status') == 'Pending'])
    total_appeals = len(appeals)
    pending_appeals = len([a for a in appeals if a.get('status') == 'Pending Review'])
    total_designs = len(designs)
    approved_designs = len([d for d in designs if d.get('status') == 'Approved'])

    # Calculate compliance rate (mock calculation)
    compliance_rate = 94.2 if total_violations == 0 else max(70, 100 - (total_violations * 2))

    stats = {
        'total_students': 1247,  # This would come from a students collection
        'compliance_rate': compliance_rate,
        'violations_today': pending_violations,
        'events_this_week': 8,  # This would come from events collection
        'total_violations': total_violations,
        'total_appeals': total_appeals,
        'total_designs': total_designs,
        'approved_designs': approved_designs
    }

    return render_template(
        "guidance_dashboard.html",
        user=user,
        violations=violations[:5],  # Show only recent 5
        appeals=appeals[:5],  # Show only recent 5
        designs=designs[:5],  # Show only recent 5
        stats=stats
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# ============ Feature pages ============

@app.route("/violations", methods=["GET", "POST"])
def violations_page():
    if not require_login():
        return redirect(url_for("login"))

    if request.method == "POST":
        data = {
            "student_name": request.form.get("student_name", "").strip(),
            "student_id": request.form.get("student_id", "").strip(),
            "violation_type": request.form.get("violation_type", "").strip(),
            "course": request.form.get("course", "").strip(),
            "date": request.form.get("date", "").strip(),
            "description": request.form.get("description", "").strip(),
            "status": request.form.get("status", "Pending"),
            "reported_by": session.get("user", {}).get("name", "Guidance"),
        }
        if not data["student_name"] or not data["student_id"] or not data["violation_type"]:
            flash("Student, ID and Type are required", "error")
        else:
            doc_id = add_to_firebase("violations", data)
            if doc_id:
                flash(f"Violation saved (ID: {doc_id})", "success")
            else:
                flash("Failed to save violation", "error")
        return redirect(url_for("violations_page"))

    items = get_from_firebase("violations") or []
    # Add document IDs to items for action buttons
    for i, item in enumerate(items):
        if 'id' not in item:
            item['id'] = f"violation_{i}"  # Fallback ID if not available
    return render_template("violations.html", user=session.get("user"), items=items)


@app.route("/violations/view/<violation_id>")
def view_violation(violation_id):
    if not require_login():
        return redirect(url_for("login"))
    
    # Get violation details from Firebase
    violation = search_in_firebase("violations", "id", violation_id)
    if not violation:
        flash("Violation not found", "error")
        return redirect(url_for("violations_page"))
    
    return render_template("violation_details.html", violation=violation[0], user=session.get("user"))


@app.route("/violations/edit/<violation_id>", methods=["GET", "POST"])
def edit_violation(violation_id):
    if not require_login():
        return redirect(url_for("login"))
    
    if request.method == "POST":
        # Update violation data
        data = {
            "student_name": request.form.get("student_name", "").strip(),
            "student_id": request.form.get("student_id", "").strip(),
            "violation_type": request.form.get("violation_type", "").strip(),
            "course": request.form.get("course", "").strip(),
            "date": request.form.get("date", "").strip(),
            "description": request.form.get("description", "").strip(),
            "status": request.form.get("status", "Pending"),
            "reported_by": session.get("user", {}).get("name", "Guidance"),
        }
        
        if not data["student_name"] or not data["student_id"] or not data["violation_type"]:
            flash("Student, ID and Type are required", "error")
        else:
            # Update in Firebase
            success = update_violation_in_firebase(violation_id, data)
            if success:
                flash("Violation updated successfully", "success")
            else:
                flash("Failed to update violation", "error")
        return redirect(url_for("violations_page"))
    
    # Get violation details for editing
    violation = search_in_firebase("violations", "id", violation_id)
    if not violation:
        flash("Violation not found", "error")
        return redirect(url_for("violations_page"))
    
    return render_template("edit_violation.html", violation=violation[0], user=session.get("user"))


@app.route("/violations/delete/<violation_id>", methods=["POST"])
def delete_violation(violation_id):
    if not require_login():
        return redirect(url_for("login"))
    
    # Delete violation from Firebase
    success = delete_violation_from_firebase(violation_id)
    if success:
        flash("Violation deleted successfully", "success")
    else:
        flash("Failed to delete violation", "error")
    
    return redirect(url_for("violations_page"))


@app.route("/appeals", methods=["GET", "POST"])
def appeals_page():
    if not require_login():
        return redirect(url_for("login"))

    if request.method == "POST":
        data = {
            "student_name": request.form.get("student_name", "").strip(),
            "student_id": request.form.get("student_id", "").strip(),
            "violation_id": request.form.get("violation_id", "").strip(),
            "appeal_date": request.form.get("appeal_date", "").strip(),
            "reason": request.form.get("reason", "").strip(),
            "status": request.form.get("status", "Pending Review"),
            "submitted_by": request.form.get("submitted_by", "").strip(),
            "priority": request.form.get("priority", "Medium"),
        }
        if not data["student_name"] or not data["student_id"] or not data["violation_id"]:
            flash("Student, ID and Violation ID are required", "error")
        else:
            doc_id = add_to_firebase("appeals", data)
            if doc_id:
                flash(f"Appeal saved (ID: {doc_id})", "success")
            else:
                flash("Failed to save appeal", "error")
        return redirect(url_for("appeals_page"))

    items = get_from_firebase("appeals") or []
    # Add document IDs to items for action buttons
    for i, item in enumerate(items):
        if 'id' not in item:
            item['id'] = f"appeal_{i}"  # Fallback ID if not available
    return render_template("appeals.html", user=session.get("user"), items=items)


@app.route("/appeals/view/<appeal_id>")
def view_appeal(appeal_id):
    if not require_login():
        return redirect(url_for("login"))
    
    # Get appeal details from Firebase
    appeal = search_in_firebase("appeals", "id", appeal_id)
    if not appeal:
        flash("Appeal not found", "error")
        return redirect(url_for("appeals_page"))
    
    return render_template("appeal_details.html", appeal=appeal[0], user=session.get("user"))


@app.route("/appeals/edit/<appeal_id>", methods=["GET", "POST"])
def edit_appeal(appeal_id):
    if not require_login():
        return redirect(url_for("login"))
    
    if request.method == "POST":
        # Update appeal data
        data = {
            "student_name": request.form.get("student_name", "").strip(),
            "student_id": request.form.get("student_id", "").strip(),
            "violation_id": request.form.get("violation_id", "").strip(),
            "appeal_date": request.form.get("appeal_date", "").strip(),
            "reason": request.form.get("reason", "").strip(),
            "status": request.form.get("status", "Pending Review"),
            "submitted_by": request.form.get("submitted_by", "").strip(),
            "priority": request.form.get("priority", "Medium"),
        }
        
        if not data["student_name"] or not data["student_id"] or not data["violation_id"]:
            flash("Student, ID and Violation ID are required", "error")
        else:
            # Update in Firebase
            success = update_appeal_in_firebase(appeal_id, data)
            if success:
                flash("Appeal updated successfully", "success")
            else:
                flash("Failed to update appeal", "error")
        return redirect(url_for("appeals_page"))
    
    # Get appeal details for editing
    appeal = search_in_firebase("appeals", "id", appeal_id)
    if not appeal:
        flash("Appeal not found", "error")
        return redirect(url_for("appeals_page"))
    
    return render_template("edit_appeal.html", appeal=appeal[0], user=session.get("user"))


@app.route("/appeals/delete/<appeal_id>", methods=["POST"])
def delete_appeal(appeal_id):
    if not require_login():
        return redirect(url_for("login"))
    
    # Delete appeal from Firebase
    success = delete_appeal_from_firebase(appeal_id)
    if success:
        flash("Appeal deleted successfully", "success")
    else:
        flash("Failed to delete appeal", "error")
    
    return redirect(url_for("appeals_page"))


@app.route("/designs", methods=["GET", "POST"])
def designs_page():
    if not require_login():
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        typ = request.form.get("type", "").strip()
        course = request.form.get("course", "").strip()
        colors = request.form.get("colors", "").strip()
        submitted_date = request.form.get("submitted_date", "").strip()
        status = request.form.get("status", "Under Review")
        designer = request.form.get("designer", "").strip()
        description = request.form.get("description", "").strip()

        image_url = ""
        file = request.files.get("image")
        if file and file.filename:
            try:
                suffix = os.path.splitext(file.filename)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    file.save(tmp.name)
                    tmp_path = tmp.name
                
                # Upload to Cloudinary instead of Firebase Storage
                public_id = f"design_{name.replace(' ', '_')}_{os.path.basename(tmp_path)}"
                image_url = upload_image_to_cloudinary(tmp_path, public_id)
            except Exception as e:
                print(f"Error uploading image: {e}")
                image_url = ""
            finally:
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass

        data = {
            "name": name,
            "type": typ,
            "course": course,
            "colors": colors,
            "submitted_date": submitted_date,
            "status": status,
            "designer": designer,
            "description": description,
            "image_url": image_url,
        }
        
        # Perform uniqueness analysis
        uniqueness_analysis = analyze_design_uniqueness(data)
        data["uniqueness_analysis"] = uniqueness_analysis
        if not name or not typ:
            flash("Design name and type are required", "error")
        else:
            doc_id = add_to_firebase("uniform_designs", data)
            if doc_id:
                analysis_score = uniqueness_analysis['overall_score']
                analysis_assessment = uniqueness_analysis['overall_assessment']
                flash(f"Design saved (ID: {doc_id}) - Uniqueness: {analysis_score}% ({analysis_assessment})", "success")
            else:
                flash("Failed to save design", "error")
        return redirect(url_for("designs_page"))

    items = get_from_firebase("uniform_designs") or []
    # Add document IDs to items for action buttons
    for i, item in enumerate(items):
        if 'id' not in item:
            item['id'] = f"design_{i}"  # Fallback ID if not available
    return render_template("designs.html", user=session.get("user"), items=items)


@app.route("/designs/view/<design_id>")
def view_design(design_id):
    if not require_login():
        return redirect(url_for("login"))
    
    # Get design details from Firebase
    design = search_in_firebase("uniform_designs", "id", design_id)
    if not design:
        flash("Design not found", "error")
        return redirect(url_for("designs_page"))
    
    return render_template("design_details.html", design=design[0], user=session.get("user"))


@app.route("/designs/edit/<design_id>", methods=["GET", "POST"])
def edit_design(design_id):
    if not require_login():
        return redirect(url_for("login"))
    
    if request.method == "POST":
        # Update design data
        name = request.form.get("name", "").strip()
        typ = request.form.get("type", "").strip()
        course = request.form.get("course", "").strip()
        colors = request.form.get("colors", "").strip()
        submitted_date = request.form.get("submitted_date", "").strip()
        status = request.form.get("status", "Under Review")
        designer = request.form.get("designer", "").strip()
        description = request.form.get("description", "").strip()
        
        # Handle image upload if provided
        image_url = ""
        if request.files.get("image"):
            img = request.files["image"]
            if img and img.filename:
                try:
                    # Save to temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
                        img.save(tmp_file.name)
                        tmp_path = tmp_file.name
                    
                    # Upload to Cloudinary
                    public_id = f"design_{design_id}_{int(time.time())}"
                    image_url = upload_image_to_cloudinary(tmp_path, public_id)
                    
                    # Clean up temporary file
                    try:
                        os.unlink(tmp_path)
                    except Exception:
                        pass
                except Exception as e:
                    print(f"Error uploading image: {e}")
                    flash("Error uploading image", "error")
        
        data = {
            "name": name,
            "type": typ,
            "course": course,
            "colors": colors,
            "submitted_date": submitted_date,
            "status": status,
            "designer": designer,
            "description": description,
        }
        
        # Only update image_url if a new image was uploaded
        if image_url:
            data["image_url"] = image_url
        
        if not name or not typ:
            flash("Design name and type are required", "error")
        else:
            # Update in Firebase
            success = update_design_in_firebase(design_id, data)
            if success:
                flash("Design updated successfully", "success")
            else:
                flash("Failed to update design", "error")
        return redirect(url_for("designs_page"))
    
    # Get design details for editing
    design = search_in_firebase("uniform_designs", "id", design_id)
    if not design:
        flash("Design not found", "error")
        return redirect(url_for("designs_page"))
    
    return render_template("edit_design.html", design=design[0], user=session.get("user"))


@app.route("/designs/delete/<design_id>", methods=["POST"])
def delete_design(design_id):
    if not require_login():
        return redirect(url_for("login"))
    
    # Delete design from Firebase
    success = delete_design_from_firebase(design_id)
    if success:
        flash("Design deleted successfully", "success")
    else:
        flash("Failed to delete design", "error")
    
    return redirect(url_for("designs_page"))


if __name__ == "__main__":
    import socket
    import os
    
    # Get configuration from environment variables or use defaults
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', os.environ.get('FLASK_PORT', 5000)))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Production mode detection
    is_production = os.environ.get('ENVIRONMENT') == 'production'
    
    # Get local IP address function
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    if is_production:
        # Production settings
        app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
        debug = False
        print(f"\n🚀 AI-niform Server - Production Mode")
        print(f"🌐 Live at: https://your-domain.com")
    else:
        # Development settings
        local_ip = get_local_ip()
        print(f"\n🚀 AI-niform Server - Development Mode")
        print(f"📡 Host: {host}")
        print(f"🔌 Port: {port}")
        print(f"🐛 Debug: {debug}")
        print(f"\n📱 Access URLs:")
        print(f"   Local: http://localhost:{port}")
        print(f"   Network: http://{local_ip}:{port}")
        print(f"\n💡 For mobile/tablet access:")
        print(f"   1. Connect device to same WiFi network")
        print(f"   2. Open browser and go to: http://{local_ip}:{port}")
        print(f"\n💡 For external internet access:")
        print(f"   1. Configure router port forwarding (port {port})")
        print(f"   2. Use your public IP address")
        print(f"\n🛑 Press Ctrl+C to stop the server\n")
    
    # Run the server
    app.run(host=host, port=port, debug=debug, threaded=True)

