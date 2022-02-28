from flask_jwt_extended import create_access_token, unset_jwt_cookies,  set_access_cookies, get_jwt, get_jwt_identity, jwt_required
from flask import jsonify, request
from server import jwt, app, db
from server.models import Student ,Teacher, Question, Exercise
from datetime import timedelta, timezone, datetime
from server.models import student_schema, students_schema, teacher_schema, teachers_schema

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Student.query.filter_by(id=identity).one_or_none() or Teacher.query.filter_by(id=identity).one_or_none()


# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    return {'message': 'Hello!'}


# Using an `after_request` callback, we refresh any token that is within 30
# minutes of expiring. Change the timedeltas to match the needs of your application.
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/token", methods=["POST"])
def token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = Student.query.filter_by(username=username).one_or_none() or Teacher.query.filter_by(username=username).one_or_none()
    if not user or not user.verify_password(password):
        return jsonify("Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
# =================================STUDENT ROUTE========================

#Get all Students
@app.route('/students', methods=['GET'])
def get_all_students():
    all_students = Student.query.all()
    result_set = students_schema.dump(all_students)
    return jsonify(result_set)

# Get student id route
@app.route('/students/<int:id>', methods=["GET"])
def get_student(id):
    student_data = Student.query.get_or_404(int(id))
    return student_schema.jsonify(student_data)

# Create new student route
@app.route("/students", methods=["POST"])
def create_student():
    try: 
        username = request.json["username"]
        password = request.json["password"]
        firstname = request.json["firstname"]
        lastname = request.json["lastname"]
        teacher_id = request.json["teacher_id"]
        
        new_student = Student(username = username, password = password, firstname = firstname, lastname = lastname, teacher_id=teacher_id)
        db.session.add(new_student)
        db.session.commit()

        return student_schema.jsonify(new_student)
    except Exception as e:
        return jsonify({"Error" : "Can't create"})


# Update student
@app.route("/students/<int:id>", methods=["PATCH"])
def update_student(id):
    get_student = Student.query.get_or_404(int(id))
    
    username = request.json["username"]
    password = request.json["password"]
    firstname = request.json["firstname"]
    lastname = request.json["lastname"]
    teacher_id = request.json["teacher_id"]

    get_student.username = username
    get_student.password = password
    get_student.firstname = firstname
    get_student.lastname = lastname
    get_student.teacher_id = teacher_id

    db.session.commit()

    return student_schema.jsonify(get_student)
# Delete student
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    get_student = Student.query.get_or_404(int(id))
    db.session.delete(get_student)
    db.session.commit()
    return jsonify({"Success": "deleted"})

# =================================TEACHER ROUTE========================
# get all teachers route
@app.route('/teachers', methods=['GET'])
def get_all_teachers():
    all_teachers = Teacher.query.all()
    result = teachers_schema.dump(all_teachers)
    return jsonify(result)

# Get teacher id route
@app.route('/teachers/<int:id>')
def get_teacher(id):
    teacher_data = Teacher.query.get_or_404(int(id))
    return teacher_schema.jsonify(teacher_data)

@app.route("/teachers/<int:id>/class")
def get_teacher_class(id):
    # result = db.session.query(Student, Teacher).join(Teacher).filter(Teacher.id == id).all()
    result = db.session.query(Teacher.firstname, Teacher.id, Student.id, Student.firstname, Student.lastname, Student.username, Student.password_hashed, Student.lastname, Student.exercise_id, Student.teacher_id).join(Teacher).filter(Teacher.id == id).all()
    return teachers_schema.jsonify(result)

# Create teacher route
@app.route("/teachers", methods=["POST"])
def create_teacher():
    try: 
        username = request.json["username"]
        password = request.json["password"]
        firstname = request.json["firstname"]
        lastname = request.json["lastname"]
        
        new_teacher = Teacher(username = username, password = password, firstname = firstname, lastname = lastname)
        db.session.add(new_teacher)
        db.session.commit()

        return student_schema.jsonify(new_teacher)
    except Exception as e:
        return jsonify({"Error" : "Can't create teacher"})

# Update teacher route
@app.route("/teachers/<int:id>", methods=["PATCH"])
def update_teacher(id):
    get_teacher = Teacher.query.get_or_404(int(id))
    
    username = request.json["username"]
    password = request.json["password"]
    firstname = request.json["firstname"]
    lastname = request.json["lastname"]

    get_teacher.username = username
    get_teacher.password = password
    get_teacher.firstname = firstname
    get_teacher.lastname = lastname

    db.session.commit()

    return student_schema.jsonify(get_teacher)


