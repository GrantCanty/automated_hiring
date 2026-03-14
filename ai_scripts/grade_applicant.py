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

class ApplicantGradeScore(BaseModel):
    applicant_grade: float = Field(description="score candidate between 0-10. 0 is bad and 10 is good. Take into account all context from the job listing, cv, question, and answer")

def grade_applicant(application_info):
    print(f'cv used when applying: {application_info["cv"]}')
    raw_cv_summary, cv_summary, summary_rest = get_cv_summary(mistral_chat_wrapper, CVSummarySchema, application_info['cv'])
    
    # set up system prompt
    system_prompt=f"You are a recruiter for {application_info['company']} and are evaluating a candidate for an AI/ML position. Grade the candidate from 0 to 10, with 0 being low and 10 being high"

    # give context about the user and job
    user_context = f"""
        job title: {application_info['job_title']}\n
        job description: {application_info['job_description']}\n
        candidate cv: {cv_summary}\n
        letter of motivation: {application_info['letter_of_motivation']}"""
    
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_context}
    ]

    # force output to a schema
    guard = gr.Guard.for_pydantic(output_class=ApplicantGradeScore, messages=messages)

    # validate output to schmea. failure cases
    raw_score, validated_score, *rest = guard(
        llm_api=mistral_chat_wrapper,
        model=MODEL)
    
    save_applicant_grade(application_info['id'], validated_score['applicant_grade'])


