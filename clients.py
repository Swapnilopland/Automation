from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

AUTH_TOKEN = "your-auth-token"
BASE_URL = "https://dev.otplx.com/api"

@app.route('/chat/clients', methods=['POST'])
def clients_module():
    selected_option = request.json.get("selected_option").lower()
    client_id = request.json.get("client_id")  # optional, only needed for contact info

    # === CLIENTS MAIN MENU ===
    if selected_option == "clients":
        return jsonify({"next": "clients_menu"})

    # === 1. View All Clients ===
    elif selected_option == "view_all_clients":
        requests.get(f"{BASE_URL}/clients/all", headers=_headers())
        return jsonify({"next": "show_all_clients"})

    # === 2. Filter Clients by Status ===
    elif selected_option == "view_active_clients":
        requests.get(f"{BASE_URL}/clients?status=active", headers=_headers())
        return jsonify({"next": "show_active_clients"})

    elif selected_option == "view_inactive_clients":
        requests.get(f"{BASE_URL}/clients?status=inactive", headers=_headers())
        return jsonify({"next": "show_inactive_clients"})

    # === 3. View Contact Info of a Client ===
    elif selected_option == "view_client_contact" and client_id:
        requests.get(f"{BASE_URL}/clients/{client_id}/contact-info", headers=_headers())
        return jsonify({"next": "show_client_contact_info"})

    return jsonify({"next": "invalid_option"})


def _headers():
    return {
        "Authorization": f"Bearer {AUTH_TOKEN}",
        "Content-Type": "application/json"
    }

if __name__ == '__main__':
    app.run(debug=True)
