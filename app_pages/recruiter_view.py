import streamlit as st
import applications
import jobs
from db_utils import get_user_from_db
from ai_scripts import create_email


def sortFunc(app):
    grade = app.get('grade')
    return grade if grade is not None else -1

def filterFunc(app):
    return app['status'] == 'In Progress'

@st.dialog("Email candidate")
def schedule_interview(app_info, hiring_decision):
    cache_key = f"email_draft_{app_info['id']}"

    if cache_key not in st.session_state:
        with st.spinner("Generating email..."):
            _, email, _ = create_email.generate_email(app_info, hiring_decision)
            st.session_state[cache_key] = email

    email = st.session_state[cache_key]
        
    st.subheader(f"Email Applicant")

    subject = st.text_input("Subject", value=email['subject'])
    body = st.text_area('Email', value=email['body'])

    if st.button("Send"):
        del st.session_state[cache_key]
        st.rerun()

@st.fragment(run_every="2s")
def show_applicants_list():
    user_info = get_user_from_db(st.session_state.username)

    company_jobs = jobs.get_jobs_for_a_company(user_info['company'])
    for job in company_jobs:
        with st.container(border=True):
            apps = applications.get_applicants_by_job_id(job['id'])
            filtered_apps = filter(filterFunc, apps)
            filtered_apps = list(filtered_apps)
            
            if len(filtered_apps) == 0:
                st.subheader("No Applicants")
            else:
                st.subheader(f"Applicants for {job['title']}")
                
                filtered_apps.sort(key=sortFunc, reverse=True)
                for app in filtered_apps:
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
                        
                        with col2:
                            job_id = f"{app_info['id']}"
                            if st.button("Schedule Interview", key=job_id+"1"):
                                schedule_interview(app_info, 'interview')
                            if st.button("Reject", key=job_id+"2"):
                                print("pressed reject button")
                                schedule_interview(app_info, "reject")
                                pass

def view_applicants():
    st.title("Applicants")
    show_applicants_list()
        

if __name__ == "__main__":
    view_applicants()