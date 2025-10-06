import os
import pytest
import requests

class TestAuthenticationUserInfo:

    def test_get_current_user_info(self, base_url, auth_params):
        url = f"{base_url}/members/me"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get user info: {response.text}"

        user = response.json()
        assert "id" in user
        assert "username" in user
        assert "fullName" in user

        pytest.user_id = user["id"]
        print(f"User ID: {pytest.user_id}, Username: {user['username']}")

    def test_get_user_boards(self, base_url, auth_params):
        url = f"{base_url}/members/me/boards"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get boards: {response.text}"

        boards = response.json()
        assert isinstance(boards, list)
        print(f"User has {len(boards)} boards")

    def test_get_user_organizations(self, base_url, auth_params):
        url = f"{base_url}/members/me/organizations"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get organizations: {response.text}"

        orgs = response.json()
        assert isinstance(orgs, list)

        # Load expected workspace from .env
        expected_workspace = os.getenv("TRELLO_WORKSPACE_NAME")
        workspace = next((org for org in orgs if org.get("name") == expected_workspace), None)

        if not workspace:
            pytest.skip(f"{expected_workspace} not found in organizations")

        pytest.workspace_id = workspace["id"]
        print(f"Found workspace {workspace['name']} with ID: {workspace['id']}")
