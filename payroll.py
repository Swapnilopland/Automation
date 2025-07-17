from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api"
user_sessions = {}

@app.route('/chat/payroll', methods=['POST'])
def payroll_module():
    user_id = request.json.get("user_id")
    selected_option = request.json.get("selected_option").lower()

    # === MAIN PAYROLL MENU ===
    if selected_option == "payroll":
        return jsonify({"next": "payroll_menu"})

    # === 1. View All Payslips ===
    elif selected_option == "view_payslips":
        requests.get(f"{BASE_URL}/payroll/payslips", headers=_headers())
        return jsonify({"next": "show_payslip_list"})

    # === 2. Download Payslip for a Specific Month ===
    elif selected_option == "download_payslip":
        user_sessions[user_id] = {"intent": "download_payslip"}
        return jsonify({"next": "ask_month"})

    elif user_id in user_sessions and user_sessions[user_id].get("intent") == "download_payslip":
        session = user_sessions[user_id]
        if "month" not in session:
            session["month"] = selected_option  # expects MM format (e.g. "06")
            return jsonify({"next": "ask_year"})
        else:
            month = session["month"]
            year = selected_option  # expects YYYY format
            url = f"{BASE_URL}/payroll/payslip?month={month}&year={year}"
            requests.get(url, headers=_headers())
            user_sessions.pop(user_id, None)
            return jsonify({"next": "show_payslip_download_link"})

    # === 3. View Salary Breakdown ===
    elif selected_option == "salary_breakdown":
        requests.get(f"{BASE_URL}/payroll/salary-breakdown", headers=_headers())
        return jsonify({"next": "show_salary_components"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    app.run(debug=True)
