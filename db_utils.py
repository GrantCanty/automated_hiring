import streamlit as st
import uuid

# example record
mock_users = {
        "alice": {
            'id': 0,
            "username": "alice",
            "password_hash": "password123",
            "role": "applicant",
            "company": None,
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice_smith@gmail.com"
        },
        'jeff': {
            'id': 2,
            'username': 'jeff',
            "password_hash": "password123",
            "role": "applicant",
            "company": None,
            "email": "jeff_deniro@gmail.com"
        },
        'grant': {
            'id': 3,
            'username': 'grant',
            "password_hash": "password123",
            "role": "applicant",
            "company": None,
            "email": "grantcanty1@gmail.com",
            "first_name": "Grant",
            "last_name": "Canty"
        },
        "bob": {
            'id': 1,
            "username": "bob",
            "password_hash": "admin789", 
            "role": "recruiter",
            "company": 'Google',
            "email": "bob_tran@google.com"
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

def update_user_profile(username, first_name, last_name, email, cv, cv_name):
    user = get_user_from_db(username)
    user['first_name'] = first_name
    user['last_name'] = last_name
    user['email'] = email
    user_cv = user.get('cv', [])

    if cv is not None:
        data = {'id': uuid.uuid1(), 'name': cv_name, 'content': cv}
        user_cv.append(data)
        user['cv'] = user_cv
        
    return True

def remove_cv_from_db(username, cv_name):
    user_info = get_user_from_db(username)
    cvs = user_info.get('cv')
    remaining_cvs = [c for c in cvs if c['name'] != cv_name]
    user_info['cv'] = remaining_cvs

    mock_users[username.lower()] = user_info
    return True
