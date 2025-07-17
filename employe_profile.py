from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api/employee-profile"
user_sessions = {}

# ✅ Only allow users to update these fields
ALLOWED_UPDATE_FIELDS = {
    "phone_number",
    "address",
    "emergency_contact",
    "blood_group",
    "gender",
    "marital_status",
    "languages_known"
}


@app.route('/chat/profile', methods=['POST'])
def employee_profile():
    user_id = request.json.get("user_id")
    selected_option = request.json.get("selected_option").lower()

    # === MAIN MENU ===
    if selected_option == "employee_profile":
        return jsonify({"next": "profile_menu"})  # Show: View Mine, View Other, Update

    # === VIEW MY PROFILE ===
    elif selected_option == "view_my_profile":
        requests.get(f"{BASE_URL}/me", headers=_headers())
        return jsonify({"next": "show_my_profile"})

    # === VIEW OTHER PROFILE ===
    elif selected_option == "view_other_profile":
        user_sessions[user_id] = {"intent": "view_other", "state": "ask_employee_id"}
        return jsonify({"next": "select_employee_id"})

    elif user_id in user_sessions and user_sessions[user_id]["intent"] == "view_other":
        emp_id = selected_option
        requests.get(f"{BASE_URL}/{emp_id}", headers=_headers())
        user_sessions.pop(user_id, None)
        return jsonify({"next": "show_other_profile"})

    # === UPDATE PROFILE ===
    elif selected_option == "update_profile":
        user_sessions[user_id] = {"intent": "update_field", "state": "ask_field", "data": {}}
        return jsonify({"next": "select_field_to_update"})

    elif user_id in user_sessions and user_sessions[user_id]["intent"] == "update_field":
        session = user_sessions[user_id]
        state = session["state"]
        data = session["data"]

        if state == "ask_field":
            if selected_option not in ALLOWED_UPDATE_FIELDS:
                user_sessions.pop(user_id, None)
                return jsonify({"next": "field_not_allowed"})

            data["field"] = selected_option
            session["state"] = "ask_new_value"
            return jsonify({"next": "select_new_value"})

        elif state == "ask_new_value":
            data["value"] = selected_option
            patch_payload = {data["field"]: data["value"]}
            requests.patch(f"{BASE_URL}/me", json=patch_payload, headers=_headers())
            user_sessions.pop(user_id, None)
            return jsonify({"next": "profile_updated"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }


if __name__ == '__main__':
    app.run(debug=True)
