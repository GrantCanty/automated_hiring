import streamlit as st
import jobs


def job_listings():
    if st.session_state.company == None:
        st.title("Jobs")
        for job in jobs.jobs:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.subheader(job['title'])
                    st.write(job['company'])
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