from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api"
user_sessions = {}

@app.route('/chat/expenses', methods=['POST'])
def expenses_module():
    user_id = request.json.get("user_id")
    selected_option = request.json.get("selected_option").lower()

    # === EXPENSE MAIN MENU ===
    if selected_option == "expenses":
        return jsonify({"next": "expenses_menu"})

    # === 1. View All Expenses ===
    elif selected_option == "view_expenses":
        requests.get(f"{BASE_URL}/expenses/mine", headers=_headers())
        return jsonify({"next": "show_all_expenses"})

    # === 2. Submit a New Expense ===
    elif selected_option == "submit_expense":
        user_sessions[user_id] = {"intent": "submit_expense"}
        return jsonify({"next": "ask_expense_date"})

    elif user_id in user_sessions and user_sessions[user_id].get("intent") == "submit_expense":
        session = user_sessions[user_id]

        if "date" not in session:
            session["date"] = selected_option
            return jsonify({"next": "ask_expense_category"})

        elif "category" not in session:
            session["category"] = selected_option
            return jsonify({"next": "ask_expense_amount"})

        elif "amount" not in session:
            session["amount"] = selected_option
            return jsonify({"next": "ask_expense_remarks"})

        elif "remarks" not in session:
            session["remarks"] = selected_option
            # Assume attachment handled outside
            data = {
                "date": session["date"],
                "category": session["category"],
                "amount": session["amount"],
                "remarks": session["remarks"]
            }
            requests.post(f"{BASE_URL}/expenses/create", headers=_headers(), json=data)
            user_sessions.pop(user_id, None)
            return jsonify({"next": "expense_submitted"})

    # === 3. View Pending Expenses ===
    elif selected_option == "pending_expenses":
        requests.get(f"{BASE_URL}/expenses/mine?status=pending", headers=_headers())
        return jsonify({"next": "show_pending_expenses"})

    # === 4. View Approved Expenses ===
    elif selected_option == "approved_expenses":
        requests.get(f"{BASE_URL}/expenses/mine?status=approved", headers=_headers())
        return jsonify({"next": "show_approved_expenses"})

    # === 5. View Rejected Expenses ===
    elif selected_option == "rejected_expenses":
        requests.get(f"{BASE_URL}/expenses/mine?status=rejected", headers=_headers())
        return jsonify({"next": "show_rejected_expenses"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    app.run(debug=True)
