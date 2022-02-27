from server import db, ma


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(65), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey("homework.id"), nullable=False )
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=False )
    # homework_id = db.Column(db.Integer, db.ForeignKey("homework.id"), nullable=False )
    # completed_id = db.Column(db.Integer, db.ForeignKey("completed.id"), nullable=False )

    # homework = db.Column(db.String(10), nullable=False, default="0")
    # completed = db.Column(db.String(10), nullable=False, default="0")

    # how object is printed
    # def __repr__(self):
    #     return f"Student('{self.firstname}','{self.lastname} ')"
    def __init__(self, username, password, firstname, lastname, homework_id, teacher_id):
        self.username = username
        self.password= password
        self.firstname = firstname
        self.lastname = lastname
        self.homework_id= homework_id
        self.teacher_id= teacher_id
    
class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password", "firstname", "lastname", "homework_id", "teacher_id")
student_schema = StudentSchema(many = False)
students_schema = StudentSchema(many = True)

# Teacher and Student relationship: one to many.
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

    # def __repr__(self):
    #     return f"Teacher('{self.firstname}','{self.lastname} ')"
    def __init__(self, username, password, firstname, lastname):
        self.username = username
        self.password= password
        self.firstname = firstname
        self.lastname= lastname


    



class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    students = db.relationship("Student", backref="homework", lazy=True)
    topic = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)

    # def __repr__(self):
    #     return f"Homework('{self.completed}','{self.score} ')"
    def __init__(self, topics, difficulty, completed, score):
        self.topics = topics
        self.difficulty= difficulty
        self.completed = completed
        self.score= score

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(20), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    question = db.Column(db.ARRAY(db.String), server_default="{}")
    answer = db.Column(db.ARRAY(db.String), server_default="{}")
    options = db.Column(db.ARRAY(db.String), server_default="{}")
    

    # def __repr__(self):
    #     return f"Question('{self.topic}','{self.difficulty} ','{self.question} ','{self.answer} ','{self.options} ')"
    def __init__(self, topic, difficulty, question, answer, options):
        self.topics = topic
        self.difficulty= difficulty
        self.question = question
        self.answer= answer
        self.options= options