import streamlit as st
from db_utils import get_user_from_db
from db_utils import update_user_profile

def dashboard():
    if st.session_state.company == None and st.session_state.role == 'applicant':
        user_info = get_user_from_db(st.session_state.username)

        if user_info.get('first_name') == None and user_info.get('last_name') == None:
            name = user_info['username']
        else:
            name = user_info['first_name']
        
        st.title(f'Welcome {name}')

        st.subheader("Your Candidate Profile")
        with st.form("profile_form"):
            first_name = st.text_input("First Name", value=user_info.get('first_name', ""))
            last_name = st.text_input("Last Name", value=user_info.get('last_name', ""))
            
            # 2. File Uploader for CV
            cv_file = st.file_uploader("Upload your CV (PDF only)", type=["pdf"])
            
            submit = st.form_submit_button("Save Profile")

            if submit:
                cv_bytes = None
                if cv_file is not None:
                    cv_bytes = cv_file.read() # Convert file to bytes for DB storage
                
                # 3. Save to Postgres
                success = update_user_profile(
                    st.session_state.username, 
                    first_name,
                    last_name, 
                    cv_bytes
                )
                
                if success:
                    st.success("Profile updated successfully!")
                else:
                    st.error("Something went wrong.")

        

if __name__ == "__main__":
    dashboard()