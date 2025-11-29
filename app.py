import os
import jwt
import datetime
from flask import Flask, request, jsonify, g,render_template
import mysql.connector
from mysql.connector import Error
from bcrypt import hashpw, gensalt, checkpw
from functools import wraps
from datetime import date, datetime, time, timedelta
import base64
import uuid
import os
import json 
import base64
import cv2
import numpy as np
import face_recognition
from io import BytesIO
from PIL import Image
import base64
import numpy as np
import face_recognition
import cv2
from PIL import Image
from io import BytesIO
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# --- Flask Application Initialization ---
app = Flask(__name__)

# --- Configuration ---
# IMPORTANT: Replace with your actual database credentials
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'attendance' # Ensure this database exists and tables are created

# IMPORTANT: Use a strong, random secret key for JWT in production
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'supersecretkeythatshouldbechanged')
app.config['JWT_EXPIRATION_DAYS'] = 7 # Token valid for 7 days

# --- Database Connection Management ---

def get_db():
    """
    Establishes a database connection if one is not already present in the global context.
    """
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DB']
            )
            g.cursor = g.db.cursor(dictionary=True) # Return rows as dictionaries
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            # In a real application, you might want to log this error and return a 500
            raise
    return g.db, g.cursor

@app.teardown_appcontext
def close_db(e=None):
    """
    Closes the database connection at the end of the request.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

# --- JWT Authentication Decorator ---

def jwt_required(f):
    """
    Decorator to protect API endpoints, requiring a valid JWT token.
    Extracts user_id from the token and makes it available in g.current_user.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            print(request.headers['Authorization'],"dsf")
            token = request.headers['Authorization'].split(" ")[1] # Bearer <token>
            print(token,"gg")


        try:
            # Decode the token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            g.current_user = data['user_id'] # Store user_id in global context
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        except Exception as e:
            return jsonify({"error": f"Token error: {str(e)}"}), 401

        return f(*args, **kwargs)
    return decorated

# --- Helper Functions (for ML Integration - Placeholder) ---


import base64
from io import BytesIO
from PIL import Image
import numpy as np
import face_recognition

# ---------------------------------------------------
# 1️⃣ Generate and store embeddings
# ---------------------------------------------------
def generate_face_embedding(image_data):
    """
    Generate a normalized face embedding vector (float32 bytes).
    """
    print("Generating face embedding from image")

    try:
        # Decode base64 image
        header, encoded = image_data.split(',', 1) if ',' in image_data else ('', image_data)
        img_bytes = base64.b64decode(encoded)

        # Open and convert to RGB
        img = Image.open(BytesIO(img_bytes)).convert('RGB')
        img_np = np.array(img)

        # Detect faces
        face_locations = face_recognition.face_locations(img_np, model='hog')
        if len(face_locations) != 1:
            print("Expected exactly one face, found:", len(face_locations))
            return None

        # Compute embedding (128D)
        face_encodings = face_recognition.face_encodings(img_np, face_locations, model='large')
        if not face_encodings:
            print("Failed to compute face encoding")
            return None

        embedding = face_encodings[0].astype(np.float32)  # use float32
        embedding = embedding / np.linalg.norm(embedding)  # L2 normalize

        # Serialize to bytes for DB
        return embedding.tobytes()

    except Exception as e:
        print("Error generating face embedding:", e)
        return None


# ---------------------------------------------------
# 2️⃣ Recognize faces
# ---------------------------------------------------
def recognize_face(image_data, class_id):
    print("Running face recognition")

    try:
        # Decode base64 image to RGB numpy array
        header, encoded = image_data.split(',', 1) if ',' in image_data else ('', image_data)
        img_bytes = base64.b64decode(encoded)
        img = Image.open(BytesIO(img_bytes)).convert("RGB")
        img_np = np.array(img)
    except Exception as e:
        print("Failed to decode image:", e)
        return []

    # Detect face(s)
    face_locations = face_recognition.face_locations(img_np, model='hog')
    if not face_locations:
        print("No faces detected.")
        return []

    face_encodings = face_recognition.face_encodings(img_np, face_locations, model='large')
    if not face_encodings:
        print("Failed to compute face encoding.")
        return []

    # Load known student embeddings
    db, cursor = get_db()
    cursor.execute("SELECT id, face_embedding FROM student WHERE class_id = %s", (class_id,))
    records = cursor.fetchall()
    if not records:
        print("No known embeddings for this class.")
        return []

    known_ids = []
    known_embeddings = []

    for rec in records:
        sid = rec['id']
        blob = rec['face_embedding']

        # Decode embedding as float32
        emb = np.frombuffer(blob, dtype=np.float32)
        if emb.size != 128:
            print(f"Invalid embedding size for student {sid}: {emb.size}")
            continue

        # Normalize to unit length
        emb = emb / np.linalg.norm(emb)

        known_ids.append(sid)
        known_embeddings.append(emb)

    if not known_embeddings:
        print("No valid embeddings found in DB.")
        return []

    known_embeddings = np.array(known_embeddings)

    recognized_students = []

    for encoding in face_encodings:
        encoding = encoding.astype(np.float32)
        encoding = encoding / np.linalg.norm(encoding)

        # Compute Euclidean distance
        distances = np.linalg.norm(known_embeddings - encoding, axis=1)
        best_idx = np.argmin(distances)
        best_distance = distances[best_idx]

        # Use tuned threshold (try 0.45–0.55)
        if best_distance < 0.2:
            confidence = 1 - best_distance  # pseudo-confidence
            recognized_students.append({
                "student_id": known_ids[best_idx],
                "confidence": round(float(confidence), 2)
            })

    print("Recognized:", recognized_students)
    return recognized_students

# --- API Endpoints ---

# --- A. Authentication Endpoints ---


# teacher registration
@app.route('/api/register', methods=['POST'])
def register_user():
    """
    Registers a new teacher/user.
    Hashes the password before storing it.
    """
    db, cursor = get_db()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    name = data.get('name')

    if not all([username, password, name]):
        return jsonify({"error": "Username, password, and name are required"}), 400

    try:
        # Hash the password
        hashed_password = hashpw(password.encode('utf-8'), gensalt())

        cursor.execute("INSERT INTO users (username, password_hash, email, name) VALUES (%s, %s, %s, %s)",
                       (username, hashed_password, email, name))
        db.commit()
        user_id = cursor.lastrowid
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            return jsonify({"error": "Username or email already exists"}), 400
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500





