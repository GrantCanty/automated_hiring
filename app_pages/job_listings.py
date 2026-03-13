import streamlit as st
import jobs
import datetime


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
                        apply_for_job(job['id'])


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