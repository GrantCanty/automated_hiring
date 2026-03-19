import streamlit as st
import datetime

jobs = [
    {'id': 0, 'title': "AI Engineer", 'company': 'Microsoft', 'salary': 95000, 'start_date': datetime.date(2026, 4, 12), 'date_posted': datetime.date(2026, 3, 6), 'description': """Overview: We are seeking an AI Engineer to bridge the gap between machine learning research and scalable production applications. You will focus on integrating Large Language Models (LLMs) into our core products to automate complex workflows.

Key Responsibilities:

Design and implement RAG (Retrieval-Augmented Generation) pipelines to improve model accuracy.

Fine-tune open-source models (e.g., Llama, Mistral) for domain-specific tasks.

Optimize inference latency and manage GPU resource allocation.

Collaborate with product teams to define AI safety guardrails and evaluation benchmarks."""},
    {'id': 1, 'title': "Backend Engineer", 'company': 'Google', 'salary': 85000, 'start_date': datetime.date(2026, 4, 6), 'date_posted': datetime.date(2026, 3, 13), 'description': """Overview: As a Frontend Engineer, you will be responsible for the "face" of our platform. We need someone obsessed with performance, accessibility, and creating intuitive user interfaces that make complex data feel simple.

Key Responsibilities:

Develop reusable UI components using React, TypeScript, and Tailwind CSS.

Optimize web applications for maximum speed and scalability across various devices.

Integrate complex REST and GraphQL APIs into the frontend state management (Redux/Zustand).

Conduct code reviews and maintain high standards for UI/UX consistency and unit testing."""},
    {'id': 2, 'title': "Front Engineer", 'company': 'Meta', 'salary': 75000, 'start_date': datetime.date(2026, 3, 23), 'date_posted': datetime.date(2026, 3, 13), 'description': """Overview: We are looking for a Backend Engineer to build the robust, scalable architecture that powers our application. You will handle the "heavy lifting"—from database design to third-party integrations and system security.

Key Responsibilities:

Architect and maintain scalable microservices and server-side logic.

Design efficient database schemas (PostgreSQL/NoSQL) and optimize complex queries.

Implement secure authentication and authorization protocols (OAuth2, JWT).

Build and document internal APIs that provide a seamless interface for the frontend and mobile teams."""},
]

def get_job_info(id):
    return [job for job in jobs if job['id'] == id][0]

def get_jobs_for_a_company(company_name):
    company_jobs = []
    job_listings = jobs.copy()
    
    for job in job_listings:
        if job['company'] == company_name:
            company_jobs.append(job)
    
    return company_jobs
        