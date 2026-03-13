import streamlit as st
import uuid


applications = []

def apply(user_id, job_id, letter_of_motivation, cv):
    app = {'id': uuid.uuid1(), 'user_id': user_id, 'job_id': job_id, 'lom': letter_of_motivation, 'cv': cv}
    applications.append(app)
    return True