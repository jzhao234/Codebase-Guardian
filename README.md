# Codebase Guardian

Codebase Guardian is an experimental autonomous codebase maintenance agent. It scans a repository, detects stale project resources, reasons about the issue, suggests a fix, and can optionally apply the fix on a Git branch after verification.

The current MVP focuses on a narrow but real maintenance problem: keeping project documentation and setup files aligned with the actual codebase.

## What It Does

Codebase Guardian can currently:

- Scan a local repository or cloned GitHub repository
- Build a structured repo map with file metadata
- Analyze important project files such as:
  - `README.md`
  - `package.json`
  - `.env.example`
  - source code files
- Detect stale README commands that do not match `package.json` scripts
- Detect environment variables used in source code but missing from `.env.example`
- Rank findings by severity
- Select a finding to handle
- Gather relevant context for the selected finding
- Generate a suggested fix
- Optionally use an LLM for reasoning and fix suggestions
- Optionally use an LLM planner to choose the next agent action
- Apply a safe fix locally
- Create a Git branch before modifying files
- Generate a Git diff
- Rerun analysis to verify the selected issue was resolved
- Commit the fix only if verification passes
- Output a JSON report containing the full agent state and trace

## Why This Project Exists

Codebases often accumulate small maintenance issues over time. Documentation becomes stale, setup instructions stop matching the actual commands, environment variables are added but not documented, and onboarding gets harder.

Codebase Guardian is designed to explore how agentic software can help maintain codebases by combining:

- deterministic repo analysis
- tool-using agents
- LLM-based reasoning
- verification before committing changes
- Git workflow automation

The goal is not to build a simple LLM wrapper. The goal is to build a system where the LLM is only one reasoning layer inside a larger, testable, tool-driven maintenance workflow.

## Current Architecture

The project is organized around a state-driven agent loop.

```text
User CLI Input
    ↓
Repo Loader
    ↓
Agent Loop
    ↓
Resource Auditor Agent
    ↓
Decision Planner
    ↓
Context Gatherer
    ↓
Suggestion Generator / LLM Suggestion Layer
    ↓
Fix Agent
    ↓
Verifier Agent
    ↓
Git Diff / Commit
    ↓
JSON Report
```

## Agent Flow

The current agent loop follows this process:

```text
1. Analyze the repository
2. Detect findings
3. Select the highest-priority finding
4. Gather context for that finding
5. Generate a suggested fix
6. Optionally apply the fix
7. Generate a diff
8. Rerun analysis
9. Commit only if verification passes
10. Save the full agent state as JSON
```

The agent records an `agent_trace` so each step is visible in the output report.

Example trace:

```json
[
  {
    "step": 1,
    "action": "choose_next_action_llm",
    "reason": "The repository has not been analyzed yet.",
    "metadata": {
      "chosen_action": "run_analysis"
    }
  },
  {
    "step": 2,
    "action": "run_analysis",
    "reason": "Analyzed repository and found 1 finding(s)."
  }
]
```

## Agents

### Resource Auditor Agent

The Resource Auditor Agent scans the repository, runs analyzers, and produces findings.

Current checks include:

- README commands that do not exist in `package.json`
- environment variables used in source files but missing from `.env.example`

### Fix Agent

The Fix Agent receives a suggested fix and handles the repair workflow.

It can:

- create a Git branch
- apply a text replacement
- generate a Git diff
- call the Verifier Agent
- commit only if verification passes

### Verifier Agent

The Verifier Agent reruns the analysis after a fix is applied.

It checks whether the selected finding was resolved. If the issue remains, the fix is not committed.

## LLM Integration

Codebase Guardian supports optional LLM usage.

There are currently two LLM-related modes:

### LLM Suggestion Mode

The LLM receives the selected finding and gathered context, then generates a structured suggestion.

The LLM does not directly edit files. It only returns a suggestion.

The deterministic system still controls:

- whether the suggestion is actionable
- whether a file is edited
- whether verification passes
- whether a commit is created

