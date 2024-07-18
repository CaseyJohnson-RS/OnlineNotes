import requests

from tests.config import HOST


def test_create_note():

    response = requests.post(HOST+"/create-note")
    assert response.json()["detail"] == "Not authenticated"


def test_update_note():

    response = requests.patch(HOST+"/update-note", data = {})
    assert response.json()["detail"] == "Not authenticated"


def test_delete_note():

    response = requests.delete(HOST+"/delete-note", data = {})
    assert response.json()["detail"] == "Not authenticated"


def test_restore_password():

    response = requests.post(HOST+"/restore-password", data = {"username":"not-in-db"})
    assert response.json() == False


def test_restore_password_confirm():

    response = requests.post(HOST+"/restore-password-confirm", data = {"username":"not-in-db", "confirm_seq":"000000"})
    assert response.json()["detail"] == "The user was not in the registration confirmation buffer"


def test_set_new_password():

    response = requests.post(HOST+"/set-new-password", data = {"username": "test", "password":"test"})
    assert response.json()["detail"] == "Username was'nt in the buffer of setting new password"
