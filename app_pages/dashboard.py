import streamlit as st

def dashboard():
    if st.session_state.company == None and st.session_state.role == 'applicant':
        st.title('Dashboard')

        

if __name__ == "__main__":
    dashboard()