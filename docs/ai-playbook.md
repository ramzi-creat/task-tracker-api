# Personal AI Playbook

## When I reach for AI first
- Boilerplate scaffolding (new project setup, config files, CI templates) — the shape is well-known and AI gets it right fast.
- Regex patterns and string manipulation — I can verify the output quickly with a test case.
- Explaining an unfamiliar library's API from its docs — AI summarizes faster than I read.

## When I do not reach for AI
- Refactoring a deeply nested legacy module — the context is too project-specific for a fresh AI session to grasp.
- Designing the data model for a new domain — I need to build the reasoning myself before delegating.
- Security-sensitive auth flows — the failure mode of an AI guess is too expensive to risk.

## My non-negotiables
- No AI-generated code is merged without a human-written test covering the happy path.
- I never paste production credentials or customer data into an AI tool.
- Every AI suggestion must be traced back to a line in the codebase before I accept it.

## My review rules
- I always run the linter and test suite on AI output before reading the diff.
- I ask "what did you assume about my codebase?" — a question I don't ask about my own code.
- I re-read the diff line-by-line for AI code; I never trust the summary alone.

## What I am still figuring out
- Whether AI pair-programming helps or hurts my long-term retention of the codebase.
- The right balance between AI-generated tests and hand-written ones.
- When to let AI refactor vs. when to do it myself to keep the mental model.

---

## Decision Card
- For a new feature I reach for: **AI for the scaffold, myself for the domain logic**
- For code review I reach for: **myself first, AI as a second pair of eyes**
- For debugging I reach for: **AI for the hypothesis, the debugger for the proof**
- For infrastructure I reach for: **AI for the config, my team for the architecture**
- I will never paste **production secrets or customer data** into an AI tool.
- My one rule is: **AI proposes, I dispose — nothing ships that I can't explain.**