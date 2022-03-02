from dataclasses import fields
from server import db, ma
from werkzeug.security import generate_password_hash, check_password_hash

class Association(db.Model):

    student_id = db.Column(db.ForeignKey('student.id'), primary_key=True)
    exercise_id = db.Column(db.ForeignKey('exercise.id'), primary_key=True)
    completed= db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    exercise = db.relationship('Exercise', back_populates='students')
    student = db.relationship('Student', back_populates='exercises')

class StudentexerciseSchema(ma.Schema):
    class Meta:
        fields = ("student_id", "exercise_id")
studentsexercise_schema = StudentexerciseSchema(many = True)

# ===============================STUDENT=======================================
# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hashed = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    # exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), nullable=True )
    #backref makes students column in exercise table
    exercises = db.relationship("Association", back_populates="student")
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=False )

    #password stuff
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    @password.setter
    def password(self,password):
        self.password_hashed = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hashed, password)
    
     # how object is printed
    def __repr__(self):
        return f"Student('{self.firstname}','{self.lastname} ')"

# Student schema to help jsonify objects
class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password_hashed", "firstname", "lastname","teacher_id")
student_schema = StudentSchema(many = False)
students_schema = StudentSchema(many = True)

# ===============================TEACHERS=======================================
# Teacher and Student relationship: one to many.
# Teacher model
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password_hashed = db.Column(db.String(128), nullable=False)
    #students attribute has relationship to Student model,
    #backref is similar to adding another column to the Student model.
    #Allows when there is a teacher, use student attribute to get the Student
    #linked to teacher. Lazy arg is used to load necessary data in one go.
    students = db.relationship("Student", backref="teacher", lazy=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)

    #password stuff
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute!')
    @password.setter
    def password(self,password):
        self.password_hashed = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hashed, password)

    def __repr__(self):
        return f"Teacher('{self.firstname}','{self.lastname} ')"
# Teacher schema
class TeachersSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password_hashed", "firstname", "lastname")
teacher_schema = TeachersSchema(many = False)
teachers_schema = TeachersSchema(many = True)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship("Association", back_populates="exercise")
    topic = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Exercise('{self.completed}','{self.score} ')"

class ExerciseSchema(ma.Schema):
    class Meta:
        fields = ("id", "topic", "difficulty", "completed", "score")
exercisesSchema = ExerciseSchema(many = True)
 
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    question = db.Column(db.ARRAY(db.String), server_default="{}")
    answer = db.Column(db.ARRAY(db.String), server_default="{}")
    options = db.Column(db.ARRAY(db.String), server_default="{}")
    

    def __repr__(self):
        return f"Question('{self.topic}','{self.difficulty} ','{self.question} ','{self.answer} ','{self.options} ')"


class AssociationSchema(ma.Schema):
    class Meta:
        fields = ("username", "firstname", "lastname", "exercise_id","completed","score", "topic")
teacherClass_schema = AssociationSchema(many=True)

    
class StudentExercise(ma.Schema):
    class Meta:
        fields = ("student_id", "exercise_id","completed","score", "topic", "difficulty")
studentExercises_schema = StudentExercise(many=True)
studentoneExercises_schema = StudentExercise(many=False)


class CompleteExercise(ma.Schema):
        class Meta:
            fields = ("student_id", "exercise_id","completed","score")
completeExercise_schema = StudentExercise(many=True)

class QuestionSchema(ma.Schema):
    class Meta:
        fields = ("id", "topic", "difficulty", "question", "answer", "options")
questions_schema = QuestionSchema(many=True)