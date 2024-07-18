import requests

from tests.config import HOST

def test_unexists_user():
    response = requests.post(HOST+"/username-exist?username=unexistuser%40gmail.com")
    assert response.json() == False

def test_exists_user():
    response = requests.post(HOST+"/username-exist?username=admin%40admin.admin")
    assert response.json() == True

