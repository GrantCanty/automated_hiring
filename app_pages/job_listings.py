import streamlit as st
import jobs
import datetime
from utils import load_pdf
from db_utils import get_user_from_db
from applications import apply
import time
import threading
from ai_scripts import grade_applicant
from applications import get_job_and_applicant_info

@st.dialog("Apply to job")
def apply_to_job(job ):
    st.subheader(job["title"])
    with st.form("profile_form"):
        username = st.session_state.username
        user_info = get_user_from_db(username)
        cvs = user_info.get('cv', [])
        cv_names = [cv['name'] for cv in cvs]

        selected_cv = st.selectbox('Choose your CV', cv_names)

        lom_file = st.file_uploader("Upload your Letter of Motivation (PDF only)", type=["pdf"])

        if st.form_submit_button("Send Application"):
            if not cv_names:
                st.error("Upload a CV on your dashboard")
            elif lom_file is None:
                st.error("Upload a Letter of Motivation.")
            else:
                # Proceed with processing
                lom_text, _ = load_pdf(lom_file)
                
                # Logic to save application to DB goes here
                final_cv = [cv['content'] for cv in cvs if cv['name'] == selected_cv]
                resp, id = apply(username, job['id'], lom_text, final_cv)

                if resp:
                    app_info = get_job_and_applicant_info(id)
                    thread = threading.Thread(
                        target=grade_applicant.grade_applicant,
                        args=(app_info,)
                    )
                    thread.start()

                    st.success("Application Sent!")
                    time.sleep(.5)
                    st.session_state.apply_view = False
                    st.rerun()
                else:
                    st.error("Error saving application")

@st.dialog("Edit job")
def edit_job(job ):
    st.subheader(job["title"])
    with st.form("profile_form"):
        job_title = st.text_input("First Name", value=job.get('title', ""))
        job_description = st.text_area("Last Name", value=job.get('description', ""))

        submit = st.form_submit_button("Save Changes")
        if submit:
            jobs.edit_job(job['id'], job_title, job_description)
            st.rerun()

@st.dialog("Create job")
def create_job():
    st.subheader("Job Info")
    with st.form("profile_form"):
        job_title = st.text_input("Job Title")
        start_date = st.date_input("Start Date")
        salary = st.number_input("Salary")
        job_description = st.text_area("Job Description")

        job = {'title': job_title, 'company': st.session_state.company, 'salary': salary, 'start_date': start_date, 'description': job_description}
        submit = st.form_submit_button("Save Changes")
        if submit:
            jobs.create_job(job)
            st.rerun()

def job_listings():
    if st.session_state.company == None and st.session_state.role == 'applicant':
        st.title("Jobs")
        for job in jobs.jobs:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(job['title'])
                    st.write(job['company'])
                    st.write(f'Start date: {job["start_date"]}')
                    
                    date_posted = job['date_posted']
                    today = datetime.date.today()
                    delta =  today - date_posted
                    days_ago = 'Today' if delta.days == 0 else f'{delta.days} ago' if delta.days <= 6 else date_posted.isoformat()
                    st.write(f'Posted: {days_ago}')

                    st.write(job['description'])
                
                with col2:
                    if st.button('Apply', key=f"apply_{job['id']}"):
                        st.session_state.apply_view = True
                        apply_to_job(job)


    else:
        st.title("Your Jobs")
        if st.button("New job"):
            create_job()
        j = list(filter(lambda c: c['company'] in st.session_state.company, jobs.jobs ))
        for job in j:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(job['title'])
                    st.write(job['company'])
                    st.write(job['description'])
                
                with col2:
                    if st.button('Edit', key=f"apply_{job['id']}"):
                        #apply_for_job(job['id'])
                        edit_job(job)
                        return


def apply_for_job(id):
    st.success(f"Application submitted for Job ID: {id}!")


if __name__ == "__main__":
    job_listings()