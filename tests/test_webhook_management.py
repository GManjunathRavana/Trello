import pytest
import requests
import os


@pytest.mark.webhook
class TestWebhookManagement:

    def test_create_webhook(self, base_url, auth_params, board_id):
        """Create a webhook to monitor board changes"""
        callback_url = os.getenv("WEBHOOK_CALLBACK_URL", "https://webhook.site/test")
        url = f"{base_url}/webhooks"
        payload = {
            "callbackURL": callback_url,
            "idModel": board_id,
            "description": "Test webhook for board changes"
        }
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200, f"Webhook creation failed: {response.text}"

        data = response.json()
        assert "id" in data
        assert "callbackURL" in data

        pytest.webhook_id = data["id"]

    def test_get_webhook_details(self, base_url, auth_params):
        """Retrieve details of the created webhook"""
        url = f"{base_url}/webhooks/{pytest.webhook_id}"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to get webhook: {response.text}"

        data = response.json()
        assert "id" in data
        assert "active" in data

    def test_list_all_webhooks(self, base_url, auth_params):
        """List all webhooks associated with the current token"""
        token = auth_params["token"]
        url = f"{base_url}/tokens/{token}/webhooks"
        response = requests.get(url, params=auth_params)
        assert response.status_code == 200, f"Failed to list webhooks: {response.text}"

        webhooks = response.json()
        assert isinstance(webhooks, list)
        assert any(wh["id"] == pytest.webhook_id for wh in webhooks)

    def test_update_webhook(self, base_url, auth_params):
        """Update webhook description"""
        url = f"{base_url}/webhooks/{pytest.webhook_id}"
        payload = {"description": "Updated webhook description - Pytest"}
        response = requests.put(url, params=auth_params, json=payload)
        assert response.status_code == 200, f"Failed to update webhook: {response.text}"

        data = response.json()
        assert "Updated" in data["description"]

    def test_delete_webhook(self, base_url, auth_params):
        """Delete the webhook"""
        url = f"{base_url}/webhooks/{pytest.webhook_id}"
        response = requests.delete(url, params=auth_params)
        assert response.status_code == 200, f"Failed to delete webhook: {response.text}"