# teacher login
@app.route('/api/login', methods=['POST'])
def login_user():
    """
    Authenticates a user and returns a JWT token upon successful login.
    """
    db, cursor = get_db()
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"error": "Username and password are required"}), 400

    try:
        cursor.execute("SELECT id, password_hash, username, name FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            # Generate JWT token
            token_payload = {
                'user_id': user['id'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=app.config['JWT_EXPIRATION_DAYS'])
            }
            token = jwt.encode(token_payload, app.config['SECRET_KEY'], algorithm="HS256")

            return jsonify({
                "message": "Login successful",
                "token": token,
                "user": {"id": user['id'], "username": user['username'], "name": user['name']}
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500





# teacher logout
@app.route('/api/logout', methods=['POST','GET'])

def logout_user():
    """
    Placeholder for logout. With JWT, client-side token deletion is common.
    This endpoint can be used for server-side token invalidation (e.g., blacklist),
    but for simplicity, we'll just confirm logout.
    """
    # In a real app, you might add the token to a blacklist in Redis/DB
    return jsonify({"message": "Logged out successfully"}), 200

# --- B. Class Management Endpoints ---


# teachet dashboard

@app.route('/dashboard')
def dash():
    return render_template('admin/dashboard.html')

@app.route('/dashboard/data', methods=['GET'])
@jwt_required
def dashboard():
    db, cursor = get_db()
    teacher_id = g.current_user
    
    # Format date explicitly for the database 'date' column (YYYY-MM-DD)
    today = datetime.date.today().strftime('%Y-%m-%d')
    first_day_month = datetime.date.today().replace(day=1).strftime('%Y-%m-%d')

    try:
        # 1. Get teacher's classes
        cursor.execute("SELECT id, name FROM classes WHERE teacher_id = %s", (teacher_id,))
        classes_info = cursor.fetchall() 
        class_ids = [row['id'] for row in classes_info]
        
        if not class_ids:
            return jsonify({
                "total_students": 0, "total_classes": 0, "attendance_percent_today": 0.0,
                "new_students": 0, "absent_today": 0, "top_class": {"name": "N/A", "attendance_rate": 0.0},
                "classes_attended_today": 0, # Ensure all metrics are present
                "pending_issues": 0
            })

        placeholders = ','.join(['%s'] * len(class_ids))
        total_classes = len(class_ids)
        class_ids_tuple = tuple(class_ids)

        # A. Total students 
        cursor.execute(
            f"SELECT COUNT(*) AS total_students FROM student WHERE class_id IN ({placeholders})",
            class_ids_tuple
        )
        total_students = cursor.fetchone()['total_students']

        # B. Absent Today (Count of UNIQUE students marked 'Absent' at least once today)
        cursor.execute(
            f"""
            SELECT COUNT(DISTINCT student_id) AS absent_today 
            FROM attendance_records 
            WHERE date=%s AND status='Absent' AND class_id IN ({placeholders})
            """,
            (today, *class_ids_tuple)
        )
        absent_today_count = cursor.fetchone()['absent_today']
        
        # C. Overall Attendance Percentage Today (Needed for reference, but not displayed as a card)
        cursor.execute(
            f"SELECT COUNT(*) AS total_recorded FROM attendance_records WHERE date=%s AND class_id IN ({placeholders})",
            (today, *class_ids_tuple)
        )
        total_recorded = cursor.fetchone()['total_recorded']
        
        cursor.execute(
            f"SELECT COUNT(*) AS present_count FROM attendance_records WHERE date=%s AND status='Present' AND class_id IN ({placeholders})",
            (today, *class_ids_tuple)
        )
        present_count = cursor.fetchone()['present_count']

        attendance_percent_today = 0.0
        if total_recorded and total_recorded > 0:
            attendance_percent_today = round((present_count / total_recorded) * 100, 2)
            
        # D. Classes Attended Today 
        cursor.execute(
            f"""
            SELECT COUNT(DISTINCT CONCAT(class_id, period, subject)) AS classes_attended_today
            FROM attendance_records 
            WHERE date=%s AND class_id IN ({placeholders})
            """,
            (today, *class_ids_tuple)
        )
        classes_attended_today = cursor.fetchone()['classes_attended_today']

        # E. New students this month 
        cursor.execute(
            f"SELECT COUNT(*) AS new_students FROM student WHERE created_at >= %s AND class_id IN ({placeholders})",
            (first_day_month, *class_ids_tuple)
        )
        new_students = cursor.fetchone()['new_students']

        # F. Top class today 
        cursor.execute(f"""
            SELECT 
                c.name,
                (SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END) * 100.0 / 
                 NULLIF(COUNT(ar.id), 0)) AS attendance_rate
            FROM classes c
            LEFT JOIN attendance_records ar 
                ON ar.class_id = c.id 
                AND ar.date = %s 
            WHERE c.id IN ({placeholders})
            GROUP BY c.id, c.name
            ORDER BY attendance_rate DESC
            LIMIT 1
        """, (today, *class_ids_tuple))
        
        top_class_data = cursor.fetchone() 

        # Safe assignment for top_class
        if top_class_data and top_class_data.get('attendance_rate') is not None:
            top_class = {
                "name": top_class_data['name'],
                "attendance_rate": round(top_class_data['attendance_rate'], 2)
            }
        else:
            top_class = {"name": "N/A", "attendance_rate": 0.0}

        # Placeholder for pending issues
        pending_issues = 0

        dashboard_data = {
            "total_students": total_students,
            "total_classes": total_classes,
            "attendance_percent_today": attendance_percent_today,
            "new_students": new_students,
            "absent_today": absent_today_count,
            "classes_attended_today": classes_attended_today, 
            "top_class": top_class,
            "pending_issues": pending_issues
        }

        return jsonify(dashboard_data)

    except Exception as e:
        print(f"CRITICAL Dashboard Error: {str(e)}")
        # Return a robust error response
        return jsonify({"error": f"An unexpected server error occurred: {str(e)}"}), 500


# treacher add class page
@app.route('/add-class')
def add_class():
    """
    Renders the page for adding a new class.
    """
    return render_template("admin/add_class.html")


# teacher add students page
@app.route('/add-students')
def add_students():
    """
    Renders the page for adding students to a class.
    """
    return render_template("admin/add_students.html")


# teacher view classes page
@app.route('/view-classes', methods=['GET'])
def view_classes():
    return render_template("admin/view_classes.html")


# teacher view students page
@app.route("/view-students")
def view_students():
    """
    Renders the page for viewing all students in a class.
    """
    return render_template("admin/view_students.html")




# teacher add class
# 1. Teacher Create Class
@app.route('/api/classes', methods=['POST'])

@jwt_required

def create_class():

    """

    Creates a new class, linking it to the authenticated user (admin/teacher).

    Uses the new columns: academic_year, teacher_name, and subjects_json.

    """

    db, cursor = get_db()

    data = request.get_json()

   

    name = data.get('name')

    academic_year = data.get('academic_year')

    teacher_name = data.get('teacher_name')

    subjects_json = data.get('subjects')



    # 'g.current_user' holds the ID of the authenticated user (the teacher who owns the class)

    teacher_id_from_jwt = g.current_user

    # CORRECTED: Changed 'id' to 'teacher_id_from_jwt' for accurate print statement

    print(f"Creating class for id: {teacher_id_from_jwt}")



    if not all([name, academic_year, teacher_name, subjects_json]):

        return jsonify({"error": "Missing required fields: name, academic year, teacher name, and subjects are required."}), 400



    try:

        # Check for uniqueness based on (name, academic_year) constraint

        # cursor.execute("SELECT id FROM classes WHERE name = %s AND academic_year = %s", (name, academic_year))

        # if cursor.fetchone():

        #     return jsonify({"error": f"Class '{name}' for academic year {academic_year} already exists."}), 409 # 409 Conflict



        # NOTE: Using teacher_id_from_jwt for ownership, and teacher_name (from form) for display.

        sql = """

        INSERT INTO classes (teacher_id, name, academic_year, teacher_name, subjects_json)

        VALUES (%s, %s, %s, %s, %s)

        """

        # CORRECTED: Using teacher_id_from_jwt for the 'teacher_id' column

        cursor.execute(sql, (teacher_id_from_jwt, name, academic_year, teacher_name, subjects_json))

        db.commit()

        class_id = cursor.lastrowid

       

        return jsonify({

            "message": "Class created successfully",

            "class_id": class_id,

            "name": name

        }), 201

       

    except Exception as e:

        db.rollback()

        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    
# 2. Teacher View All Classes
@app.route('/api/classes', methods=['GET'])
@jwt_required
def get_all_classes():
    """
    Retrieves all classes managed by the authenticated user (admin/teacher).
    """
    db, cursor = get_db()
    teacher_id_from_jwt = g.current_user # ID of the authenticated user

    try:
        sql = """
        SELECT 
            id, name, academic_year, teacher_name, subjects_json, teacher_id
        FROM 
            classes 
        WHERE 
            teacher_id = %s -- CORRECTED: Filter by the 'teacher_id' column, not the primary key 'id'
        """
        # CORRECTED: Passing the JWT user ID to filter by the 'teacher_id' column
        cursor.execute(sql, (teacher_id_from_jwt,)) 
        classes = cursor.fetchall()
        
        # NOTE: You may need to load the subjects_json string into a Python list
        # using json.loads(class_item['subjects_json']) before sending to the frontend.
        
        return jsonify({"classes": classes}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# 3. Teacher View Single Class Details
@app.route('/api/classes/<int:class_id>', methods=['GET'])
@jwt_required
def get_class_details(class_id):
    """
    Retrieves details for a specific class, ensuring the user owns it.
    """
    db, cursor = get_db()
    teacher_id_from_jwt = g.current_user

    try:
        sql = """
        SELECT 
            id, name, academic_year, teacher_name, subjects_json, teacher_id
        FROM 
            classes 
        WHERE 
            id = %s AND teacher_id = %s -- CORRECTED: Check class ID AND ownership (teacher_id)
        """
        # CORRECTED: class_id is the first parameter, teacher_id_from_jwt is the second
        cursor.execute(sql, (class_id, teacher_id_from_jwt)) 
        class_details = cursor.fetchone()

        if class_details:
            if 'subjects_json' in class_details and class_details['subjects_json']:
                class_details['subjects'] = json.loads(class_details['subjects_json'])
                del class_details['subjects_json']
                
            return jsonify(class_details), 200
        else:
            return jsonify({"error": "Class not found or you don't have access"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# 4. Teacher Update Class
@app.route('/api/classes/<int:class_id>', methods=['PUT'])
@jwt_required
def update_class(class_id):
    """
    Updates details for an existing class, ensuring the user owns it.
    """
    db, cursor = get_db()
    data = request.get_json()
    
    name = data.get('name')
    academic_year = data.get('academic_year')
    teacher_name = data.get('teacher_name')
    
    # FIX: Correct the key name from 'subjects' to 'subjects_json' to match the JS payload.
    subjects_json = data.get('subjects_json') 

    teacher_id_from_jwt = g.current_user

    if not all([name, academic_year, teacher_name, subjects_json]):
        # This will now only trigger if the required fields are genuinely missing
        return jsonify({"error": "All fields are required for update"}), 400

    try:
        # Check for uniqueness of the NEW name/academic_year combination, excluding the current class
        cursor.execute("SELECT id FROM classes WHERE name = %s AND academic_year = %s AND id != %s", 
                       (name, academic_year, class_id))
        if cursor.fetchone():
            return jsonify({"error": f"Cannot update. Class '{name}' for academic year {academic_year} already exists in another class."}), 409

        sql = """
        UPDATE classes 
        SET 
            name = %s, 
            academic_year = %s, 
            teacher_name = %s, 
            subjects_json = %s
        WHERE 
            id = %s AND teacher_id = %s
        """
        # Ensure 'subjects_json' is passed to the database query
        cursor.execute(sql, (name, academic_year, teacher_name, subjects_json, class_id, teacher_id_from_jwt)) 
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Class not found or you don't have access"}), 404
        else:
            # Requires the 'json' module to be imported at the top of your file: `import json`
            import json 
            return jsonify({
                "message": "Class updated successfully", 
                "class_id": class_id,
                "name": name,
                "subjects": json.loads(subjects_json)
            }), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# 5. Teacher Delete Class
@app.route('/api/classes/<int:class_id>', methods=['DELETE'])
@jwt_required
def delete_class(class_id):
    """
    Deletes a class. Ensures the user owns the class.
    """
    db, cursor = get_db()
    teacher_id_from_jwt = g.current_user

    try:
        sql = "DELETE FROM classes WHERE id = %s AND teacher_id = %s" # CORRECTED: Check class ID AND ownership (teacher_id)
        # CORRECTED: Passed teacher_id_from_jwt for ownership check
        cursor.execute(sql, (class_id, teacher_id_from_jwt))
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Class not found or you don't have access"}), 404
        else:
            return jsonify({"message": "Class deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# --- C. Student Management Endpoints ---


# teacher add student to class
@app.route('/api/classes/<int:class_id>/students', methods=['POST'])
@jwt_required
def add_student_to_class(class_id):
    db, cursor = get_db()
    data = request.get_json()
    name = data.get('name')
    parent_email = data.get('parent_email')
    student_id_number = data.get('student_id_number')
    image_data = data.get('image_data')  # Base64 encoded image string

    teacher_id = g.current_user

    if not all([name, student_id_number, image_data,parent_email]):
        return jsonify({"error": "Name, student ID number,Parent Email and image data are required"}), 400

    try:
        # Verify class ownership
        cursor.execute("SELECT id FROM classes WHERE id = %s AND teacher_id = %s", (class_id, teacher_id))
        if not cursor.fetchone():
            return jsonify({"error": "Class not found or you don't have access"}), 404

        # Generate face embedding
        face_embedding = generate_face_embedding(image_data)
        if face_embedding is None:
            return jsonify({"error": "Failed to generate face embedding from provided image"}), 400

        # Decode base64 image and save to static/uploads
        header, encoded = image_data.split(',', 1) if ',' in image_data else (None, image_data)
        image_bytes = base64.b64decode(encoded)
        filename = f"{uuid.uuid4().hex}.jpg"
        upload_dir = os.path.join('static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        upload_path = os.path.join(upload_dir, filename)
        with open(upload_path, 'wb') as f:
            f.write(image_bytes)

        # Store relative image path for frontend access
        db_image_path = os.path.join('uploads', filename)

        # Insert student with face embedding and image path
        cursor.execute(
            "INSERT INTO student (class_id, name, student_id_number, face_embedding, image_path,parent_email) VALUES (%s, %s, %s, %s, %s,%s)",
            (class_id, name, student_id_number, face_embedding, db_image_path,parent_email)
        )
        db.commit()
        student_id = cursor.lastrowid

        return jsonify({
            "message": "Student added successfully",
            "student_id": student_id,
            "name": name,
            "image_path": db_image_path
        }), 201

    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e) and "student_id_number" in str(e):
            return jsonify({"error": "Student ID number already exists"}), 400
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500




# teacher get students in class
@app.route('/api/classes/<int:class_id>/students', methods=['GET'])
@jwt_required
def get_all_students_in_class(class_id):
    """
    Retrieves a list of all students belonging to a specific class.
    Ensures the teacher owns the class.
    """
    db, cursor = get_db()
    teacher_id = g.current_user

    try:
        # Verify if the class exists and belongs to the current teacher
        cursor.execute("SELECT id FROM classes WHERE id = %s AND teacher_id = %s", (class_id, teacher_id))
        if not cursor.fetchone():
            return jsonify({"error": "Class not found or you don't have access"}), 404

        # Select relevant fields, exclude face_embedding for response
        cursor.execute(
            "SELECT id, name, student_id_number, class_id, image_path,parent_email FROM student WHERE class_id = %s", 
            (class_id,)
        )
        students = cursor.fetchall()

        return jsonify({"students": students}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



# teacher get single student details
@app.route('/api/students/<int:student_id>', methods=['GET'])
@jwt_required
def get_student_details(student_id):
    """
    Retrieves details for a specific student, ensuring the teacher owns the class.
    """
    db, cursor = get_db()
    teacher_id = g.current_user

    try:
        # Join students and classes to verify teacher ownership
        query = """
            SELECT s.id, s.name, s.student_id_number, s.class_id,
                   CASE WHEN s.face_embedding IS NOT NULL THEN TRUE ELSE FALSE END AS face_embedding_exists
            FROM student s
            JOIN classes c ON s.class_id = c.id
            WHERE s.id = %s AND c.teacher_id = %s
        """
        cursor.execute(query, (student_id, teacher_id))
        student_details = cursor.fetchone()

        if student_details:
            return jsonify(student_details), 200
        else:
            return jsonify({"error": "Student not found or you don't have access"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# teacher update student details
@app.route('/api/students/<int:student_id>', methods=['PUT'])
@jwt_required
def update_student_details(student_id):
    """
    Updates details for an existing student. Can also update/re-capture face embedding and image.
    Ensures the teacher owns the class the student belongs to.
    """
    db, cursor = get_db()
    data = request.get_json()
    name = data.get('name')
    parent_email = data.get('parent_email')
    student_id_number = data.get('student_id_number')
    image_data = data.get('image_data')  # Base64 or other format string for new image


    teacher_id = g.current_user


    if not any([name, student_id_number, image_data]):
        return jsonify({"error": "No data provided for update"}), 400


    try:
        # Verify student exists and belongs to a class owned by this teacher
        cursor.execute("""
            SELECT s.id, s.class_id, s.image_path
            FROM student s
            JOIN classes c ON s.class_id = c.id
            WHERE s.id = %s AND c.teacher_id = %s
        """, (student_id, teacher_id))
        student_check = cursor.fetchone()


        if not student_check:
            return jsonify({"error": "Student not found or you don't have access"}), 404


        update_fields = []
        update_values = []


        if name:
            update_fields.append("name = %s")
            update_values.append(name)
        if parent_email:
            update_fields.append("parent_email = %s")
            update_values.append(parent_email)
        if student_id_number:
            update_fields.append("student_id_number = %s")
            update_values.append(student_id_number)


        if image_data:
            # Save new image file from the image_data (base64 or other format)
            # Implement save_image_file() accordingly
            new_image_path = save_image_file(image_data)
            if not new_image_path:
                return jsonify({"error": "Failed to save new image"}), 400


            # Generate new face embedding from image_data
            new_face_embedding = generate_face_embedding(image_data)
            if new_face_embedding is None:
                return jsonify({"error": "Failed to generate new face embedding"}), 400


            update_fields.append("face_embedding = %s")
            update_values.append(new_face_embedding)


            update_fields.append("image_path = %s")
            update_values.append(new_image_path)


        if not update_fields:
            return jsonify({"message": "No valid fields to update"}), 200


        query = f"UPDATE student SET {', '.join(update_fields)} WHERE id = %s"
        update_values.append(student_id)


        cursor.execute(query, tuple(update_values))
        db.commit()


        # Construct updated student info for response
        updated_student = {
            "id": student_id,
            "name": name if name else student_check["name"],
            "parent_email": parent_email if parent_email else student_check["parent_email"],
            "student_id_number": student_id_number if student_id_number else student_check["student_id_number"],
            "image_path": new_image_path if image_data else student_check["image_path"]
        }


        return jsonify({"message": "Student updated successfully", "student": updated_student}), 200

    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e) and "student_id_number" in str(e):
            return jsonify({"error": "Student ID number already exists"}), 400
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# Example helper function (implement saving image files properly)
def save_image_file(image_data):
    """
    Decodes image_data and saves the file to 'static/uploads/', returns relative path.
    """
    import base64
    import uuid
    import os


    try:
        # Expect image_data as "data:image/png;base64,...."
        header, encoded = image_data.split(",", 1)
        file_ext = header.split("/")[1].split(";")[0]  # e.g. png, jpeg


        binary_data = base64.b64decode(encoded)
        filename = f"{uuid.uuid4()}.{file_ext}"
        save_path = os.path.join("static", "uploads", filename)


        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)


        with open(save_path, "wb") as f:
            f.write(binary_data)


        return f"uploads/{filename}"
    except Exception as ex:
        print(f"Error saving image file: {ex}")
        return None


# delete student
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
@jwt_required
def delete_student(student_id):
    """
    Deletes a student and all their associated attendance records (due to CASCADE).
    Ensures the teacher owns the class the student belongs to.
    """
    db, cursor = get_db()
    teacher_id = g.current_user

    try:
        # Verify student exists and belongs to a class owned by the teacher
        cursor.execute("""
            SELECT s.id
            FROM student s
            JOIN classes c ON s.class_id = c.id
            WHERE s.id = %s AND c.teacher_id = %s
        """, (student_id, teacher_id))
        if not cursor.fetchone():
            return jsonify({"error": "Student not found or you don't have access"}), 404

        cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
        db.commit()

        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# --- D. Attendance Endpoints (Live & Manual) ---


@app.route('/attendance-live')
def attendance_live():
    return render_template("admin/attendance_live.html")

@app.route('/track-attendance')
def track_attendance():
    return render_template("admin/track_attendance.html")

@app.route('/get-report')
def report():
    return render_template('admin/report.html')


import datetime # Make sure this is present

@app.route('/api/classes/<int:class_id>/attendance/live', methods=['POST'])
@jwt_required
def mark_attendance_live(class_id):
    db, cursor = get_db()
    data = request.get_json()
    image_data = data.get('image_data')  # Base64 encoded frame
    
    # Extract session details (Period and Subject)
    period = data.get('period')        
    subject = data.get('subject_id')  
    if not subject:
        subject = data.get('subject') # Fallback 

    teacher_id = g.current_user

    # Input validation
    if not image_data:
        return jsonify({"error": "No image data provided"}), 400
    if not period or not subject:
        return jsonify({"error": "Missing 'period' or 'subject' in request data"}), 400

    try:
        # Verify class and teacher access
        cursor.execute("SELECT id FROM classes WHERE id = %s AND teacher_id = %s", (class_id, teacher_id))
        if not cursor.fetchone():
            return jsonify({"error": "Class not found or access denied"}), 404

        # Assume recognize_face is defined and works
        identified_students_ml = recognize_face(image_data, class_id)
        
        identified_student_ids = {student['student_id'] for student in identified_students_ml}

        # Fetch student names
        cursor.execute("SELECT id, name FROM student WHERE class_id = %s", (class_id,))
        students = cursor.fetchall()
        id_to_name = {student['id']: student['name'] for student in students}

        today = datetime.date.today()
        now_time = datetime.datetime.now().time()

        attendance_report = []

        for student_id in identified_student_ids:
            status = "Present"
            name = id_to_name.get(student_id, "Unknown")

            # Check if a record exists for THIS SPECIFIC SESSION (date, period, subject)
            cursor.execute(
                """
                SELECT id 
                FROM attendance_records 
                WHERE student_id = %s 
                  AND class_id = %s 
                  AND date = %s 
                  AND period = %s 
                  AND subject = %s
                """,
                (student_id, class_id, today, period, subject)
            )
            att_rec = cursor.fetchone()

            if att_rec:
                # UPDATE EXISTING RECORD (only if student was marked, e.g., 'Late', or to refresh time)
                cursor.execute("""
                    UPDATE attendance_records
                    SET status = %s, time = %s, recorded_by = %s
                    WHERE id = %s
                """, (status, now_time, teacher_id, att_rec['id']))
            else:
                # INSERT NEW RECORD for this unique session
                cursor.execute("""
                    INSERT INTO attendance_records 
                        (student_id, class_id, date, time, status, recorded_by, period, subject)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (student_id, class_id, today, now_time, status, teacher_id, period, subject))

            attendance_report.append({
                "student_id": student_id,
                "name": name,
                "status": status,
                "period": period,
                "subject": subject
            })

        db.commit()
        
        if not identified_student_ids:
            message = "Face Match Not Found!! Try Again"
        else:
            message = "Attendance processed successfully."

        return jsonify({
            "message": message,
            "identified_students": attendance_report,
            "unidentified_faces": 0
        }), 200

    except Exception as e:
        db.rollback()
        print(f"Error marking attendance: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@app.route('/api/classes/<int:class_id>/attendance/manual', methods=['POST'])
@jwt_required
def mark_attendance_manual(class_id):
    """
    Allows a teacher to manually mark attendance for multiple students.
    """
    db, cursor = get_db()
    data = request.get_json()
    date_str = data.get('date')
    attendance_list = data.get('attendance_list') # List of {'student_id': ..., 'status': ...}

    teacher_id = g.current_user

    if not all([date_str, attendance_list]):
        return jsonify({"error": "Date and attendance list are required"}), 400

    try:
        # Verify if the class exists and belongs to the current teacher
        cursor.execute("SELECT id FROM classes WHERE id = %s AND teacher_id = %s", (class_id, teacher_id))
        if not cursor.fetchone():
            return jsonify({"error": "Class not found or you don't have access"}), 404

        attendance_records_to_insert = []
        current_time = datetime.datetime.now().time()
        attendance_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

        for record in attendance_list:
            student_id = record.get('student_id')
            status = record.get('status')

            if not all([student_id, status]):
                return jsonify({"error": "Each attendance record must have student_id and status"}), 400

            # Optional: Validate student_id belongs to the class
            cursor.execute("SELECT id FROM students WHERE id = %s AND class_id = %s", (student_id, class_id))
            if not cursor.fetchone():
                return jsonify({"error": f"Student ID {student_id} not found in this class"}), 400

            attendance_records_to_insert.append((student_id, class_id, attendance_date, current_time, status, teacher_id))

        # Delete existing records for the given date and class to avoid duplicates on manual override
        cursor.execute("DELETE FROM attendance_records WHERE class_id = %s AND date = %s", (class_id, attendance_date))
        db.commit() # Commit delete before insert

        insert_query = """
            INSERT INTO attendance_records (student_id, class_id, date, time, status, recorded_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, attendance_records_to_insert)
        db.commit()

        return jsonify({"message": "Attendance updated successfully", "records_updated": len(attendance_records_to_insert)}), 200
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"An unexpected error occurred during manual attendance: {str(e)}"}), 500

# --- E. Reporting and Tracking Endpoints ---
from flask import request, jsonify, g
from datetime import date, datetime, time, timedelta

# Assuming get_db(), app, and jwt_required are defined

@app.route('/api/classes/<int:class_id>/attendance', methods=['GET'])
@jwt_required
def get_attendance_report_for_class(class_id):
    """
    Retrieves attendance records for a class with optional filters,
    including period and subject, and properly serializes datetime fields.
    """
    
    try:
        db, cursor = get_db() 
        teacher_id = g.current_user

        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        period_filter = request.args.get('period')
        subject_filter = request.args.get('subject')
        student_id_filter = request.args.get('student_id', type=int)

        # 1. FIX: Updated Class Verification Query (No JOIN needed for teacher)
        class_verification_query = """
            SELECT 
                c.id, 
                c.name,
                c.teacher_name  -- Selecting teacher_name directly from the class table
            FROM `classes` c  
            -- NO JOIN `teacher` t... needed
            WHERE c.id = %s AND c.teacher_id = %s
        """
        cursor.execute(class_verification_query, (class_id, teacher_id))
        
        class_info = cursor.fetchone()
        
        if not class_info:
            return jsonify({"error": "Class not found or you don't have access"}), 404

        # 2. Attendance Query: Still uses the `student` table which is assumed to exist
        query = """
            SELECT 
                ar.id, 
                ar.student_id, 
                s.name AS student_name, 
                ar.date, 
                ar.time, 
                ar.status, 
                ar.period, 
                ar.subject
            FROM `attendance_records` ar
            JOIN `student` s ON ar.student_id = s.id -- Assuming `student` table still exists
            WHERE ar.class_id = %s
        """
        params = [class_id]

        # Add filters dynamically
        if start_date:
            query += " AND ar.date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND ar.date <= %s"
            params.append(end_date)
        if student_id_filter:
            query += " AND ar.student_id = %s"
            params.append(student_id_filter)
        if period_filter:
            query += " AND ar.period = %s"
            params.append(period_filter)
        if subject_filter:
            query += " AND ar.subject = %s"
            params.append(subject_filter)

        query += " ORDER BY ar.date DESC, ar.time DESC"

        cursor.execute(query, tuple(params))
        attendance_records = cursor.fetchall()

        # 3. Serialization (unchanged)
        for record in attendance_records:
            if isinstance(record['date'], (date, datetime)):
                record['date'] = record['date'].isoformat()

            if isinstance(record['time'], time):
                record['time'] = record['time'].strftime('%H:%M:%S')
            elif isinstance(record['time'], timedelta):
                total_seconds = int(record['time'].total_seconds())
                hours = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                seconds = total_seconds % 60
                record['time'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            else:
                if record['time'] is None:
                    record['time'] = ''

        return jsonify({
            "class_id": class_info['id'],
            "class_name": class_info['name'],
            "teacher_name": class_info['teacher_name'],
            "attendance_records": attendance_records
        }), 200

    except Exception as e:
        print(f"Error fetching attendance report: {str(e)}")
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500 
    
@app.route('/api/classes/<int:class_id>/attendance/summary', methods=['GET'])
@jwt_required
def get_attendance_summary_for_class(class_id):
    """
    Provides a summary of attendance (e.g., total present/absent counts) 
    for a class over a period, based on recorded session entries.
    """
    db, cursor = get_db()
    teacher_id = g.current_user

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        # Verify if the class exists and belongs to the current teacher
        cursor.execute("SELECT id, name FROM classes WHERE id = %s AND teacher_id = %s", (class_id, teacher_id))
        class_info = cursor.fetchone()
        if not class_info:
            return jsonify({"error": "Class not found or you don't have access"}), 404

        # 1. NEW: Calculate the total number of *unique recorded sessions* # (date, period, subject) in the attendance_records table for this class/period.
        # This acts as the total baseline for percentage calculation.
        session_query = """
            SELECT COUNT(DISTINCT CONCAT(date, ' ', period, ' ', subject)) AS total_recorded_sessions 
            FROM attendance_records 
            WHERE class_id = %s
        """
        session_params = [class_id]

        if start_date:
            session_query += " AND date >= %s"
            session_params.append(start_date)
        if end_date:
            session_query += " AND date <= %s"
            session_params.append(end_date)
            
        cursor.execute(session_query, tuple(session_params))
        total_recorded_sessions = cursor.fetchone()['total_recorded_sessions']
        
        # 2. Get attendance counts per student
        summary_query = """
            SELECT
                s.id AS student_id,
                s.name AS student_name,
                -- Count statuses ONLY where the date range criteria are met
                SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END) AS present_count,
                SUM(CASE WHEN ar.status = 'Absent' THEN 1 ELSE 0 END) AS absent_count,
                SUM(CASE WHEN ar.status = 'Late' THEN 1 ELSE 0 END) AS late_count,
                COUNT(ar.id) AS total_recorded_statuses_for_student
            FROM student s
            -- LEFT JOIN to ensure students with NO attendance records still appear
            LEFT JOIN attendance_records ar ON s.id = ar.student_id AND ar.class_id = %s
            WHERE s.class_id = %s -- Filter students only from this class
        """
        summary_params = [class_id, class_id]

        # 3. Apply date filters directly in the WHERE clause on the student table result set
        # Note: If ar.date is NULL (because of LEFT JOIN), these filters skip those students.
        if start_date:
            summary_query += " AND ar.date >= %s"
            summary_params.append(start_date)
        if end_date:
            summary_query += " AND ar.date <= %s"
            summary_params.append(end_date)
        
        summary_query += " GROUP BY s.id, s.name ORDER BY s.name ASC"

        cursor.execute(summary_query, tuple(summary_params))
        student_summaries = cursor.fetchall()

        # 4. Calculate percentages
        for student in student_summaries:
            # We use the total number of times this student was marked (Present/Absent/Late)
            # as the baseline for their percentage calculation, as we cannot determine 
            # the total expected sessions without a separate schedule table.
            
            total_recorded_statuses = student['total_recorded_statuses_for_student']
            
            if total_recorded_statuses > 0:
                student['present_percentage'] = round((student['present_count'] / total_recorded_statuses) * 100, 2)
            else:
                student['present_percentage'] = 0.0

            # Clean up the unnecessary calculated field for the final JSON output
            del student['total_recorded_statuses_for_student'] 

        return jsonify({
            "class_id": class_info['id'],
            "class_name": class_info['name'],
            "summary": {
                "total_recorded_sessions_in_range": total_recorded_sessions, # Now more accurately named
                "student": student_summaries
            }
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred while fetching summary: {str(e)}"}), 500



@app.route("/")
def index():
    return render_template("index.html")



@app.route("/about")
def about():    
    return render_template("about.html")

@app.route("/contact")
def contact():  
    return render_template("contact.html")

@app.route("/login")
def login():    
    return render_template("login.html")

@app.route("/register")
def register():     
    return render_template("register.html")


@app.route('/student-attendence')
def student_attendence():
    return render_template('attendence.html')



import datetime # Ensure 'datetime' is imported

@app.route('/api/classes/<int:class_id>/attendance/absent', methods=['POST'])
@jwt_required
def get_absent_students(class_id):
    """
    Returns a list of students who were NOT marked present for the specific 
    period and subject today.
    NOTE: The method is changed to POST to receive period/subject data in the body.
    """
    db, cursor = get_db()
    teacher_id = g.current_user
    today_date = datetime.date.today().isoformat()  # YYYY-MM-DD

    # 1. Get period and subject from the POST request body
    data = request.get_json()
    period = data.get('period')
    subject = data.get('subject_id')
    if not subject:
        subject = data.get('subject') # Fallback if frontend uses 'subject' key

    if not period or not subject:
        return jsonify({"error": "Missing 'period' or 'subject' in request data."}), 400

    try:
        # Verify class ownership
        cursor.execute(
            "SELECT id, name FROM classes WHERE id = %s AND teacher_id = %s",
            (class_id, teacher_id)
        )
        class_info = cursor.fetchone()
        if not class_info:
            return jsonify({"error": "Class not found or you don't have access"}), 404

        # Get all students in the class
        cursor.execute("SELECT id, name FROM student WHERE class_id = %s", (class_id,))
        all_students = cursor.fetchall()

        # 2. Query for students marked 'Present' or 'Late' for TODAY, THIS PERIOD, and THIS SUBJECT
        cursor.execute(
            """
            SELECT student_id 
            FROM attendance_records 
            WHERE class_id = %s 
              AND date = %s 
              AND period = %s
              AND subject = %s
              AND status IN ('Present', 'Late') 
            """,
            (class_id, today_date, period, subject)
        )
        present_or_marked_students = {row['student_id'] for row in cursor.fetchall()}

        # 3. Compute absent students (those in class but not in the present/late set)
        absent_students = [
            {'student_id': s['id'], 'name': s['name']} 
            for s in all_students 
            if s['id'] not in present_or_marked_students
        ]

        # Return session details along with the list for the confirmation step
        return jsonify({
            "absent_students": absent_students, 
            "period": period, 
            "subject": subject
        }), 200

    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    

from datetime import date # Assuming date is imported

@app.route('/api/classes/<int:class_id>/attendance/absent/confirm', methods=['POST'])
@jwt_required
def confirm_absent_students(class_id):
    """
    Marks the list of absent students (for the specified period/subject) 
    in the attendance_records table and sends emails to parents.
    """
    db, cursor = get_db()
    teacher_id = g.current_user
    today_date = date.today().isoformat()
    
    data = request.get_json()
    absent_students_list = data.get('absent_students', []) # List of {'student_id': X, 'name': Y}
    period = data.get('period')
    subject = data.get('subject') # Subject name string

    if not period or not subject:
        return jsonify({"error": "Missing 'period' or 'subject' in request data."}), 400
        
    if not absent_students_list:
        # If the list is empty, simply return success (all students present)
        return jsonify({"message": "No absent students to record for this session."}), 200

    try:
        # 1. Verify class ownership
        cursor.execute(
            "SELECT id FROM classes WHERE id = %s AND teacher_id = %s",
            (class_id, teacher_id)
        )
        if not cursor.fetchone():
            return jsonify({"error": "Class not found or you don't have access"}), 404

        recorded_absent_count = 0
        emails_to_send = []

        # 2. Process each student marked absent by the previous endpoint
        for student_data in absent_students_list:
            s_id = student_data['student_id']
            s_name = student_data['name']
            
            # --- CRITICAL FIX: Check if the record already exists for THIS PERIOD/SUBJECT ---
            cursor.execute(
                """
                SELECT id 
                FROM attendance_records 
                WHERE student_id = %s AND class_id = %s AND date = %s 
                  AND period = %s AND subject = %s
                """,
                (s_id, class_id, today_date, period, subject)
            )
            
            if not cursor.fetchone():
                # Record doesn't exist, insert the new 'Absent' record
                cursor.execute(
                    """
                    INSERT INTO attendance_records 
                    (student_id, class_id, date, period, subject, status) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (s_id, class_id, today_date, period, subject, 'Absent')
                )
                recorded_absent_count += 1
                
                # Fetch parent email for the absent student (if not already fetched)
                # Note: You might need to adjust how you get parent_email efficiently
                cursor.execute("SELECT parent_email FROM student WHERE id = %s", (s_id,))
                parent_info = cursor.fetchone()
                if parent_info and parent_info.get('parent_email'):
                    emails_to_send.append({
                        'name': s_name, 
                        'email': parent_info['parent_email']
                    })

        db.commit()

        # 3. Send emails to parents for newly recorded absentees
        for student in emails_to_send:
            send_absent_email(student['name'], student['email'], today_date)

        return jsonify({
            "message": f"Attendance finalized. {recorded_absent_count} students marked Absent for {subject}, {period}.",
            "absent_count": recorded_absent_count
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Unexpected error during finalization: {str(e)}"}), 500
    
def send_absent_email(student_name, parent_email, date_str):
    """
    Sends email notification to parent about absent student.
    """
    sender_email = "educareattendance26@gmail.com"
    sender_password = "rsnm quox hhmo kifa"  # Use app password for Gmail
    subject = f"Attendance Alert: {student_name} Absent on {date_str}"

    body = f"""
    Dear Parent,

    This is to inform you that your child, {student_name}, was marked as absent on {date_str}.

    Regards,
    School Administration
    """

    # Create MIME message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = parent_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Send email via SMTP (example for Gmail)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {parent_email}")
    except Exception as e:
        print(f"Failed to send email to {parent_email}: {e}")




# Assume 'get_db()' and necessary imports like 'db, cursor' are defined elsewhere

@app.route('/api/check_attendance', methods=['POST'])
def check_attendance():
    """
    Returns detailed attendance summary for a student, aggregated by Class, Subject, Period, and Teacher.
    Fixes Table 'attendance.user' doesn't exist error by using 'users' table name.
    """
    try:
        db, cursor = get_db()
        data = request.get_json()

        if not data or 'student_id' not in data:
            return jsonify({"error": "Missing student_id"}), 400

        student_id = data['student_id']

        # 1. Fetch student internal ID
        # Assumes 'student' table has id (PK), name, and student_id_number
        cursor.execute("SELECT id, name FROM student WHERE student_id_number = %s", (student_id,))
        student = cursor.fetchone()
        if not student:
            return jsonify({"error": "Student not found"}), 404
        
        student_pk_id = student['id']

        # 2. Fetch Detailed Attendance Summaries grouped by Class, Subject, Period, and Teacher.
        cursor.execute("""
            SELECT
                c.name AS class_name,
                ar.subject, 
                ar.period, 
                u.name AS teacher_name, -- Teacher name for 'Attendance Taken By' from the 'users' table
                COUNT(ar.id) AS total_days,
                SUM(CASE WHEN ar.status = 'Present' THEN 1 ELSE 0 END) AS present_days,
                SUM(CASE WHEN ar.status = 'Absent' THEN 1 ELSE 0 END) AS absent_days
            FROM attendance_records ar
            INNER JOIN classes c ON ar.class_id = c.id
            LEFT JOIN users u ON ar.recorded_by = u.id -- *** CRITICAL FIX: Changed 'user' to 'users' ***
            WHERE ar.student_id = %s 
            GROUP BY c.name, ar.subject, ar.period, u.name
            ORDER BY c.name, ar.period, ar.subject;
        """, (student_pk_id,))
        
        detailed_summaries = cursor.fetchall()

        if not detailed_summaries:
            return jsonify({"error": "No detailed attendance records found for this student"}), 404

        # 3. Calculate Overall Summary and Format Output
        overall_total = sum(s['total_days'] for s in detailed_summaries)
        overall_present = sum(s['present_days'] for s in detailed_summaries)
        overall_absent = overall_total - overall_present
        overall_percent = round((overall_present / overall_total) * 100, 2) if overall_total > 0 else 0.0

        class_wise_summary = []
        for session in detailed_summaries:
            total_days = session['total_days'] or 0
            present_days = session['present_days'] or 0
            
            percent = round((present_days / total_days) * 100, 2) if total_days > 0 else 0.0

            class_wise_summary.append({
                "class_name": session['class_name'],
                "subject": session['subject'] or 'N/A',
                "period": session['period'] or 'N/A',
                "teacher_name": session['teacher_name'] or 'N/A', 
                "total_days": total_days,
                "present_days": present_days,
                "absent_days": session['absent_days'] or 0,
                "attendance_percentage": percent
            })

        # 4. Prepare the final JSON response
        return jsonify({
            "student_id": student_id,
            "student_name": student['name'],
            "overall_summary": {
                "total_days": overall_total,
                "present_days": overall_present,
                "absent_days": overall_absent,
                "attendance_percentage": overall_percent
            },
            "class_wise_summary": class_wise_summary
        }), 200

    except Exception as e:
        print(f"[ERROR] Attendance fetch error: {str(e)}")
        # If the table name is now correct, this will capture other errors, like the 'No result set to fetch from' error.
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
    
# --- Run the Flask app ---
if __name__ == '__main__':
    # Ensure you have set your environment variables or replaced the placeholders
    # For development, you can run: python app.py
    # For production, use a WSGI server like Gunicorn or uWSGI
    app.run(debug=True, host='0.0.0.0', port=5000)
