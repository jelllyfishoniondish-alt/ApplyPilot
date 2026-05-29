# ApplyPilot Devpost Draft

## Tagline

An agent that turns job postings into tracked, tailored application workflows.

## Inspiration

Applying for jobs is not one task. It is a chain of small decisions: understand the role, compare it with your background, adapt materials without inventing facts, submit on time, and follow up. ApplyPilot was built to make that workflow executable instead of advisory.

## What It Does

ApplyPilot helps a job seeker manage an application from discovery to follow-up. Given a job posting, it creates a plan, checks fit against the user's approved profile, identifies missing evidence, drafts a tailored checklist, stores the application record, and schedules the next action.

## How We Built It

- Gemini powers reasoning and planning through Google Cloud Vertex AI Agent Builder.
- MongoDB MCP gives the agent persistent, queryable memory for profiles, jobs, applications, and event logs.
- The local reference implementation in this repository demonstrates the workflow and the exact database operations the deployed agent performs.

## Partner Integration

ApplyPilot uses MongoDB MCP as its operational memory. The agent reads approved profile facts, inserts parsed job records, updates application states, and appends audit events. This makes the workflow resumable, inspectable, and useful across many applications.

## Demo Flow

1. User gives ApplyPilot a target role.
2. ApplyPilot retrieves the user's profile from MongoDB.
3. ApplyPilot produces a fit analysis and application plan.
4. User approves storing the opportunity.
5. ApplyPilot writes the job, application, and event records through MongoDB MCP.
6. ApplyPilot shows the next concrete action and follow-up date.

## Impact

ApplyPilot helps job seekers preserve momentum and quality during a stressful, repetitive process. It is especially useful for students, career switchers, and international applicants who need careful tracking and strong evidence alignment across many roles.

## What Is Next

- Add live Agent Builder deployment instructions with screenshots.
- Add resume and cover-letter artifact generation.
- Add calendar/email integrations behind approval checkpoints.
- Add analytics for which application strategies lead to interviews.
