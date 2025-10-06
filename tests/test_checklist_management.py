import pytest
import requests


@pytest.mark.checklist
class TestChecklistManagement:

    def test_create_checklist(self, base_url, auth_params, card_id):
        url = f"{base_url}/checklists"
        payload = {"name": "Test Checklist", "idCard": card_id}
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200, f"Checklist creation failed: {response.text}"
        checklist = response.json()
        self.checklist_id = checklist["id"]
        print(f"Created checklist ID: {self.checklist_id}")

    def test_get_checklist_details(self, base_url, auth_params, checklist_id):
        url = f"{base_url}/checklists/{checklist_id}"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get checklist: {response.text}"

    def test_add_check_item(self, base_url, auth_params, checklist_id):
        url = f"{base_url}/checklists/{checklist_id}/checkItems"
        response = requests.post(url, params=auth_params, json={"name": "My Check Item"})
        assert response.status_code == 200, f"Add check item failed: {response.text}"

        data = response.json()
        assert "id" in data
        assert "name" in data

        pytest.checkitem_id = data["id"]

    def test_update_check_item(self, base_url, auth_params, card_id):
        """Mark check item as complete"""
        url = f"{base_url}/cards/{card_id}/checkItem/{pytest.checkitem_id}"
        payload = {"state": "complete"}
        response = requests.put(url, params=auth_params, json=payload)
        assert response.status_code == 200, f"Failed to update check item: {response.text}"

        data = response.json()
        assert data.get("state") == "complete"

    def test_delete_checklist(self, base_url, auth_params, checklist_id):
        """Delete the checklist"""
        url = f"{base_url}/checklists/{checklist_id}"
        response = requests.delete(url, params=auth_params)
        assert response.status_code == 200, f"Failed: {response.text}"
