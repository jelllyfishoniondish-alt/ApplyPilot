# ApplyPilot

ApplyPilot is an agent for the Google Cloud Rapid Agent Hackathon. It helps job seekers move from "I found a role" to a tracked, tailored application package.

The agent plans the application workflow, checks fit against the user's profile, drafts a targeted application checklist, records the application state, and prepares follow-up actions. The hackathon partner integration is MongoDB MCP, used as the system of record for profiles, jobs, applications, notes, and reminders.

## Hackathon Fit

- Agent name: ApplyPilot
- Challenge: Building Agents for Real-World Challenges
- Track: MongoDB
- Google Cloud: Gemini through Vertex AI Agent Builder / Agent Development Kit
- Partner MCP: MongoDB MCP Server
- Real-world task: manage multi-step job applications with human approval before sending or storing important changes

## What ApplyPilot Does

1. Reads a job posting and the user's reusable profile.
2. Creates a step-by-step application plan.
3. Scores fit and identifies missing evidence or resume bullets.
4. Drafts a tailored application package checklist.
5. Uses MongoDB MCP to persist the job, application state, notes, and follow-up tasks.
6. Keeps the user in control with approval checkpoints before external actions.

## Repository Layout

```text
agent/
  applypilot.agent.yaml      Agent Builder / ADK-oriented system instructions
config/
  mcp.mongodb.example.json   MongoDB MCP client configuration template
devpost/
  PROJECT.md                 Submission draft: pitch, impact, demo flow
src/applypilot/
  agent.py                   Core planning agent
  models.py                  Domain models
  tools.py                   Tool abstractions and MongoDB MCP call planner
  demo.py                    Local demo entry point
tests/
  test_applypilot.py         Standard-library unit tests
```

## Quick Local Demo

Install dependencies, then run the API or the local planning demo.

```bash
python3 -m pip install -e .
PYTHONPATH=src uvicorn applypilot.api:app --host 0.0.0.0 --port 8000
```

The API exposes:

- `POST /analyze-job`
- `GET /jobs`
- `POST /jobs`

`POST /analyze-job` accepts either pasted JD text in `job.description` or a public posting URL in `job.source_url`. When only `source_url` is provided, the backend fetches readable page text before sending the job to Gemini.

Gemini analysis is enabled when Vertex AI environment variables are present:

```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=global
export GOOGLE_GENAI_USE_VERTEXAI=True
export APPLYPILOT_GEMINI_MODEL=gemini-2.5-flash
```

For a quick local demo without `gcloud`, you can also use an API key:

```bash
export GOOGLE_API_KEY=your-gemini-api-key
export APPLYPILOT_GEMINI_MODEL=gemini-2.5-flash
```

If Gemini is not configured or the call fails, `/analyze-job` falls back to the local deterministic analyzer.

Local demo and tests:

```bash
PYTHONPATH=src python3 -m applypilot.demo
PYTHONPATH=src python3 -m unittest discover -s tests
```

The demo does not call a live LLM or database. It shows the deterministic workflow and the MongoDB MCP tool calls that the deployed agent should make.

## MongoDB MCP Setup

1. Create a MongoDB Atlas cluster or use an existing MongoDB deployment.
2. Copy `config/mcp.mongodb.example.json` to your MCP client configuration.
3. Set `MDB_MCP_CONNECTION_STRING` in your runtime environment.
4. In Agent Builder or your ADK runner, register the MongoDB MCP server as a tool source.
5. Create these collections in the `applypilot` database:
   - `profiles`
   - `jobs`
   - `applications`
   - `events`

## Agent Builder Setup

Use [agent/applypilot.agent.yaml](agent/applypilot.agent.yaml) as the canonical agent specification. In Vertex AI Agent Builder, create a new agent named `ApplyPilot`, paste the instruction block, connect Gemini, then add MongoDB MCP as the partner tool.

The agent should require approval before:

- Marking an application as submitted
- Sending messages or emails
- Mutating profile data
- Deleting records

## Open Source License

This project is released under the MIT License. See [LICENSE](LICENSE).
