import streamlit as st
import applications

@st.fragment(run_every="2s")
def show_applicants_list():
    for application in applications.applications:
        app_info = applications.get_job_and_applicant_info(application['id'])
        
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.subheader(app_info['name'])
                st.write(f"Role: {app_info['job_title']} - {app_info['company']}")
                if app_info.get('grade', None) is not None:
                    st.write(f"Grade: {app_info['grade']}")
                else:
                    st.info('Grading in progress...')

def view_applicants():
    st.title("Applicants")
    show_applicants_list()
        

if __name__ == "__main__":
    view_applicants()