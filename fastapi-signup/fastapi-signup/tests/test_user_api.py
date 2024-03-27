import pytest
from fastapi.testclient import TestClient

from fastapi_signup.main import app

client = TestClient(app)


@pytest.fixture
def authorization_headers():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiVGVzdCBDaGl6aSIsInVzZXJfZW1haWwiOiJjaGl6aUBnbWFpbC5jb20iLCJyb2xlIjoiYWRtaW4iLCJleHBpcmVzIjoxNjg3MzkzODA4LjkyMjcwM30.86de3iJiSQ51KbMkGKOEzypoWxeAjHpVP_GLxG0ols8"
    }


@pytest.fixture
def sign_up_info():
    return {
        "fullname": "Test Chizi",
        "email": "tetchizik@gmail.com",
        "password": "ChiziKarogwaTena",
        "role": "admin",
    }


@pytest.fixture
def sample_update_payload():
    return {
        "fullname": "Pro Admin",
        "email": "admin50@gmail.com",
        "password": "this is an updated field",
        "role": "admin",
    }


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok 👍 "}


# 동일한 이메일을 가진 사용자가 이미 등록되어 있는 경우 실패합니다.
def test_user_creation(sign_up_info):
    response = client.post("/signup/", json=sign_up_info)
    assert response.status_code == 201


def test_user_login():
    response = client.post(
        "/login/", json={"email": "chizi@gmail.com", "password": "ChiziKarogwaTena"}
    )
    assert response.status_code == 200
    assert response is not None
    assert "access_token" in response.json()
    assert response.json()["access_token"] != ""


def test_get_users(authorization_headers):
    response = client.get("/users/", headers=authorization_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    for element in response.json():
        assert isinstance(element, dict)
        assert all(
            key in element
            for key in ["id", "fullname", "email", "role", "date", "time"]
        )


# 데이터베이스에서 해당 ID를 가진 사용자를 찾을 수 없는 경우 실패합니다.
def test_update_users(authorization_headers, sample_update_payload):
    user_id = 1  # this could be any user id existing in the database
    response = client.put(
        f"/users/{user_id}", headers=authorization_headers, json=sample_update_payload
    )
    assert response.status_code == 200

    expected_elements = {"id": user_id, **sample_update_payload}

    response_json = response.json()
    assert all(key in response_json for key in expected_elements)

    for key, value in expected_elements.items():
        assert response_json[key] == value


# this test will fail is the user with the user_id is not found in the database
def test_delete_user(authorization_headers):
    user_id = 1  # this could be any user id existing in the database
    response = client.delete(f"/users/{user_id}", headers=authorization_headers)
    assert response.status_code == 200
    assert response.json() == {
        "status": "Success",
        "message": "User deleted successfully.",
    }
