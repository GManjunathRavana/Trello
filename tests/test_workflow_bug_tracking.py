import pytest
import requests


@pytest.mark.workflow
class TestBugTrackingWorkflow:

    def test_1_create_bug_tracking_board(self, base_url, auth_params):
        url = f"{base_url}/boards"
        payload = {
            "name": "Bug Tracking Board - Pytest",
            "desc": "Complete bug tracking workflow with lifecycle management",
            "prefs_permissionLevel": "private"
        }
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200, f"Board creation failed: {resp.text}"
        pytest.board_id = resp.json()["id"]
        print(f"🐛 Bug Tracking Board ID: {pytest.board_id}")

    def test_2_create_bug_backlog_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "🐛 Bug Backlog", "idBoard": pytest.board_id, "pos": "top"}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.backlog_list_id = resp.json()["id"]

    def test_3_create_in_progress_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "🔧 In Progress", "idBoard": pytest.board_id, "pos": "bottom"}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.in_progress_list_id = resp.json()["id"]

    def test_4_create_testing_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "🧪 Testing", "idBoard": pytest.board_id, "pos": "bottom"}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.testing_list_id = resp.json()["id"]

    def test_5_create_closed_list(self, base_url, auth_params):
        url = f"{base_url}/lists"
        payload = {"name": "✅ Closed", "idBoard": pytest.board_id, "pos": "bottom"}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.closed_list_id = resp.json()["id"]

    def test_6_create_priority_label(self, base_url, auth_params):
        url = f"{base_url}/labels"
        payload = {"name": "Critical Bug", "color": "red", "idBoard": pytest.board_id}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.label_id = resp.json()["id"]

    def test_7_report_new_bug(self, base_url, auth_params):
        url = f"{base_url}/cards"
        payload = {
            "name": "Login button not working on mobile",
            "desc": "Bug: Login button does not respond on mobile devices",
            "idList": pytest.backlog_list_id,
            "due": "2025-10-15T17:00:00.000Z"
        }
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        pytest.card_id = resp.json()["id"]
        print(f"📝 Bug Card ID: {pytest.card_id}")

    def test_8_add_label_to_bug(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}/idLabels"
        payload = {"value": pytest.label_id}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200

    def test_9_assign_bug_to_developer(self, base_url, auth_params, user_id):
        url = f"{base_url}/cards/{pytest.card_id}/idMembers"
        payload = {"value": user_id}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200

    def test_10_move_bug_to_in_progress(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}"
        payload = {"idList": pytest.in_progress_list_id}
        resp = requests.put(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        assert resp.json()["idList"] == pytest.in_progress_list_id

    def test_11_add_investigation_comment(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}/actions/comments"
        payload = {"text": "Investigation: Root cause found. Working on fix."}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200

    def test_12_move_bug_to_testing(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}"
        payload = {"idList": pytest.testing_list_id}
        resp = requests.put(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        assert resp.json()["idList"] == pytest.testing_list_id

    def test_13_add_testing_results(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}/actions/comments"
        payload = {"text": "✅ Tests passed on iOS and Android. Ready for release."}
        resp = requests.post(url, params=auth_params, json=payload)
        assert resp.status_code == 200

    def test_14_close_bug(self, base_url, auth_params):
        url = f"{base_url}/cards/{pytest.card_id}"
        payload = {"idList": pytest.closed_list_id}
        resp = requests.put(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        assert resp.json()["idList"] == pytest.closed_list_id

    def test_15_archive_board(self, base_url, auth_params):
        url = f"{base_url}/boards/{pytest.board_id}"
        payload = {"closed": True}
        resp = requests.put(url, params=auth_params, json=payload)
        assert resp.status_code == 200
        assert resp.json()["closed"] is True
        print("📦 Bug Tracking Board archived")
