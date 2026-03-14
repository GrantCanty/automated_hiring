import streamlit as st
import uuid
from db_utils import get_user_from_db
from jobs import get_job_info


applications = []

def apply(username, job_id, letter_of_motivation, cv):
    id = uuid.uuid1()
    app = {'id': id, 'username': username, 'job_id': job_id, 'lom': letter_of_motivation, 'cv': cv}
    print(app)
    applications.append(app)
    return True, id

def get_job_and_applicant_info(id):
    appication = [app for app in applications if app['id'] == id][0]
    
    # get use and job info from the application
    user_info = get_user_from_db(appication['username'])
    job_info = get_job_info(appication['job_id'])

    # prepare needed data for llm
    data = {
        'id': id,
        'name': user_info['first_name'] + ' ' + user_info['last_name'], 
        'company': job_info['company'], 
        'job_description': job_info['description'],
        'job_title': job_info['title'],
        'cv': appication['cv'],
        'letter_of_motivation': appication['lom']
        }
    
    return data

def save_applicant_grade(id, score):
    for i in range(len(applications)):
        if applications[i]['id'] == id:
            applications[i]['grade'] = score
            break