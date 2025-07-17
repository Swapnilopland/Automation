from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api"

@app.route('/chat/insurance', methods=['POST'])
def insurance_module():
    selected_option = request.json.get("selected_option").lower()

    # === INSURANCE MAIN MENU ===
    if selected_option == "insurance":
        return jsonify({"next": "insurance_menu"})

    # === 1. View My Insurance Details ===
    elif selected_option == "view_insurance_details":
        requests.get(f"{BASE_URL}/insurance/my-policy", headers=_headers())
        return jsonify({"next": "show_insurance_details"})

    # === 2. View My Family Members Covered ===
    elif selected_option == "view_family_coverage":
        requests.get(f"{BASE_URL}/insurance/family-members", headers=_headers())
        return jsonify({"next": "show_family_members"})

    # === 3. View Claims History ===
    elif selected_option == "view_claims_history":
        requests.get(f"{BASE_URL}/insurance/claims-history", headers=_headers())
        return jsonify({"next": "show_claims_history"})

    # === 4. Download Policy Document ===
    elif selected_option == "download_policy":
        requests.get(f"{BASE_URL}/insurance/policy-document", headers=_headers())
        return jsonify({"next": "download_policy_document"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    app.run(debug=True)
