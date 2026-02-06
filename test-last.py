from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)
users = {}  # Dictionary to store user credentials and status

# Helper function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required."}), 400
    
    if username in users:
        return jsonify({"error": "User already exists."}), 400
    
    users[username] = {"password": hash_password(password), "active": True}
    return jsonify({"message": "User registered successfully."}), 201

@app.route('/authenticate', methods=['GET'])
def authenticate():
    username = request.args.get('username')
    password = request.args.get('password')
    
    if username not in users:
        return jsonify({"error": "User not found."}), 404
    
    if not users[username]["active"]:
        return jsonify({"error": "User is deactivated."}), 403
    
    if users[username]["password"] == hash_password(password):
        return jsonify({"message": "Authentication successful."}), 200
    else:
        return jsonify({"error": "Invalid credentials."}), 401

@app.route('/update-password', methods=['PUT'])
def update_password():
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if username not in users:
        return jsonify({"error": "User not found."}), 404
    
    if users[username]["password"] != hash_password(old_password):
        return jsonify({"error": "Incorrect old password."}), 401
    
    users[username]["password"] = hash_password(new_password)
    return jsonify({"message": "Password updated successfully."}), 200

@app.route('/deactivate', methods=['PUT'])
def deactivate():
    data = request.json
    username = data.get('username')
    
    if username not in users:
        return jsonify({"error": "User not found."}), 404
    
    users[username]["active"] = False
    return jsonify({"message": "User deactivated successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)