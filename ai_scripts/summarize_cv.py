import os
from dotenv import load_dotenv
import guardrails as gr
from pydantic import BaseModel, Field

load_dotenv()

MODEL=os.getenv("MISTRAL_MODEL")

class CVSummarySchema(BaseModel):
    skils: list[str] = Field(description="Candidate skills")
    highest_degree: str = Field(description='Highest degree attained')
    years_of_exp: float = Field(description="Total years that candidate has worked")
    job_titles: list[str] = Field(description="Jobs that candidate has worked")
    job_resp: list[str] = Field(description="What resposibilities did the candidate have?")

def get_cv_summary(chat_wrapper, output_schema, applicant_cv):
    # set up system prompt
    system_prompt="Return information about the CV including the candidate's skills, highest degree attained, total years of experience, jobs that the candidate has worked, and the job responsibilities"

    # give context on the user from the job description and cv. respon
    user_context = f"candidate cv: {applicant_cv}"
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_context}
    ]

    guard = gr.Guard.for_pydantic(output_class=output_schema, messages=messages)

    raw_output, validated_output, *rest = guard(
        llm_api=chat_wrapper,
        model=MODEL)

    return raw_output, validated_output, rest