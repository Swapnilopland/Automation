from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api/employee-profile"
user_sessions = {}

@app.route('/chat/employee', methods=['POST'])
def employee_module():
    user_id = request.json.get("user_id")
    selected_option = request.json.get("selected_option").lower()

    # === MAIN MENU ===
    if selected_option == "employee":
        return jsonify({"next": "employee_menu"})  # View All, View By ID, Filter

    # === VIEW ALL EMPLOYEES ===
    elif selected_option == "view_all":
        requests.get(BASE_URL, headers=_headers())
        return jsonify({"next": "show_all_employees"})

    # === VIEW EMPLOYEE BY ID ===
    elif selected_option == "view_by_id":
        user_sessions[user_id] = {"intent": "view_by_id"}
        return jsonify({"next": "ask_employee_id"})

    elif user_id in user_sessions and user_sessions[user_id]["intent"] == "view_by_id":
        emp_id = selected_option
        requests.get(f"{BASE_URL}/{emp_id}", headers=_headers())
        user_sessions.pop(user_id, None)
        return jsonify({"next": "show_employee_profile"})

    # === FILTER EMPLOYEES ===
    elif selected_option == "filter":
        user_sessions[user_id] = {"intent": "filter", "state": "ask_filter_type"}
        return jsonify({"next": "select_filter_type"})  # Options: department, designation, location

    elif user_id in user_sessions and user_sessions[user_id]["intent"] == "filter":
        session = user_sessions[user_id]
        state = session["state"]

        if state == "ask_filter_type":
            filter_type = selected_option
            if filter_type not in ["department", "designation", "location"]:
                user_sessions.pop(user_id, None)
                return jsonify({"next": "invalid_filter"})
            session["filter_type"] = filter_type
            session["state"] = "ask_filter_value"
            return jsonify({"next": f"select_{filter_type}"})  # e.g., select_department

        elif state == "ask_filter_value":
            filter_type = session["filter_type"]
            filter_value = selected_option
            url = f"{BASE_URL}?{filter_type}={filter_value}"
            requests.get(url, headers=_headers())
            user_sessions.pop(user_id, None)
            return jsonify({"next": "show_filtered_employees"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    app.run(debug=True)
