import requests
import pytest
from utils import config

@pytest.fixture
def auth_params():
    return {"key": config.API_KEY, "token": config.TOKEN}

def test_get_current_user(auth_params):
    url = f"{config.BASE_URL}/members/me"
    response = requests.get(url, params=auth_params)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["username"] == "manjunathsparta"
