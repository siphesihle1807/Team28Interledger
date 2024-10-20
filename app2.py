import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

# Function to load JSON data from external files with error handling
def load_json_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} does not exist.")
        return None
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON data from {file_path}: {e}")
        return None

# Load wallets and JWKS from external JSON files
wallets = load_json_data('wallets.json')
jwks = load_json_data('jwks.json')

if wallets is None or jwks is None:
    print("Error loading external JSON files. Make sure the files are present and valid.")
    exit(1)  # Exit if JSON files cannot be loaded

@app.route('/', methods=['GET'])
def get_wallet_address():
    wallet_url = "https://rafiki.money/alice"  # Default wallet to retrieve (Alice)
    
    if wallet_url in wallets:
        response_data = {
            "id": wallet_url,
            **wallets[wallet_url]
        }
        return jsonify(response_data), 200

    return jsonify({"error": "Wallet Address Not Found"}), 404

@app.route('/<username>/jwks.json', methods=['GET'])
def get_jwks(username):
    wallet_url = f"https://rafiki.money/{username}/jwks.json"
    
    if wallet_url in jwks:
        return jsonify(jwks[wallet_url]), 200

    return jsonify({"error": "JWKS Not Found"}), 404

@app.route('/transfer', methods=['POST'])
def transfer_money():
    data = request.get_json()
    
    sender = data.get('sender')
    receiver = data.get('receiver')
    amount = data.get('amount')

    if sender not in wallets or receiver not in wallets:
        return jsonify({"error": "Invalid wallet address"}), 404

    if amount <= 0:
        return jsonify({"error": "Transfer amount must be positive"}), 400

    if wallets[sender]['balance'] < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    # Deduct amount from sender's wallet and add to receiver's wallet
    wallets[sender]['balance'] -= amount
    wallets[receiver]['balance'] += amount

    return jsonify({
        "message": "Transfer successful",
        "sender_balance": wallets[sender]['balance'],
        "receiver_balance": wallets[receiver]['balance']
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
