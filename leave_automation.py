from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api/leaves"

# Session store to track user flow
user_sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    user_id = request.json.get("user_id")
    selected_option = request.json.get("selected_option").lower()

    # Initial menu selection
    if selected_option == "apply_leave":
        user_sessions[user_id] = {"intent": "apply_leave", "state": "ask_leave_type", "data": {}}
        return jsonify({"next": "ask_leave_type"})

    elif selected_option == "leave_balance":
        requests.get(f"{BASE_URL}/balance", headers=_headers())
        return jsonify({"next": "show_leave_balance"})

    elif selected_option == "leave_status":
        requests.get(f"{BASE_URL}/status", headers=_headers())
        return jsonify({"next": "show_leave_status"})

    elif selected_option == "cancel_leave":
        user_sessions[user_id] = {"intent": "cancel_leave", "state": "ask_leave_id", "data": {}}
        return jsonify({"next": "ask_leave_id"})

    # Continue Apply Leave flow
    if user_id in user_sessions:
        session = user_sessions[user_id]
        intent = session["intent"]
        state = session["state"]
        data = session["data"]

        if intent == "apply_leave":
            if state == "ask_leave_type":
                data["leave_type"] = selected_option
                session["state"] = "ask_start_date"
                return jsonify({"next": "ask_start_date"})

            elif state == "ask_start_date":
                data["start_date"] = selected_option
                session["state"] = "ask_end_date"
                return jsonify({"next": "ask_end_date"})

            elif state == "ask_end_date":
                data["end_date"] = selected_option
                session["state"] = "ask_reason"
                return jsonify({"next": "ask_reason"})

            elif state == "ask_reason":
                data["reason"] = selected_option
                requests.post(f"{BASE_URL}/apply", json=data, headers=_headers())
                user_sessions.pop(user_id, None)
                return jsonify({"next": "leave_applied"})

        elif intent == "cancel_leave":
            if state == "ask_leave_id":
                requests.post(f"{BASE_URL}/cancel", json={"leave_id": selected_option}, headers=_headers())
                user_sessions.pop(user_id, None)
                return jsonify({"next": "leave_cancelled"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    app.run(debug=True)
