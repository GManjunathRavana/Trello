import pytest
import requests


@pytest.mark.workflow
class TestTodoDoingDoneWorkflow:

    def test_1_create_todo_board(self, base_url, auth_params):
        url = f"{base_url}/boards"
        payload = {
            "name": "Todo Workflow Board - Pytest",
            "desc": "Complete Todo/Doing/Done workflow demonstration",
            "prefs_permissionLevel": "private"
        }
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200, f"Board creation failed: {response.text}"

        data = response.json()
        pytest.workflow_board_id = data["id"]
        print(f"✅ Todo Board created: {pytest.workflow_board_id}")

    def test_2_create_todo_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "📝 Todo", "idBoard": pytest.workflow_board_id, "pos": "top"}
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200

        pytest.todo_list_id = response.json()["id"]
        print(f"📝 Todo List ID: {pytest.todo_list_id}")

    def test_3_create_doing_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "⚡ Doing", "idBoard": pytest.workflow_board_id, "pos": "bottom"}
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200

        pytest.doing_list_id = response.json()["id"]
        print(f"⚡ Doing List ID: {pytest.doing_list_id}")

    def test_4_create_done_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "✅ Done", "idBoard": pytest.workflow_board_id, "pos": "bottom"}
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200

        pytest.done_list_id = response.json()["id"]
        print(f"✅ Done List ID: {pytest.done_list_id}")

    def test_5_create_sample_todo_card(self, base_url, auth_params):
        url = f"{base_url}/cards"
        payload = {
            "name": "Complete API documentation",
            "desc": "Write comprehensive API documentation with examples",
            "idList": pytest.todo_list_id,
            "due": "2025-12-31T17:00:00.000Z"
        }
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200

        pytest.test_card_id = response.json()["id"]
        print(f"📝 First Todo Card ID: {pytest.test_card_id}")

    def test_6_create_more_todo_card(self, base_url, auth_params):
        url = f"{base_url}/cards"
        payload = {
            "name": "Set up CI/CD pipeline",
            "desc": "Configure automated testing and deployment",
            "idList": pytest.todo_list_id
        }
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200

        print(f"📝 Second Todo Card ID: {response.json()['id']}")

    def test_7_move_card_to_doing(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.test_card_id}"
        payload = {"idList": pytest.doing_list_id}
        response = requests.put(url, params=auth_params, json=payload)
        assert response.status_code == 200
        assert response.json()["idList"] == pytest.doing_list_id

        print("➡️ Card moved to Doing list")

    def test_8_add_progress_comment(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.test_card_id}/actions/comments"
        payload = {
            "text": "Started working on this task. Research phase completed, now moving to implementation."
        }
        response = requests.post(url, params=auth_params, json=payload)
        assert response.status_code == 200
        assert response.json()["type"] == "commentCard"

        print("💬 Progress comment added to card")

    def test_9_move_card_to_done(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.test_card_id}"
        payload = {"idList": pytest.done_list_id}
        response = requests.put(url, params=auth_params, json=payload)
        assert response.status_code == 200
        assert response.json()["idList"] == pytest.done_list_id

        print("✅ Card moved to Done list")

    def test_10_archive_board(self, base_url, auth_params):
        url = f"{base_url}/boards/{pytest.workflow_board_id}"
        payload = {"closed": True}
        response = requests.put(url, params=auth_params, json=payload)
        assert response.status_code == 200
        assert response.json()["closed"] is True

        print("📦 Workflow board archived")
