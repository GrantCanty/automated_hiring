import streamlit as st

# example record
mock_users = {
        "alice": {
            'id': 0,
            "username": "alice",
            "password_hash": "password123",
            "role": "applicant",
            "company": None,
            "first_name": "Alice",
            "last_name": "Smith"
        },
        'jeff': {
            'id': 2,
            'username': 'jeff',
            "password_hash": "password123",
            "role": "applicant",
            "company": None,
        },
        "bob": {
            'id': 1,
            "username": "bob",
            "password_hash": "admin789", 
            "role": "recruiter",
            "company": 'Google'
        }
    }

def get_user_from_db(username):
    """
    Mocks a PostgreSQL query. 
    In production, use: conn.query("SELECT * FROM users WHERE username = :u", params={"u": username})
    """
    
    return mock_users.get(username.lower())

def add_user_to_db(username, password, role, company):
    if get_user_from_db(username) == None:
        u_lower = username.lower()
        r_lower = role.lower()
        db_data = {'username': username, 'password_hash': password, 'role': r_lower, 'company': company}
        mock_users[u_lower] = db_data

def update_user_profile(username, first_name, last_name, cv):
    return