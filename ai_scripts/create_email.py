import os
from dotenv import load_dotenv
import guardrails as gr
from pydantic import BaseModel, Field
from openai import OpenAI
from ai_scripts.summarize_cv import get_cv_summary, CVSummarySchema
from applications import save_applicant_grade

load_dotenv()

MISTAL_API_KEY=os.getenv('MISTRAL_API_KEY')
MODEL=os.getenv("MISTRAL_MODEL")
#model="mistral-large-latest"

system_prompts = {'interview': ''}

mis_client = OpenAI(
    api_key=MISTAL_API_KEY,
    base_url="https://api.mistral.ai/v1"
)

def mistral_chat_wrapper(messages, model, **kwargs):
    response = mis_client.chat.completions.create(
        model=model,
        messages=messages,
        **kwargs
    )

    return response.choices[0].message.content

class EmailSchema(BaseModel):
    subject: str = Field(description="Subject line of email")
    body: str = Field(description='Body of email')

def generate_email(app_info, decision):
    schedule_link = f'https://www.scheduleme.com/{app_info["company"]}/round-1/18523ab4jmp273sd4a8s'

    if decision != 'reject':
        system_prompt = f"You are part of the recruiting team at {app_info['company']}. This candidate has been accepted for a 1 hour long first round interview. Outline the topic(s) and general flow of the interview for the recruiter to cover."
        user_prompt = f"job posting: {app_info['job_description']}\ncandidate resume: {app_info['cv']}"

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]

        interview_questions = mistral_chat_wrapper(messages, MODEL)
        print(interview_questions)

    system_prompts = {
        'interview': f"You are an automated recruiter at {app_info['company']} reaching out to a candidate about their application. Address the candidate by name. Recruiting email are completely automated, do not include a name, contact email/phone number, or anything else personal when closing the email. Email the applicant about scheduling a 1 hour long first round interview on Zoom. You can include a breif outline of the interview but don't go too in depth",
        'reject': f"You are an automated recruiter at {app_info['company']} reaching out to a candidate about their application. Address the candidate by name. Recruiting email are completely automated, do not include a name, contact email/phone number, or anything else personal when closing the email. Email the applicant to let them know they were rejected. Give a few reasons for why and areas to improve."
    }
    system_prompt = system_prompts[decision]
    if decision == 'interview':
        user_prompt = f"job title: {app_info['job_title']} job posting: {app_info['job_description']}\ncandidate resume: {app_info['cv']}\ncandidate name: {app_info['name']}\nschedule link: {schedule_link}\ninterview questions: {interview_questions}"
    else:
        user_prompt = f"job title: {app_info['job_title']} job posting: {app_info['job_description']}\ncandidate resume: {app_info['cv']}\ncandidate name: {app_info['name']}\n"

    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]

    guard = gr.Guard.for_pydantic(output_class=EmailSchema, messages=messages)

    # validate output to schmea. failure cases
    raw_output, validated_output, *rest = guard(
        llm_api=mistral_chat_wrapper,
        model=MODEL)
    print(validated_output)

    return raw_output, validated_output, rest