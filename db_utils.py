import streamlit as st

# fake record
mock_users = {
        "alice": {
            "username": "alice",
            "password_hash": "password123", # Plain text for testing ONLY
            "role": "applicant",
            "company": None
        },
        "bob": {
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