users_db = {
    "admin": {"password": "admin123", "role": "admin"},
    "user1": {"password": "user123", "role": "user"},
}

def authenticate(username, password):
    user = users_db.get(username)

    if user and user["password"] == password:
        return {
            "username": username,
            "role": user["role"]
        }

    return None