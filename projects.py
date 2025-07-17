from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api"

@app.route('/chat/projects', methods=['POST'])
def projects_module():
    selected_option = request.json.get("selected_option").lower()
    project_id = request.json.get("project_id")  # Optional, for detailed view

    # === PROJECTS MAIN MENU ===
    if selected_option == "projects":
        return jsonify({"next": "projects_menu"})

    # === 1. View All Projects ===
    elif selected_option == "view_all_projects":
        requests.get(f"{BASE_URL}/projects/all", headers=_headers())
        return jsonify({"next": "show_all_projects"})

    # === 2. Filter by Status ===
    elif selected_option == "view_active_projects":
        requests.get(f"{BASE_URL}/projects?status=active", headers=_headers())
        return jsonify({"next": "show_active_projects"})

    elif selected_option == "view_completed_projects":
        requests.get(f"{BASE_URL}/projects?status=completed", headers=_headers())
        return jsonify({"next": "show_completed_projects"})

    elif selected_option == "view_on_hold_projects":
        requests.get(f"{BASE_URL}/projects?status=on_hold", headers=_headers())
        return jsonify({"next": "show_on_hold_projects"})

    # === 3. Project Details ===
    elif selected_option == "view_project_details" and project_id:
        requests.get(f"{BASE_URL}/projects/{project_id}/details", headers=_headers())
        return jsonify({"next": "show_project_details"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    app.run(debug=True)
