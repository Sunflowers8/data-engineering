# Sessionization and Gaps & Islands

## Overview

Sessionization and Gaps & Islands are SQL techniques for analyzing sequential or time-based data.

Both techniques use a similar pattern:

```text
LAG()
   ↓
Compare with previous row
   ↓
CASE
   ↓
Create a 0/1 boundary flag
   ↓
Running SUM()
   ↓
Generate group ID
```

These exercises were studied conceptually during Week 2 using event and date examples.

---

# Sessionization

## What Is Sessionization?

Sessionization groups individual events into separate user sessions.

For example, suppose a user generates events at:

```text
09:00
09:10
09:20
11:30
11:40
```

If a new session begins whenever there is more than **30 minutes of inactivity**, the events become:

```text
Session 1
09:00
09:10
09:20

Session 2
11:30
11:40
```

The gap between:

```text
09:20 → 11:30
```

is greater than 30 minutes, so `11:30` begins a new session.

---

## Step 1 — Find the Previous Event

`LAG()` retrieves the previous event time.

```sql
SELECT user_id,
       event_time,
       LAG(event_time) OVER (
           PARTITION BY user_id
           ORDER BY event_time
       ) AS previous_event
FROM website_events;
```

Conceptually:

```text
event_time    previous_event
09:00         NULL
09:10         09:00
09:20         09:10
11:30         09:20
11:40         11:30
```

---

## Step 2 — Detect a New Session

A `CASE` statement determines whether the current event starts a new session.

```sql
CASE
    WHEN previous_event IS NULL THEN 1
    WHEN event_time - previous_event > INTERVAL '30 minutes' THEN 1
    ELSE 0
END AS new_session
```

Result:

```text
09:00 → 1
09:10 → 0
09:20 → 0
11:30 → 1
11:40 → 0
```

`1` means:

```text
Start a new session
```

`0` means:

```text
Continue the current session
```

---

## Step 3 — Generate Session IDs

A running `SUM()` converts the boundary flags into session numbers.

```sql
SUM(new_session) OVER (
    PARTITION BY user_id
    ORDER BY event_time
) AS session_id
```

Running sum:

```text
new_session    session_id
1              1
0              1
0              1
1              2
0              2
```

Therefore:

```text
09:00 → Session 1
09:10 → Session 1
09:20 → Session 1
11:30 → Session 2
11:40 → Session 2
```

---

## Complete Sessionization Pattern

```sql
WITH event_gaps AS (

    SELECT user_id,
           event_time,

           LAG(event_time) OVER (
               PARTITION BY user_id
               ORDER BY event_time
           ) AS previous_event

    FROM website_events
),

session_flags AS (

    SELECT user_id,
           event_time,
           previous_event,

           CASE
               WHEN previous_event IS NULL THEN 1
               WHEN event_time - previous_event > INTERVAL '30 minutes' THEN 1
               ELSE 0
           END AS new_session

    FROM event_gaps
)

SELECT user_id,
       event_time,
       previous_event,
       new_session,

       SUM(new_session) OVER (
           PARTITION BY user_id
           ORDER BY event_time
       ) AS session_id

FROM session_flags;
```

---

## Why Running SUM Instead of ROW_NUMBER?

`ROW_NUMBER()` increases for every row:

```text
1
2
3
4
5
```

But session IDs should increase only when a **new session begins**.

The boundary flags are:

```text
1
0
0
1
0
```

Their running sum becomes:

```text
1
1
1
2
2
```

That correctly represents the two sessions.

---

# Gaps and Islands

## What Are Gaps and Islands?

The Gaps and Islands pattern identifies groups of consecutive records separated by missing periods or breaks.

Consider:

```text
2026-01-01
2026-01-02
2026-01-03
2026-01-07
2026-01-08
```

There are two continuous groups:

```text
Island 1
Jan 1
Jan 2
Jan 3

Gap
Jan 4
Jan 5
Jan 6

Island 2
Jan 7
Jan 8
```

An **island** is a continuous sequence.

A **gap** is the break between sequences.

---

## Step 1 — Retrieve the Previous Date

```sql
SELECT event_date,
       LAG(event_date) OVER (
           ORDER BY event_date
       ) AS previous_date
FROM daily_events;
```

Conceptually:

```text
event_date    previous_date
Jan 1         NULL
Jan 2         Jan 1
Jan 3         Jan 2
Jan 7         Jan 3
Jan 8         Jan 7
```

---

## Step 2 — Detect a New Island

```sql
CASE
    WHEN previous_date IS NULL THEN 1
    WHEN event_date - previous_date > 1 THEN 1
    ELSE 0
END AS new_island
```

Result:

```text
Jan 1 → 1
Jan 2 → 0
Jan 3 → 0
Jan 7 → 1
Jan 8 → 0
```

---

## Step 3 — Generate Island IDs

Use a running sum:

```sql
SUM(new_island) OVER (
    ORDER BY event_date
) AS island_id
```

Result:

```text
Jan 1 → Island 1
Jan 2 → Island 1
Jan 3 → Island 1
Jan 7 → Island 2
Jan 8 → Island 2
```

---

## Complete Gaps & Islands Pattern

```sql
WITH previous_dates AS (

    SELECT event_date,

           LAG(event_date) OVER (
               ORDER BY event_date
           ) AS previous_date

    FROM daily_events
),

island_flags AS (

    SELECT event_date,
           previous_date,

           CASE
               WHEN previous_date IS NULL THEN 1
               WHEN event_date - previous_date > 1 THEN 1
               ELSE 0
           END AS new_island

    FROM previous_dates
)

SELECT event_date,
       previous_date,
       new_island,

       SUM(new_island) OVER (
           ORDER BY event_date
       ) AS island_id

FROM island_flags;
```

---

# Sessionization vs Gaps & Islands

The two techniques are closely related.

```text
Sessionization
→ usually works with timestamps/events
→ boundary may be inactivity > 30 minutes

Gaps & Islands
→ identifies consecutive sequences
→ boundary may be missing dates or another break
```

Both commonly follow:

```text
LAG
→ compare
→ CASE
→ running SUM
```

---

# Important Portfolio Note

The Week 2 sessionization exercise used conceptual `website_events` data.

The NYC Yellow Taxi dataset does not provide a passenger/user identifier that can reliably represent an individual customer.

Therefore, a fake `user_id` was not created just to force sessionization onto the taxi dataset.

This keeps the project logic consistent with the actual meaning of the source data.

---

# Key Takeaways

- `LAG()` allows comparison with the previous record.
- `CASE` can identify boundaries between groups.
- `1` can represent the start of a new group.
- `0` can represent continuation of the existing group.
- A running `SUM()` converts boundary flags into group IDs.
- Sessionization is useful for event and clickstream analysis.
- Gaps & Islands identifies continuous sequences separated by breaks.
- `ROW_NUMBER()` is not a replacement for the running-sum technique because it increments on every row.
- Data-engineering techniques should only be applied when the source data actually supports them.