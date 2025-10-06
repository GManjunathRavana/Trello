import requests

class TestOrganizationManagement:

    def test_get_organization_details(self, base_url, auth_params, workspace_id):
        """Get details of an organization (workspace)"""
        url = f"{base_url}/organizations/{workspace_id}"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get workspace details: {response.text}"
        data = response.json()
        assert "id" in data
        assert data["id"] == workspace_id

    def test_get_organization_boards(self, base_url, auth_params, workspace_id):
        """Get all boards in an organization"""
        url = f"{base_url}/organizations/{workspace_id}/boards"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get boards: {response.text}"
        boards = response.json()
        assert isinstance(boards, list)

    def test_get_organization_members(self, base_url, auth_params, workspace_id):
        """Get all members in an organization"""
        url = f"{base_url}/organizations/{workspace_id}/members"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get members: {response.text}"
        members = response.json()
        assert isinstance(members, list)
        if members:
            assert "id" in members[0]
