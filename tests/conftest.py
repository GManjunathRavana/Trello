import requests
from dotenv import load_dotenv
import os
import pytest

# Load .env file
load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("TRELLO_BASE_URL", "https://api.trello.com/1")


@pytest.fixture(scope="session")
def auth_params():
    key = os.getenv("TRELLO_API_KEY")
    token = os.getenv("TRELLO_TOKEN")
    if not key or not token:
        pytest.exit("❌ Missing TRELLO_API_KEY or TRELLO_TOKEN in environment/.env")
    return {"key": key, "token": token}


# ------------------------
# Board Fixture
# ------------------------
@pytest.fixture(scope="session")
def board_id(base_url, auth_params):
    """Create a board for the test session, cleanup after"""
    url = f"{base_url}/boards/"
    payload = {"name": "PyTest Board"}
    response = requests.post(url, params=auth_params, json=payload)
    assert response.status_code == 200, f"Board creation failed: {response.text}"
    board = response.json()

    yield board["id"]

    # Cleanup
    requests.delete(f"{base_url}/boards/{board['id']}", params=auth_params)


# ------------------------
# List Fixture
# ------------------------
@pytest.fixture(scope="class")
def list_id(base_url, auth_params, board_id):
    """Create a list in the board"""
    url = f"{base_url}/lists"
    payload = {"name": "PyTest List", "idBoard": board_id}
    response = requests.post(url, params=auth_params, json=payload)
    assert response.status_code == 200, f"List creation failed: {response.text}"
    lid = response.json()["id"]

    yield lid

    # Cleanup → archive list
    requests.put(f"{base_url}/lists/{lid}", params=auth_params, json={"closed": True})


# ------------------------
# Card Fixture
# ------------------------
@pytest.fixture(scope="class")
def card_id(base_url, auth_params, list_id):
    """Create a card in the list"""
    url = f"{base_url}/cards"
    payload = {"name": "PyTest Card", "idList": list_id}
    response = requests.post(url, params=auth_params, json=payload)
    assert response.status_code == 200, f"Card creation failed: {response.text}"
    card = response.json()

    yield card["id"]

    # Cleanup
    requests.delete(f"{base_url}/cards/{card['id']}", params=auth_params)


# ------------------------
# Checklist Fixture
# ------------------------
@pytest.fixture(scope="class")
def checklist_id(base_url, auth_params, card_id):
    """Create a checklist on a card"""
    url = f"{base_url}/checklists"
    payload = {"name": "Test Checklist", "idCard": card_id}
    response = requests.post(url, params=auth_params, json=payload)
    assert response.status_code == 200, f"Checklist creation failed: {response.text}"
    checklist = response.json()

    yield checklist["id"]

    # Cleanup
    requests.delete(f"{base_url}/checklists/{checklist['id']}", params=auth_params)

@pytest.fixture(scope="session")
def workspace_id():
    wid = os.getenv("TRELLO_WORKSPACE_ID")
    if not wid:
        pytest.exit("Missing TRELLO_WORKSPACE_ID in .env")
    return wid

@pytest.fixture(scope="session")
def user_id():
    uid = os.getenv("TRELLO_USER_ID")
    if not uid:
        pytest.exit("Missing TRELLO_USER_ID in .env")
    return uid

@pytest.fixture(scope="class")
def label_id(base_url, auth_params, board_id):
    """Create and cleanup a label inside the board"""
    url = f"{base_url}/labels"
    payload = {"name": "Test Label", "color": "green", "idBoard": board_id}
    response = requests.post(url, params=auth_params, json=payload)
    assert response.status_code == 200, f"Label creation failed: {response.text}"
    label = response.json()
    yield label["id"]
    requests.delete(f"{base_url}/labels/{label['id']}", params=auth_params)

