import json
from flask_jwt_extended import create_access_token

def test_home(api):
    res = api.get('/')
    assert res.status == '200 OK'
    assert res.json == {'message': 'Hello!'}

def test_get_teacher(api):
    #Teacher should be able to get user information, should not return password
    access_token = create_access_token('jagan123')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.get('/teachers', headers=headers)
    assert res.status == '200 OK'
    assert res.json == {'username': 'jagan123', 'firstname': 'Jagan', 'lastname': 'Devaraj', 'classes': [{'class': '1', 'students': [
        {'username': 'zh123', 'firstname': 'Zelda', 'lastname': 'Hyrule', 'teacher': 'jagan123', 'homework': [], 'completed': [{'exercise': 'maths1', 'difficulty': 'easy', 'score': 5}]}
        ]}]}

def test_post_teacher(api):
    #Teacher should be able to register an account
    data = json.dumps({'username': 'jagan123', 'password': 'test', 'firstname': 'Jagan', 'lastname': 'Devaraj'})
    access_token = create_access_token('jagan123')
    headers = {
        'Content-Type': 'application/json',
    }
    res = api.post('/teachers', data=data, headers=headers)
    assert res.status == '201 CREATED'
    assert res.json == {'accessToken': access_token}

def test_get_teacher_class(api):
    #Teacher should be able to get class information
    access_token = create_access_token('jagan123')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.get('/teachers/classes/1', headers=headers)
    assert res.status == '200 OK'
    assert res.json == {'class': '1', 'students': [
        {'username': 'zh123', 'firstname': 'Zelda', 'lastname': 'Hyrule', 'teacher': 'jagan123', 'homework': [], 'completed': [{'exercise': 'maths1', 'difficulty': 'easy', 'score': 5}]}
        ]}

def test_post_teacher_homework(api):
    #Teacher should be able to post homework to class
    data = json.dumps({'exercise': 'maths2', 'difficulty': 'easy'})
    access_token = create_access_token('jagan123')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.post('/teachers/classes/1', data=data, headers=headers)
    assert res.status == '201 CREATED'
    assert res.json == {'class': '1', 'students': [
        {'username': 'zh123', 'firstname': 'Zelda', 'lastname': 'Hyrule', 'teacher': 'jagan123', 'homework': [{'exercise': 'maths2', 'difficulty': 'easy'}], 'completed': [{'exercise': 'maths1', 'difficulty': 'easy', 'score': 5}]}
        ]}

def test_get_teacher_student(api):
    #Teacher should be able to get student information
    access_token = create_access_token('jagan123')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.get('/teachers/classes/1/1', headers=headers)
    assert res.status == '200 OK'
    assert res.json == {'student': {'username': 'zh123', 'firstname': 'Zelda', 'lastname': 'Hyrule', 'teacher': 'jagan123', 'homework': [], 'completed': [{'exercise': 'maths1', 'difficulty': 'easy', 'score': 5}]}}

def test_get_student(api):
    #Student should be able to get user information, should not return password
    access_token = create_access_token('zh123')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.get('/students', headers=headers)
    assert res.status == '200 OK'
    assert res.json == {'username': 'zh123', 'firstname': 'Zelda', 'lastname': 'Hyrule', 'teacher': 'jagan123', 'homework': [{'exercise': 'maths2', 'difficulty': 'easy'}], 'completed': [{'exercise': 'maths1', 'difficulty': 'easy', 'score': 5}]}

def test_post_student(api):
    #Teacher should be able to make a new student
    data = json.dumps({'firstname': 'Ziggy', 'lastname': 'Beth'})
    access_token = create_access_token('jagan123')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.post('/students', data=data, headers=headers)
    assert res.status == '201 CREATED'
    assert res.json == {'username': 'zb123', 'password': 'test', 'firstname': 'Ziggy', 'lastname': 'Beth', 'teacher': 'jagan123', 'homework': [], 'completed': []}

def test_get_student_homework(api):
    #Student should be able to get list of homework
    access_token = create_access_token('zh123')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.get('/students/completed', headers=headers)
    assert res.status == '200 OK'
    assert res.json == {'homework': [{'exercise': 'maths2', 'difficulty': 'easy'}]}

