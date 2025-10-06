import pytest
import requests


@pytest.mark.search
class TestSearchOperations:

    def test_search_all_content(self, base_url, auth_params, board_id):
        """Search across all content types in a board"""
        url = f"{base_url}/search"
        params = {
            "query": "test",
            "idBoards": board_id,
            "modelTypes": "all",
            **auth_params
        }
        response = requests.get(url, params=params)
        assert response.status_code == 200, f"Search all failed: {response.text}"

        data = response.json()
        assert "cards" in data
        assert "boards" in data
        assert "members" in data

        print(f"Search found: {len(data['cards'])} cards, {len(data['boards'])} boards, {len(data['members'])} members")

    def test_search_cards_only(self, base_url, auth_params):
        """Search only for cards"""
        url = f"{base_url}/search"
        params = {
            "query": "card",
            "modelTypes": "cards",
            "cards_limit": 20,
            **auth_params
        }
        response = requests.get(url, params=params)
        assert response.status_code == 200, f"Search cards failed: {response.text}"

        data = response.json()
        assert "cards" in data
        assert isinstance(data["cards"], list)

        print(f"Found {len(data['cards'])} cards matching search")
