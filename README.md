# Hired

An AI-assisted recruiting platform that helps companies manage job applicants, grade CVs, and automate interview outreach.

---

## Problem

Recruiters spend a disproportionate amount of time on repetitive, low-value tasks — manually reviewing CVs, deciding who to advance, and drafting individual outreach emails. This slows down hiring and introduces inconsistency.

## Solution

Hired automates the most time-consuming parts of the recruiting workflow. It grades applicants automatically using AI, surfaces the strongest candidates first, and generates personalized interview or rejection emails with one click — all from a simple recruiter dashboard.

## Target Users

Recruiting teams and hiring managers at small to mid-sized companies who manage a high volume of applicants and want to reduce manual work without sacrificing quality.

---

## Quick Start

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/hired.git
   cd hired
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Fill in MISTRAL_API_KEY and MISTRAL_MODEL in .env
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## AI Components Disclosure

### 1. Where AI Is Used

   - **CV Summarization & Grading** — Applicant resumes are automatically summarized and graded against the job description to help prioritize candidates.
   - **Email Generation** — Interview scheduling and rejection emails are drafted automatically using the Mistral language model, based on the job posting and candidate resume. Recruiters review and can edit all emails before sending.

   All AI-generated content is presented to the recruiter for review before any action is taken. No emails are sent without explicit recruiter approval.

### 2. Why These Models

   Mistral was chosen as the primary LLM for email generation due to its GDPR compliance — all data is processed within EU infrastructure, which is a hard requirement when handling candidate personal data. This makes it suitable for recruiting workflows without additional data processing agreements or residency workarounds that would be needed with US-based providers like OpenAI or Anthropic.

   The trade-off is that Mistral's largest models are somewhat less capable than GPT-4 or Claude on open-ended generation tasks, but for structured outputs like recruitment emails — where the format is predictable and Guardrails enforces a schema — this gap is acceptable. Temperature is fixed at 0 across all calls to maximise consistency and reduce variance between runs.

### 3. Guardrails Implemented

   | Concern | Approach |
   |---|---|
   | Output structure | Guardrails AI enforces `EmailSchema` (subject + body) and `CVSummarySchema` on all LLM outputs |
   | PII exposure | CVs are summarised before grading — the raw resume is never passed directly to the grading prompt, reducing the surface area of personal data in context |
   | Prompt injection | CV summarisation acts as a partial defence — injected instructions embedded in a candidate's resume are less likely to survive summarisation intact before reaching downstream prompts |
   | Consistency | Temperature = 0 on all calls eliminates sampling randomness |
   | Human in the loop | No email is sent without recruiter review and explicit approval |

   **Known gaps to address:**
   - No input filtering for toxicity or explicit prompt injection attempts
   - No rate limiting on AI calls per user session
   - Max tokens and timeout bounds are not yet explicitly set — a runaway generation would currently block the thread

### 4. Quality & Observability

   Currently, there is no telemetry, logging, or eval pipeline in place. This is the most significant operational risk in the current state of the project. Planned improvements in priority order:

   1. **Error handling & timeouts** — AI calls should be wrapped in try/except with a timeout, and failures should surface a user-friendly message rather than crashing the app
   2. **Structured logging** — log each AI call with timestamp, model, prompt version, input hash, output, and Guardrails validation result (pass/fail)
   3. **Prompt version tracking** — system prompts should be versioned (e.g., stored with a `v1`, `v2` label) so that changes can be correlated with changes in output quality
   4. **Offline evals** — a small golden set of CVs with known expected grades can be used to catch regressions when prompts or models change
   5. **Guardrails failure rate monitoring** — tracking how often schema validation fails is a leading indicator of prompt drift or model degradation

### 5. Known Risks & Mitigations

| Risk | Mitigation |
|---|---|
| **Biased grading / unfair candidate ranking** | CVs are summarised before grading to produce a normalised input, reducing the influence of formatting, name, or writing style on scores. Recruiters see raw grades but make all final decisions. |
| **Prompt injection via CV** | CV summarisation acts as a sanitisation step — instructions embedded in a candidate's resume are unlikely to survive summarisation intact before reaching downstream prompts. |
| **PII leakage through LLM** | Raw CVs are never passed directly to the grading prompt. Summarisation reduces the personal data surface area sent to the model. Mistral processes all data within EU infrastructure under GDPR. |
| **App crash on AI failure** | Email drafts are cached in session state — if generation fails mid-session the recruiter is not left with a broken form. Full error handling and timeouts are a planned improvement. |
| **Model hallucination in emails** | Guardrails AI enforces a strict output schema (`EmailSchema`) on every generation. All emails are reviewed and editable by a recruiter before sending. |