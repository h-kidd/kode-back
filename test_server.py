import json
from flask_jwt_extended import create_access_token

def test_home(api):
    res = api.get('/')
    assert res.status == '200 OK'
    assert res.json == {'message': 'Hello!'}

def test_get_teacher(api):
    access_token = create_access_token('jagan123')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.get('/teachers', headers=headers)
    assert res.status == '200 OK'
    assert res.json == {'classes': [{'class': '1', 'students': [
        {'username': 'ZH123', 'firstname': 'Zelda', 'lastname': 'Hyrule', 'teacher': 'jagan123', 'homework': [], 'completed': [{'exercise': 'maths1', 'score': 5}]}
        ]}]}

def test_get_student(api):
    access_token = create_access_token('zh123')
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.get('/students', headers=headers)
    assert res.status == '200 OK'
    assert res.json == {'username': 'zh123', 'firstname': 'Zelda', 'lastname': 'Hyrule', 'teacher': 'jagan123', 'homework': [], 'completed': [{'exercise': 'maths1', 'difficulty': 'easy', 'score': 5}]}

def test_post_student(api):
    data = json.dumps({'firstname': 'Ziggy', 'lastname': 'Beth'})
    access_token = create_access_token('jagan123')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    res = api.post('/students', headers=headers)
    assert res.status == '200 OK'
    assert res.json == {'username': 'zb123', 'firstname': 'Ziggy', 'lastname': 'Beth', 'teacher': 'jagan123', 'homework': [], 'completed': []}

def test_post_login_teacher(api):
    data = json.dumps({'username': 'jagan123', 'password': 'test'})
    headers = {'Content-Type': 'application/json'}
    res = api.post('/login/teacher', data=data, headers=headers)
    access_token = create_access_token('jagan123')
    assert res.status == '200 OK'
    assert res.json == {'accessToken': access_token}

def test_post_login_student(api):
    mock_data = json.dumps({'username': 'zh123', 'password': 'test'})
    mock_headers = {'Content-Type': 'application/json'}
    res = api.post('/login/student', data=mock_data, headers=mock_headers)
    access_token = create_access_token('zh123')
    assert res.status == '200 OK'
    assert res.json == {'accessToken': access_token}

def test_get_questions(api):
    res = api.get('/questions/maths1/easy')
    assert res.status == '200 OK'
    assert res.json == {'questions': [
        {'question': 'How would you get the output to equal 10?', 'answer': ['5*2', '2*5'], 'options': ['5', '/', '4', '*', '2', '+']},
        {'question': 'How would you get the output to equal 10?', 'answer': ['5*2', '2*5'], 'options': ['5', '/', '4', '*', '2', '+']},
        {'question': 'How would you get the output to equal 10?', 'answer': ['5*2', '2*5'], 'options': ['5', '/', '4', '*', '2', '+']}
    ]}

def test_404(api):
    res = api.get('/drftgyhujkl')
    assert res.status == '404 NOT FOUND'

def test_401(api):
    res = api.get('/teachers')
    assert res.status == '401 UNAUTHORIZED'