import streamlit as st
import uuid
from db_utils import get_user_from_db
from jobs import get_job_info


applications = []

def apply(username, job_id, letter_of_motivation, cv):
    id = uuid.uuid1()
    app = {'id': id, 'username': username, 'job_id': job_id, 'lom': letter_of_motivation, 'cv': cv}
    applications.append(app)
    return True, id

def get_job_and_applicant_info(id):
    application = [app for app in applications if app['id'] == id][0]
    
    # get use and job info from the application
    user_info = get_user_from_db(application['username'])
    job_info = get_job_info(application['job_id'])

    grade = application.get('grade', None)

    # prepare needed data for llm
    data = {
        'id': id,
        'name': user_info['first_name'] + ' ' + user_info['last_name'], 
        'company': job_info['company'], 
        'job_description': job_info['description'],
        'job_title': job_info['title'],
        'cv': application['cv'],
        'letter_of_motivation': application['lom']
        }
    
    if grade is not None:
        data['grade'] = grade
    
    return data

def save_applicant_grade(id, score):
    for i in range(len(applications)):
        if applications[i]['id'] == id:
            applications[i]['grade'] = score
            break

def get_applicants_per_company(company_name):
    applicant_count = 0
    apps = applications.copy()
    for app in apps:
        if app['company'] == company_name:
            applicant_count += 1
    
    return applicant_count
