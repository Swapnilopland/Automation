from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api"
user_sessions = {}

@app.route('/chat/clock', methods=['POST'])
def clock_module():
    user_id = request.json.get("user_id")
    selected_option = request.json.get("selected_option").lower()

    # ==== MAIN MENU ====
    if selected_option == "clock":
        return jsonify({"next": "clock_menu"})

    # ==== CLOCK IN ====
    elif selected_option == "clock_in":
        requests.post(f"{BASE_URL}/clock-in", headers=_headers())
        return jsonify({"next": "clocked_in"})

    # ==== CLOCK OUT ====
    elif selected_option == "clock_out":
        requests.post(f"{BASE_URL}/clock-out", headers=_headers())
        return jsonify({"next": "clocked_out"})

    # ==== VIEW LOGS ====
    elif selected_option == "view_logs":
        requests.get(f"{BASE_URL}/clock-logs", headers=_headers())
        return jsonify({"next": "show_clock_logs"})

    elif selected_option == "view_today":
        requests.get(f"{BASE_URL}/clock-logs?date=today", headers=_headers())
        return jsonify({"next": "show_today_status"})

    elif selected_option == "view_by_date":
        user_sessions[user_id] = {"intent": "clock_range"}
        return jsonify({"next": "ask_start_date"})

    elif user_id in user_sessions and user_sessions[user_id].get("intent") == "clock_range":
        session = user_sessions[user_id]
        if "start_date" not in session:
            session["start_date"] = selected_option
            return jsonify({"next": "ask_end_date"})
        else:
            end_date = selected_option
            start_date = session["start_date"]
            requests.get(f"{BASE_URL}/clock-logs?start_date={start_date}&end_date={end_date}", headers=_headers())
            user_sessions.pop(user_id, None)
            return jsonify({"next": "show_clock_logs_by_date"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    app.run(debug=True)
