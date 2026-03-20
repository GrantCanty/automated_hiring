## Responsible AI

- **Model selection** — Smaller, efficient models were chosen over frontier models where the task allows it. This reduces energy consumption per inference and keeps costs low, without meaningfully impacting output quality for structured tasks like email generation and CV summarisation.
- **GDPR compliance** — Mistral was selected specifically because it processes data within EU infrastructure, ensuring candidate personal data never leaves a compliant jurisdiction.
- **PII minimisation** — Raw CVs are summarised before being passed to grading prompts, reducing the amount of personal data in context and limiting exposure across the pipeline.
- **Human oversight** — No automated action is taken on a candidate without recruiter review. All AI-generated emails are editable and require explicit approval before sending. The AI surfaces and ranks; humans decide.
- **Prompt injection mitigation** — CV summarisation acts as a sanitisation step, reducing the risk of malicious instructions embedded in candidate resumes propagating to downstream prompts.