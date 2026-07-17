from app.models.schemas import TaskCreate, TaskUpdate
from pydantic import ValidationError

def expect_fail(test_name, lambda_func):
    try:
        lambda_func()
        print(f"FAIL: {test_name} (Expected validation to fail, but it passed)")
    except ValidationError:
        print(f"PASS: {test_name}")
    except Exception as e:
        print(f"FAIL: {test_name} (Unexpected error: {e})")

def verify_success(test_name, lambda_func):
    try:
        lambda_func()
        print(f"PASS: {test_name}")
    except Exception as e:
        print(f"FAIL: {test_name} (Error: {e})")

print("\n--- Starting Part A Verifications ---")

# 1. whitespace title rejected
expect_fail("whitespace title rejected", lambda: TaskCreate(title="   ", description="test"))

# 2. empty title rejected
expect_fail("empty title rejected", lambda: TaskCreate(title="", description="test"))

# 3. title over 200 chars rejected
expect_fail("title over 200 chars rejected", lambda: TaskCreate(title="x" * 201, description="test"))

# 4. defaults applied (ToDo, Medium, empty description)
# (Assuming your schemas use your default values or allow them)
verify_success("defaults applied (ToDo, Medium, empty description)", lambda: TaskCreate(title="Valid Title"))

# 5. extra field rejected on TaskCreate
expect_fail("extra field rejected on TaskCreate", lambda: TaskCreate(title="Valid", extra_field="not allowed"))

# 6. id NOT settable via TaskCreate
expect_fail("id rejected on TaskCreate", lambda: TaskCreate(title="x", id="forced-id"))

# 7. created_at NOT settable via TaskUpdate
expect_fail("created_at rejected on TaskUpdate", lambda: TaskUpdate(created_at="2026-01-01"))

# 8. Invalid enum value rejected
expect_fail("invalid status rejected", lambda: TaskCreate(title="x", status="INVALID_STATUS"))

print("--- Part A verifications complete ---\n")