import pytest
import requests

@pytest.mark.list
class TestListManagement:

    def test_create_list(self, list_id):
        assert list_id is not None

    def test_get_list_details(self, base_url, auth_params, list_id):
        url = f"{base_url}/lists/{list_id}"
        params = {**auth_params, "fields": "all", "cards": "open"}
        response = requests.get(url, params=params)
        assert response.status_code == 200
        assert response.json()["id"] == list_id

    def test_update_list(self, base_url, auth_params, list_id):
        url = f"{base_url}/lists/{list_id}"
        payload = {"name": "PyTest List Updated"}
        response = requests.put(url, params=auth_params, json=payload)
        assert response.status_code == 200
        assert "Updated" in response.json()["name"]

    def test_archive_list(self, base_url, auth_params, list_id):
        url = f"{base_url}/lists/{list_id}"
        payload = {"closed": True}
        response = requests.put(url, params=auth_params, json=payload)
        assert response.status_code == 200
        assert response.json()["closed"] is True
