from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api/timesheets"
user_sessions = {}

@app.route('/chat/timesheet', methods=['POST'])
def timesheet_module():
    user_id = request.json.get("user_id")
    selected_option = request.json.get("selected_option").lower()

    # ==== MAIN MENU ====
    if selected_option == "timesheet":
        return jsonify({"next": "timesheet_menu"})

    # ==== VIEW TIMESHEETS ====
    elif selected_option == "view_all":
        requests.get(BASE_URL, headers=_headers())
        return jsonify({"next": "show_all_timesheets"})

    elif selected_option == "view_approved":
        requests.get(BASE_URL + "?status=approved", headers=_headers())
        return jsonify({"next": "show_approved_timesheets"})

    elif selected_option == "view_rejected":
        requests.get(BASE_URL + "?status=rejected", headers=_headers())
        return jsonify({"next": "show_rejected_timesheets"})

    elif selected_option == "view_by_date":
        user_sessions[user_id] = {"intent": "date_range"}
        return jsonify({"next": "ask_start_date"})

    elif user_id in user_sessions and user_sessions[user_id].get("intent") == "date_range":
        session = user_sessions[user_id]
        if "start_date" not in session:
            session["start_date"] = selected_option
            return jsonify({"next": "ask_end_date"})
        else:
            end_date = selected_option
            start_date = session["start_date"]
            requests.get(f"{BASE_URL}?start_date={start_date}&end_date={end_date}", headers=_headers())
            user_sessions.pop(user_id, None)
            return jsonify({"next": "show_timesheets_by_date"})

    # ==== SUBMIT NEW TIMESHEET ====
    elif selected_option == "submit":
        user_sessions[user_id] = {"intent": "submit", "state": "ask_date"}
        return jsonify({"next": "ask_timesheet_date"})

    elif user_id in user_sessions and user_sessions[user_id]["intent"] == "submit":
        session = user_sessions[user_id]
        state = session["state"]

        if state == "ask_date":
            session["date"] = selected_option
            session["state"] = "ask_project"
            return jsonify({"next": "ask_project"})

        elif state == "ask_project":
            session["project"] = selected_option
            session["state"] = "ask_hours"
            return jsonify({"next": "ask_hours"})

        elif state == "ask_hours":
            session["hours"] = selected_option
            session["state"] = "ask_description"
            return jsonify({"next": "ask_description"})

        elif state == "ask_description":
            session["description"] = selected_option
            payload = {
                "date": session["date"],
                "project": session["project"],
                "hours": session["hours"],
                "description": session["description"],
                "status": "submitted"
            }
            requests.post(BASE_URL, json=payload, headers=_headers())
            user_sessions.pop(user_id, None)
            return jsonify({"next": "timesheet_submitted"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    app.run(debug=True)
