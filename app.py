import streamlit as st

# 1. Check login state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None

# 2. Define Page Objects
login_page = st.Page("app_pages/login.py", title="Log In", icon=":material/login:")
signup_page = st.Page("app_pages/signup.py", title="Create Account")
dashboard = st.Page("app_pages/dashboard.py", title="Dashboard", icon=":material/dashboard:")
jobs = st.Page("app_pages/job_listings.py", title="Browse Jobs")
admin = st.Page("app_pages/recruiter_view.py", title="Recruiter Panel")

# 3. Build Dynamic Menu
if st.session_state.authenticated:
    pages = [dashboard, jobs]
    if st.session_state.role == "recruiter":
        pages.append(admin)
    
    # Add a logout button in the sidebar
    if st.sidebar.button("Log out"):
        st.session_state.authenticated = False
        st.rerun()
else:
    pages = [login_page, signup_page]

# 4. Run Navigation
pg = st.navigation(pages)
pg.run()