def test_get_student_completed(api):
    #Student should be able to get list of completed exercises
    access_token = create_access_token('zh123')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.get('/students/completed', headers=headers)
    assert res.status == '200 OK'
    assert res.json == {'completed': [{'exercise': 'maths1', 'difficulty': 'easy', 'score': 5}]}

def test_post_student_completed(api):
    #Student should be able to post a completed exercise
    data = json.dumps({'exercise': 'maths2', 'difficulty': 'easy', 'score': 7})
    access_token = create_access_token('zh123')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.post('/students', data=data, headers=headers)
    assert res.status == '201 CREATED'
    assert res.json == {'completed': [{'exercise': 'maths1', 'difficulty': 'easy', 'score': 5}, {'exercise': 'maths2', 'difficulty': 'easy', 'score': 7}]}

def test_patch_student_completed(api):
    #Student should be able to update a previous completed exercises score
    data = json.dumps({'exercise': 'maths1', 'difficulty': 'easy', 'score': 10})
    access_token = create_access_token('zh123')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.patch('/students', data=data, headers=headers)
    assert res.status == '204 NO CONTENT'

def test_post_login_teacher(api):
    #Teacher should be able to log in and recieve jwt
    data = json.dumps({'username': 'jagan123', 'password': 'test'})
    headers = {'Content-Type': 'application/json'}
    res = api.post('/login/teacher', data=data, headers=headers)
    access_token = create_access_token('jagan123')
    assert res.status == '200 OK'
    assert res.json == {'accessToken': access_token}

def test_post_login_teacher_student(api):
    #Student should not be able to login to teacher route
    data = json.dumps({'username': 'zh123', 'password': 'test'})
    headers = {'Content-Type': 'application/json'}
    res = api.post('/login/teacher', data=data, headers=headers)
    assert res.status == '401 UNAUTHORIZED'

def test_post_login_student(api):
    #Student should be able to log in and recieve jwt
    mock_data = json.dumps({'username': 'zh123', 'password': 'test'})
    mock_headers = {'Content-Type': 'application/json'}
    res = api.post('/login/student', data=mock_data, headers=mock_headers)
    access_token = create_access_token('zh123')
    assert res.status == '200 OK'
    assert res.json == {'accessToken': access_token}

def test_post_login_student_teacher(api):
    #Teacher should not be able to login to student route
    data = json.dumps({'username': 'zh123', 'password': 'test'})
    headers = {'Content-Type': 'application/json'}
    res = api.post('/login/student', data=data, headers=headers)
    assert res.status == '401 UNAUTHORIZED'

def test_get_teacher_student(api):
    #Student should be able to acces teachers route
    access_token = create_access_token('zh123')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.get('/teachers', headers=headers)
    assert res.status == '401 UNAUTHORIZED'

def test_get_teacher_student(api):
    #Teacher should be able to acces students route
    access_token = create_access_token('jagan123')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.get('/students', headers=headers)
    assert res.status == '401 UNAUTHORIZED'

def test_get_questions(api):
    #Should be able to access a list of question by subject and difficulty
    res = api.get('/questions/maths1/easy')
    assert res.status == '200 OK'
    assert res.json == {'questions': [
        {'question': ['How would you get the output to equal 10?', '___=10'], 'answer': ['5*2', '2*5'], 'options': ['5', '/', '4', '*', '2', '+']},
        {'question': ['How would you get the output to equal 10?', '___=10'], 'answer': ['5*2', '2*5'], 'options': ['5', '/', '4', '*', '2', '+']},
        {'question': ['How would you get the output to equal 10?', '___=10'], 'answer': ['5*2', '2*5'], 'options': ['5', '/', '4', '*', '2', '+']}
    ]}

def test_404(api):
    #Unknown route should respond with error 404
    res = api.get('/drftgyhujkl')
    assert res.status == '404 NOT FOUND'

def test_401(api):
    #Unauthrized route should respond with eror 401
    res = api.get('/teachers')
    assert res.status == '401 UNAUTHORIZED'