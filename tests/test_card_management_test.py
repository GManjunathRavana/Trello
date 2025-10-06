import pytest
import requests
from datetime import datetime

@pytest.mark.card
class TestCardManagement:

    def test_create_card(self, base_url, auth_params, list_id):
        url = f"{base_url}/cards"
        payload = {"name": "Card from test", "idList": list_id}
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200, f"Card creation failed: {response.text}"
        card = response.json()
        assert "id" in card
        self.card_id = card["id"]   # store in self, not pytest
        print(f"Created card ID: {self.card_id}")

    def test_get_card_details(self, base_url, auth_params, card_id):
        url = f"{base_url}/cards/{card_id}"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get card details: {response.text}"
        card = response.json()
        assert card["id"] == card_id

    def test_update_card(self, base_url, auth_params, card_id):
        url = f"{base_url}/cards/{card_id}"
        response = requests.put(url, params=auth_params, json={"name": "Updated Card"})
        assert response.status_code == 200, f"Failed: {response.text}"

        data = response.json()
        assert "Updated" in data["name"]
        assert "due" in data

    def test_move_card_to_another_list(self, base_url, auth_params, board_id, card_id):
        # Create another list in same board
        list_url = f"{base_url}/lists"
        list_payload = {"name": "PyTest Doing List", "idBoard": board_id}
        list_response = requests.post(list_url, params=auth_params, json=list_payload)
        assert list_response.status_code == 200
        doing_list_id = list_response.json()["id"]

        # Move card to new list
        url = f"{base_url}/cards/{card_id}"
        response = requests.put(url, params=auth_params, json={"idList": doing_list_id})
        assert response.status_code == 200, f"Failed: {response.text}"

    def test_add_comment_to_card(self, base_url, auth_params, card_id):
        url = f"{base_url}/cards/{card_id}/actions/comments"
        payload = {"text": "This is a test comment"}
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200, f"Failed: {response.text}"

        data = response.json()
        assert data["type"] == "commentCard"
        pytest.test_comment_id = data["id"]

    # def test_archive_card(self, base_url, auth_params):
    #     url = f"{base_url}/cards/{pytest.test_card_id}"
    #     payload = {"closed": True}
    #     response = requests.put(url, params=auth_params, json=payload)
    #     assert response.status_code == 200
    #     assert response.json()["closed"] is True
    #
    # def test_delete_card(self, base_url, auth_params):
    #     url = f"{base_url}/cards/{pytest.test_card_id}"
    #     response = requests.delete(url, params=auth_params)
    #     assert response.status_code == 200
