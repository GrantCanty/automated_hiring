import streamlit as st
import roles
from db_utils import add_user_to_db

def sign_up():
    st.title("Sign up")
    role = st.selectbox("Role", roles.ROLES )

    with st.form("Sign Up"):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        if role == 'admin':
            company = st.selectbox("Company", roles.COMPANIES)
        else:
            company = None
        submit = st.form_submit_button("Sign up")

        if submit:
            add_user_to_db(username, password, role, company)
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = role

            st.success(f"Signed up in as {username}")
            st.rerun()

if __name__ == "__main__":
    sign_up()