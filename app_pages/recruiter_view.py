import streamlit as st
import applications
import jobs
from db_utils import get_user_from_db

def sortFunc(app):
    grade = app.get('grade')
    return grade if grade is not None else -1

@st.fragment(run_every="2s")
def show_applicants_list():
    user_info = get_user_from_db(st.session_state.username)

    company_jobs = jobs.get_jobs_for_a_company(user_info['company'])
    for job in company_jobs:
        with st.container(border=True):
            st.subheader(f"Applicants for {job['title']}")

            #for application in applications.applications:
            #    app_info = applications.get_job_and_applicant_info(application['id'])
            #    app_info.sort(key=sortFunc, reverse=True)
            apps = applications.get_applicants_by_job_id(job['id'])
            apps.sort(key=sortFunc, reverse=True)
            for app in apps:                
                app_info = applications.get_job_and_applicant_info(app['id'])
                
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