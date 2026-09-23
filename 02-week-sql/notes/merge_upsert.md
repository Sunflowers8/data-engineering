# MERGE and UPSERT

## MERGE

`MERGE` synchronizes incoming data with an existing target table.

The Week 2 exercise used:

- `employee_merge` as the target
- `employee_staging` as the source
- `employee_id` as the matching business key

### Logic

If the employee already exists:

`WHEN MATCHED` → UPDATE

If the employee does not exist:

`WHEN NOT MATCHED` → INSERT

The exercise updated Ram's salary from 25,000 to 28,000 and inserted Gita as a new employee.

## UPSERT

UPSERT means:

`UPDATE + INSERT`

PostgreSQL supports this using:

`INSERT ... ON CONFLICT ... DO UPDATE`

The Week 2 exercise attempted to insert Ram again using the same primary key.

Because `employee_id = 2` already existed, PostgreSQL detected the conflict and updated Ram's salary instead.

## EXCLUDED

Inside `ON CONFLICT`, `EXCLUDED` represents the incoming record that PostgreSQL attempted to insert.

Example:

`EXCLUDED.salary`

means the salary value from the incoming row.

## MERGE vs ON CONFLICT

MERGE asks:

Does the source record match an existing target record?

- MATCHED → perform an action such as UPDATE
- NOT MATCHED → perform an action such as INSERT

ON CONFLICT asks:

Can this INSERT be completed without violating a UNIQUE or PRIMARY KEY constraint?

- No conflict → INSERT
- Conflict → perform the specified action such as UPDATE

## Key Takeaways

- MERGE is useful for synchronizing source and target datasets.
- A stable key is required to determine whether records represent the same entity.
- UPSERT combines insert and update behavior.
- PostgreSQL implements UPSERT using `ON CONFLICT`.
- `EXCLUDED` refers to the incoming row.
- PRIMARY KEY or UNIQUE constraints allow PostgreSQL to detect conflicts.
- MERGE and UPSERT are common techniques in incremental data pipelines.