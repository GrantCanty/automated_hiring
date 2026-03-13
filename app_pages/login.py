import streamlit as st
import bcrypt
from db_utils import get_user_from_db

def login():
    st.title("Log in")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit = st.form_submit_button("Log in")

        if submit:
            user = get_user_from_db(username)

            if user and password == user['password_hash']:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = user['role']
                if user.get('company') == None:
                    st.session_state.company = None
                else:
                    st.session_state.company = user.get('company')

                st.success(f"Logged in as {username}")
                st.rerun()
            else:
                st.error("Invalid username or pwd")
        
    st.write("Don't have an account?")
    if st.button("Create an account"):
        # This is a bit of a hack to "switch" pages programmatically 
        # if you don't want them to use the sidebar
        st.switch_page("app_pages/signup.py")



if __name__ == "__main__":
    login()