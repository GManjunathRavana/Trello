import pytest
import requests

@pytest.mark.board
class TestBoardManagement:

    def test_create_board(self, board_id):
        assert board_id is not None

    def test_get_board_details(self, base_url, auth_params, board_id):
        url = f"{base_url}/boards/{board_id}"
        params = {**auth_params, "fields": "all", "lists": "open", "cards": "open"}
        response = requests.get(url, params=params)
        assert response.status_code == 200
        assert response.json()["id"] == board_id

    def test_update_board(self, base_url, auth_params, board_id):
        url = f"{base_url}/boards/{board_id}"
        payload = {"name": "PyTest Board Updated"}
        response = requests.put(url, params=auth_params, json=payload)
        assert response.status_code == 200
        assert "Updated" in response.json()["name"]

    # def test_archive_board(self, base_url, auth_params, board_id):
    #     url = f"{base_url}/boards/{board_id}"
    #     payload = {"closed": True}
    #     response = requests.put(url, params=auth_params, json=payload)
    #     assert response.status_code == 200
    #     assert response.json()["closed"] is True
    #
    # def test_delete_board(self, base_url, auth_params, board_id):
    #     url = f"{base_url}/boards/{board_id}"
    #     response = requests.delete(url, params=auth_params)
    #     assert response.status_code == 200
