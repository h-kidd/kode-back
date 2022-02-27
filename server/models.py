from server import db, ma

# ===============================STUDENT=======================================
# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(65), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), nullable=True )
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=False )
    
     # how object is printed
    def __repr__(self):
        return f"Student('{self.firstname}','{self.lastname} ')"

# Student schema to help jsonify objects
class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "firstname", "lastname", "exercise_id", "teacher_id")
student_schema = StudentSchema(many = False)
students_schema = StudentSchema(many = True)

# ===============================TEACHERS=======================================
# Teacher and Student relationship: one to many.
# Teacher model
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(65), nullable=False)
    #students attribute has relationship to Student model,
    #backref is similar to adding another column to the Student model.
    #Allows when there is a teacher, use student attribute to get the Student
    #linked to teacher. Lazy arg is used to load necessary data in one go.
    students = db.relationship("Student", backref="teacher", lazy=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Teacher('{self.firstname}','{self.lastname} ')"
# Teacher schema
class TeachersSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "firstname", "lastname")
teacher_schema = TeachersSchema(many = False)
teachers_schema = TeachersSchema(many = True)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship("Student", backref="exercise", lazy=True)
    topic = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Exercise('{self.completed}','{self.score} ')"
 
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    question = db.Column(db.ARRAY(db.String), server_default="{}")
    answer = db.Column(db.ARRAY(db.String), server_default="{}")
    options = db.Column(db.ARRAY(db.String), server_default="{}")
    

    def __repr__(self):
        return f"Question('{self.topic}','{self.difficulty} ','{self.question} ','{self.answer} ','{self.options} ')"
    