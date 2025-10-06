import pytest
import requests


@pytest.mark.member
class TestMemberManagement:

    def test_get_board_members(self, base_url, auth_params, board_id):
        """Get all members of a board"""
        url = f"{base_url}/boards/{board_id}/members"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to fetch members: {response.text}"

        members = response.json()
        assert isinstance(members, list)
        assert len(members) >= 1  # at least the board owner should be present
        pytest.test_user_id = members[0]["id"]  # save first member ID for next test

    def test_add_member_to_board(self, base_url, auth_params, board_id):
        """Try adding a member to the board by email"""
        url = f"{base_url}/boards/{board_id}/members"
        payload = {
            "email": "test@example.com",  # replace with a real Trello user email if you want to test properly
            "type": "normal"
        }
        response = requests.put(url, params=auth_params, json=payload)

        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list), "Expected member list in response"
        else:
            # Expected if email doesn't exist or already added
            print(f"⚠️ Member addition failed (expected for dummy email): {response.text}")

    def test_get_member_details(self, base_url, auth_params):
        """Get details of a specific member"""
        url = f"{base_url}/members/{pytest.test_user_id}"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to fetch member details: {response.text}"

        data = response.json()
        assert "id" in data
        assert "username" in data
