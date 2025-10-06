import pytest
import requests


@pytest.mark.workflow
class TestScrumWorkflow:

    def test_1_create_scrum_board(self, base_url, auth_params):
        url = f"{base_url}/boards"
        payload = {
            "name": "Scrum Board Sprint 1 - Pytest",
            "desc": "Agile Scrum board with sprint management workflow",
            "prefs_permissionLevel": "private"
        }
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200, f"Failed to create Scrum board: {resp.text}"
        pytest.board_id = resp.json()["id"]
        print(f"📋 Scrum Board ID: {pytest.board_id}")

    def test_2_create_product_backlog(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "📋 Product Backlog", "idBoard": pytest.board_id, "pos": "top"}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.backlog_list_id = resp.json()["id"]

    def test_3_create_sprint_planning_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "🎯 Sprint Planning", "idBoard": pytest.board_id, "pos": "bottom"}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.planning_list_id = resp.json()["id"]

    def test_4_create_active_sprint_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "🏃 Active Sprint", "idBoard": pytest.board_id, "pos": "bottom"}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.active_list_id = resp.json()["id"]

    def test_5_create_sprint_review_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "📊 Sprint Review", "idBoard": pytest.board_id, "pos": "bottom"}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.review_list_id = resp.json()["id"]

    def test_6_create_sprint_done_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "✅ Sprint Done", "idBoard": pytest.board_id, "pos": "bottom"}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.done_list_id = resp.json()["id"]

    def test_7_create_story_point_label(self, base_url, auth_params):
        url = f"{base_url}/labels"
        payload = {"name": "5 Story Points", "color": "orange", "idBoard": pytest.board_id}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.label_id = resp.json()["id"]

    def test_8_create_user_story(self, base_url, auth_params):
        url = f"{base_url}/cards"
        payload = {
            "name": "As a user, I want to see my purchase history",
            "desc": "User story with acceptance criteria and DoD",
            "idList": pytest.backlog_list_id,
            "due": "2025-10-30T17:00:00.000Z"
        }
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.card_id = resp.json()["id"]
        print(f"📝 User Story Card ID: {pytest.card_id}")

    def test_9_add_story_points(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}/idLabels"
        payload = {"value": pytest.label_id}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200

    def test_10_move_story_to_planning(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}"
        payload = {"idList": pytest.planning_list_id}
        resp = requests.put(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        assert resp.json()["idList"] == pytest.planning_list_id

    def test_11_create_task_checklist(self, base_url, auth_params):
        url = f"{base_url}/checklists"
        payload = {"name": "Sprint Tasks", "idCard": pytest.card_id}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.checklist_id = resp.json()["id"]

    def test_12_add_sprint_task(self, base_url, auth_params):
        url = f"{base_url}/checklists/{pytest.checklist_id}/checkItems"
        payload = {"name": "Design database schema", "checked": False}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.checkitem_id = resp.json()["id"]

    def test_13_start_sprint_move_to_active(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}"
        payload = {"idList": pytest.active_list_id}
        resp = requests.put(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        assert resp.json()["idList"] == pytest.active_list_id

    def test_14_complete_sprint_task(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}/checkItem/{pytest.checkitem_id}"
        payload = {"state": "complete"}
        resp = requests.put(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        assert resp.json()["state"] == "complete"

    def test_15_add_daily_standup(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}/actions/comments"
        payload = {"text": "Daily Standup: Yesterday did X, Today doing Y, No blockers."}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200

    def test_16_move_to_review(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}"
        payload = {"idList": pytest.review_list_id}
        resp = requests.put(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        assert resp.json()["idList"] == pytest.review_list_id

    def test_17_add_sprint_review_notes(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}/actions/comments"
        payload = {"text": "Sprint Review: ✅ All features delivered, feedback noted."}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200

    def test_18_move_to_done(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}"
        payload = {"idList": pytest.done_list_id}
        resp = requests.put(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        assert resp.json()["idList"] == pytest.done_list_id

    def test_19_add_retrospective(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}/actions/comments"
        payload = {"text": "Retrospective: Went well: X, Improve: Y, Action Items: Z"}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200

    def test_20_archive_scrum_board(self, base_url, auth_params):
        url = f"{base_url}/boards/{pytest.board_id}"
        payload = {"closed": True}
        resp = requests.put(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        assert resp.json()["closed"] is True
        print("✅ Scrum Board archived after sprint completion")