### LLM Planner Mode

The LLM can also be used as a planner to choose the next action in the agent loop.

The planner receives:

- the current goal
- a summary of the current state
- recent agent trace entries
- a list of safe actions

It must choose from allowed actions only.

Example actions:

```text
run_analysis
select_finding
gather_context
generate_suggestion
run_fix_agent
finish
```

This keeps the LLM constrained while still allowing it to participate in the agent’s decision-making process.

## Installation

From the `backend/` directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If dependencies are not installed yet:

```bash
pip install openai python-dotenv pytest
pip freeze > requirements.txt
```

## Environment Variables

Create a `.env` file inside the `backend/` directory:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=your_model_here
```

Example:

```env
OPENAI_MODEL=gpt-4.1-mini
```

Do not commit `.env`.

Make sure `.gitignore` includes:

```gitignore
.env
backend/.env
```

## Usage

Run analysis only:

```bash
python main.py --repo ../demo-run-repo --output demo_analysis.json
```

Run with LLM-generated suggestions:

```bash
python main.py --repo ../demo-run-repo --output demo_llm.json --use-llm
```

Run with LLM planner:

```bash
python main.py --repo ../demo-run-repo --output demo_planner.json --use-llm-planner
```

Run with LLM planner, LLM suggestions, and automatic fix application:

```bash
python main.py --repo ../demo-run-repo --output demo_full.json --use-llm-planner --use-llm --apply-fix
```

## Demo Repository

A simple demo repo can be used to test the agent.

The demo repo contains:

```text
README.md
package.json
```

Example `package.json`:

```json
{
  "scripts": {
    "dev": "next dev",
    "build": "next build"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

Example stale `README.md` command:

```text
npm run serve
```

Since `serve` is not defined in `package.json`, Codebase Guardian detects it as a stale README command.

Expected finding:

```json
{
  "type": "stale_readme_command",
  "severity": "medium",
  "command": "serve",
  "old_text": "npm run serve"
}
```

Expected fix:

```text
Replace npm run serve with npm run dev
```

## Output Report

The output JSON includes:

```text
goal
repo_path
repo_map
findings
selected_finding
selected_context
suggestion
branch
fix_result
diff
verification
commit
agent_trace
final_status
```

This makes the agent’s work inspectable and debuggable.

## Testing

Run all tests:

```bash
pytest
```

The test suite currently covers:

- package analyzer behavior
- resource auditor behavior
- full agent flow
- mocked LLM suggestion flow

The LLM tests use mocked responses so tests do not require real API calls or spend API credits.

## Current Limitations

This is an MVP and still has important limitations:

- The current checks are narrow
- The LLM planner is constrained to a small set of actions
- The system does not yet open GitHub pull requests
- The system does not yet run project tests or linters after fixes
- The system does not yet maintain long-term memory across runs
- The system does not yet use a trained ML risk model
- The current fix applier only supports simple safe text replacements

## Roadmap

Planned improvements:

- Add GitHub Actions integration to run on push and pull requests
- Add GitHub issue / pull request creation
- Add a stronger LLM issue discovery agent
- Add support for architecture rule checks
- Add test gap detection
- Add security hygiene checks
- Add deterministic validation for LLM-generated suggestions
- Add rollback behavior if verification fails
- Add persistent memory across scans
- Add a risk scoring model for prioritizing findings
- Add a dashboard for repo health and agent activity

## Project Vision

The long-term goal is to build a multi-agent codebase maintenance system that can continuously inspect a repository, detect stale or risky resources, reason about what matters, suggest safe fixes, verify changes, and integrate with real developer workflows.

The system is designed around a hybrid approach:

```text
Rules and analyzers provide reliable detection.
LLMs provide flexible reasoning and planning.
Verification keeps the system safe.
Git integration makes the output actionable.
```

Codebase Guardian is currently an MVP, but the architecture is being built toward a more autonomous code maintenance agent framework.
