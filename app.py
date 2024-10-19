from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for wallet addresses with balances
wallets = {
    "https://rafiki.money/alice": {
        "publicName": "Alice",
        "assetCode": "USD",
        "assetScale": 2,
        "authServer": "https://rafiki.money/auth",
        "resourceServer": "https://rafiki.money/op",
        "balance": 100.00  # Alice's initial balance
    },
    "https://rafiki.money/bob": {
        "publicName": "Bob",
        "assetCode": "EUR",
        "assetScale": 2,
        "authServer": "https://rafiki.money/auth",
        "resourceServer": "https://rafiki.money/op",
        "balance": 50.00   # Bob's initial balance
    }
}

# Sample JWKS for Alice and Bob
jwks = {
    "https://rafiki.money/alice/jwks.json": {
        "keys": [
            {
                "kty": "RSA",
                "kid": "alice-key",
                "use": "sig",
                "n": "MODULUS_FOR_ALICE_BASE64",
                "e": "AQAB"  # Example exponent
            }
        ]
    },
    "https://rafiki.money/bob/jwks.json": {
        "keys": [
            {
                "kty": "RSA",
                "kid": "bob-key",
                "use": "sig",
                "n": "MODULUS_FOR_BOB_BASE64",
                "e": "AQAB"  # Example exponent
            }
        ]
    }
}

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
