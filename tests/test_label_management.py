import pytest
import requests


@pytest.mark.label
class TestLabelManagement:

    def test_create_label(self, base_url, auth_params, board_id):
        url = f"{base_url}/labels"
        payload = {"name": "High Priority", "color": "red", "idBoard": board_id}
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200, f"Label creation failed: {response.text}"
        label = response.json()
        self.label_id = label["id"]
        print(f"Created label ID: {self.label_id}")

    def test_get_label_details(self, base_url, auth_params):
        """Get details of the created label"""
        url = f"{base_url}/labels/{pytest.label_id}"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get label details: {response.text}"

        data = response.json()
        assert "id" in data
        assert "name" in data

    def test_add_label_to_card(self, base_url, auth_params, card_id, label_id):
        url = f"{base_url}/cards/{card_id}/idLabels"
        payload = {"value": label_id}
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200, f"Failed: {response.text}"

        data = response.json()
        assert isinstance(data, list)

    def test_get_label_details(self, base_url, auth_params, label_id):
        url = f"{base_url}/labels/{label_id}"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed: {response.text}"

        data = response.json()
        assert "Test Label" in data["name"]  # matches creation

    def test_delete_label(self, base_url, auth_params, label_id):
        url = f"{base_url}/labels/{label_id}"
        response = requests.delete(url, params=auth_params)
        assert response.status_code == 200, f"Failed: {response.text}"

