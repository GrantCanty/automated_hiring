## Security

This MVP prioritises speed of iteration over hardened security. The following are known trade-offs that would be addressed before any production deployment:

- **Storage** — Data is currently held in in-memory Python structures rather than a proper database. A production version would use a managed database (e.g. PostgreSQL) with access controls and encrypted storage at rest.
- **Authentication** — User sessions are minimal. A production system would integrate a proper auth provider (e.g. Auth0, Supabase Auth) with role-based access control to separate recruiter and admin permissions.
- **API keys** — Secrets are loaded from a local `.env` file. These would be moved to a secrets manager (e.g. AWS Secrets Manager, HashiCorp Vault) in any deployed environment.
- **Input validation** — There is currently no server-side validation on form inputs beyond what Guardrails enforces on LLM outputs.
- **Audit logging** — No record is kept of who sent which email or made which hiring decision. A production system would maintain a full audit trail.