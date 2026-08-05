# Adopt an in-memory task store with centralized validation and explicit status rules

## Context

The task tracker API is a learning-oriented FastAPI service that exposes endpoints for creating, reading, updating, deleting, and filtering tasks. Before this decision, the implementation in [app/main.py](../../app/main.py) had route handlers that accepted request payloads directly, but the business rules for status normalization, tag parsing, overdue filtering, and status transitions were not consistently centralized. The project also needed a simple way to support validation without turning the service into a larger infrastructure effort.

The repository structure already separated request models and storage concerns, but the implementation still had to choose between keeping logic lightweight for the mid-course scope or introducing a more elaborate persistence layer. The description in [README.md](../../README.md) made it clear that the intended scope was a robust but manageable API rather than a production-grade backend.

## Decision

The implementation uses an in-memory task store in [app/storage.py](../../app/storage.py) and centralizes validation in [app/models/schemas.py](../../app/models/schemas.py) and [app/business_rules.py](../../app/business_rules.py). In practice, the route handlers in [app/main.py](../../app/main.py) rely on `storage.add_task`, `storage.get_all_tasks`, `storage.get_task_by_id`, and `storage.update_task` for behavior, while `TaskCreate`, `TaskUpdate`, `TaskStatus.normalize`, and `validate_status_transition` enforce the rules exposed by the API.

## Alternatives Considered

- A database-backed implementation using SQLite or PostgreSQL was rejected because it would add migration, connection, and deployment concerns that were disproportionate to the current scope. The project is framed in [README.md](../../README.md) as a learning-focused application, and the existing behavior is already testable without a persistent database layer.

- Inline validation inside the route handlers in [app/main.py](../../app/main.py) was rejected because it would duplicate logic across `create_task`, `patch_task`, and query filtering. Placing validation in the models and business-rules layer keeps the handlers thin and makes the rules easier to reuse and test independently.

- A file-based persistence layer was considered but not chosen because it would have introduced serialization and file-locking concerns without solving the immediate educational objective of keeping the API simple and predictable.

## Trade-offs

This decision favors simplicity, rapid iteration, and a clear mental model for the API. It allows the code to stay compact, makes the validation path easier to follow, and keeps the existing pytest suite focused on the core behavior of the service. The trade-off is that the system does not provide durable storage across process restarts, and it does not support concurrent writers or multi-instance consistency.

The design also gives up some flexibility for shared data. Because state is kept in memory, restarting the service clears all tasks, and the current implementation cannot support long-lived history, shared state, or backup and restore workflows. In exchange, the API remains easy to reason about and well aligned to the repository’s current educational and demo-oriented purpose.

## Consequences

The main consequence is that the API is straightforward to run and test locally. Endpoints such as `/tasks`, `/tasks/{task_id}`, `/health`, and `/version` work without external services, and the validation path is centralized enough that the same rules apply when a task is created or patched. The explicit transition rules in [app/business_rules.py](../../app/business_rules.py) also prevent invalid status changes from slipping through the request layer.

A second consequence is that the architecture is better suited for prototyping than for production use. The in-memory store in [app/storage.py](../../app/storage.py) makes per-request behavior deterministic, but it also means that data disappears when the process exits. This is acceptable for a mid-course project, but it creates a clear boundary around what the system can support.

## Open Questions

- Should the current in-memory store remain as-is for the demo phase, or should it be replaced with a file-backed or database-backed persistence layer before broader use?

- How should task history or audit trails be modeled if the API is extended beyond simple CRUD operations?

- Should overdue calculation be based on UTC, local time, or a configurable timezone setting rather than the current date-based logic in [app/storage.py](../../app/storage.py)?

- Is the current set of status transitions in [app/business_rules.py](../../app/business_rules.py) sufficient for future workflow needs, or should it become configurable rather than hard-coded?
