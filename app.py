from flask import Flask, request, jsonify
from db import Database
from objects.user import User

app = Flask(__name__)

users = []

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return jsonify({'error': 'Name and email are required'}), 400

    # Check if user with the same email already exists in the list
    existing_user = next((user for user in users if user.email == email), None)
    if existing_user:
        return jsonify({'error': 'User with the same email already exists'}), 400

    # Create a new User object
    user = User(name, email)

    # Generate a unique ID for the user
    user_id = len(users) + 1
    user.id = user_id

    # Add the user to the list
    users.append(user)

    return jsonify({'message': 'User created successfully', 'user': str(user)}), 201

if __name__ == '__main__':
    app.run()