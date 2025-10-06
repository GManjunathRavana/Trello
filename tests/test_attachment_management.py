import pytest
import requests


@pytest.mark.attachment
class TestAttachmentManagement:

    def test_add_url_attachment(self, base_url, auth_params, card_id):
        """Add a URL attachment to a card"""
        url = f"{base_url}/cards/{card_id}/attachments"
        payload = {
            "name": "Test Document",
            "url": "https://www.example.com/document.pdf"
        }
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200, f"Failed to add attachment: {response.text}"

        data = response.json()
        assert "id" in data
        assert "name" in data
        assert "url" in data

        pytest.attachment_id = data["id"]

    def test_get_card_attachments(self, base_url, auth_params, card_id):
        """Retrieve all attachments from a card"""
        url = f"{base_url}/cards/{card_id}/attachments"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get attachments: {response.text}"

        attachments = response.json()
        assert isinstance(attachments, list)
        assert any(att["id"] == pytest.attachment_id for att in attachments)

    def test_get_attachment_details(self, base_url, auth_params, card_id):
        """Get details of a specific attachment"""
        url = f"{base_url}/cards/{card_id}/attachments/{pytest.attachment_id}"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get attachment details: {response.text}"

        data = response.json()
        assert data["id"] == pytest.attachment_id
        assert "name" in data

    def test_delete_attachment(self, base_url, auth_params, card_id):
        """Delete the attachment from the card"""
        url = f"{base_url}/cards/{card_id}/attachments/{pytest.attachment_id}"
        response = requests.delete(url, params=auth_params)
        assert response.status_code == 200, f"Failed to delete attachment: {response.text}"
