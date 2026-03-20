import streamlit as st
from db_utils import get_user_from_db, update_user_profile, remove_cv_from_db
from utils import load_pdf
from applications import get_applicants_per_company

@st.dialog("Resume")
def view_cv(cv_text):
    st.subheader(cv_text['name'])
    st.write(cv_text['content'])
    if st.button("Return"):
        st.session_state.vew_cv = False
        st.rerun()


def dashboard():
    if st.session_state.company == None and st.session_state.role == 'applicant':
        user_info = get_user_from_db(st.session_state.username)

        if user_info.get('first_name') == None and user_info.get('last_name') == None:
            name = user_info['username']
        else:
            name = user_info['first_name']
        
        st.title(f'Welcome {name}')

        st.subheader("Your Candidate Profile")
        if len(user_info.get('cv', [])) > 0:
            st.subheader('Your CV(s)')
            cv_names = [cv['name'] for cv in user_info.get('cv')]
            
            selected_cv_name = st.selectbox("Select a CV to manage", cv_names)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("View Details"):
                    st.session_state.view_cv = True
                    selected_cv = next(item for item in user_info.get('cv') if item["name"] == selected_cv_name)
                    view_cv(selected_cv)
            
            with col2:
                if st.button("🗑️ Remove CV", type="primary"):
                    remove_cv_from_db(st.session_state.username, selected_cv_name)
                    st.success(f"Removed {selected_cv_name}")
                    st.rerun()
        else:
            st.write("No CVs uploaded yet.")

        st.divider()
        
        with st.form("profile_form"):
            st.subheader(f"Update your profile")
            first_name = st.text_input("First Name", value=user_info.get('first_name', ""))
            last_name = st.text_input("Last Name", value=user_info.get('last_name', ""))
            email = st.text_input('Email', value=user_info.get('email', ""))

            # 2. File Uploader for CV
            cv_file = st.file_uploader("Upload your CV (PDF only)", type=["pdf"])
            
            submit = st.form_submit_button("Save Profile")

            if submit:
                cv_text, cv_file_name = load_pdf(cv_file)

                # 3. Save to local files
                success = update_user_profile(
                    st.session_state.username, 
                    first_name,
                    last_name,
                    email,
                    cv_text,
                    cv_file_name
                )

                st.rerun()
                
                if success:
                    st.success("Profile updated successfully!")
                else:
                    st.error("Something went wrong.")

    elif st.session_state.company is not None and st.session_state.role == 'recruiter':
        user_info = get_user_from_db(st.session_state.username)
        
        if user_info.get('first_name') == None and user_info.get('last_name') == None:
            name = user_info['username']
        else:
            name = user_info['first_name']
        
        st.title(f'Welcome {name}')
        
        with st.form("profile_form"):
            st.subheader(f"Update your profile")
            first_name = st.text_input("First Name", value=user_info.get('first_name', ""))
            last_name = st.text_input("Last Name", value=user_info.get('last_name', ""))
            email = st.text_input('Email', value=user_info.get('email', ""))
            
            submit = st.form_submit_button("Save Profile")

            if submit:

                # 3. Save to local files
                success = update_user_profile(
                    st.session_state.username, 
                    first_name,
                    last_name,
                    email,
                    None,
                    None
                )

                st.rerun()
                
                if success:
                    st.success("Profile updated successfully!")
                else:
                    st.error("Something went wrong.")
        

if __name__ == "__main__":
    dashboard()