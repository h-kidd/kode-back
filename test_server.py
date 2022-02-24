import json

def test_home(api):
    res = api.get('/')
    assert res.json == {'meassage': 'Hello!'}