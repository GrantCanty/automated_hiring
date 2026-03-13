import streamlit as st
import jobs
import datetime
from utils import load_pdf
from db_utils import get_user_from_db
import time

@st.dialog("Apply to job")
def apply_to_job(job ):
    st.subheader(job["title"])
    with st.form("profile_form"):
        username = st.session_state.username
        user_info = get_user_from_db(username)
        cvs = user_info.get('cv', [])
        cv_names = [cv['name'] for cv in cvs]

        st.selectbox('Choose your CV', cv_names)

        lom_file = st.file_uploader("Upload your Letter of Motivation (PDF only)", type=["pdf"])
        #lom_text , _ = load_pdf(lom_file)

        if st.form_submit_button("Send Application"):
            if not cv_names:
                st.error("Upload a CV on your dashboard")
            elif lom_file is None:
                st.error("Upload a Letter of Motivation.")
            else:
                # Proceed with processing
                lom_text, _ = load_pdf(lom_file)
                
                # Logic to save application to DB goes here
                # save_application(username, job['id'], selected_cv, lom_text)
                
                st.success("Application Sent!")
                time.sleep(.5)
                st.session_state.apply_view = False
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
                        #apply_for_job(job['id'])
                        apply_to_job(job)


    else:
        st.title("Your Jobs")
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
                        return


def apply_for_job(id):
    st.success(f"Application submitted for Job ID: {id}!")


if __name__ == "__main__":
    job_listings()