from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api/org"

user_sessions = {}

@app.route('/chat/org', methods=['POST'])
def organisation_structure():
    user_id = request.json.get("user_id")
    selected_option = request.json.get("selected_option")

    # Step 1 - Entry point
    if selected_option == "org_structure":
        return jsonify({"next": "org_menu"})

    # Step 2 View Departments (no filters)
    elif selected_option == "view_departments":
        requests.get(f"{BASE_URL}/departments", headers=_headers())
        return jsonify({"next": "show_departments"})

    # Step 3 View All Teams (no filter)
    elif selected_option == "view_teams":
        requests.get(f"{BASE_URL}/teams", headers=_headers())
        return jsonify({"next": "show_teams"})

    # Step 4 Start filtered teams flow
    elif selected_option == "view_teams_by_department":
        user_sessions[user_id] = {"intent": "teams_by_dept", "state": "ask_department"}
        return jsonify({"next": "select_department"})

    # Step 5 Start filtered hierarchy flow
    elif selected_option == "view_hierarchy_by_manager":
        user_sessions[user_id] = {"intent": "hierarchy_by_manager", "state": "ask_manager"}
        return jsonify({"next": "select_manager"})

    # Step 6 Department selected
    elif user_id in user_sessions and user_sessions[user_id]["intent"] == "teams_by_dept":
        department = selected_option
        requests.get(f"{BASE_URL}/teams?department={department}", headers=_headers())
        user_sessions.pop(user_id, None)
        return jsonify({"next": "show_filtered_teams"})

    # Step 7 Manager selected
    elif user_id in user_sessions and user_sessions[user_id]["intent"] == "hierarchy_by_manager":
        manager = selected_option
        requests.get(f"{BASE_URL}/hierarchy?manager={manager}", headers=_headers())
        user_sessions.pop(user_id, None)
        return jsonify({"next": "show_filtered_hierarchy"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    app.run(debug=True)
