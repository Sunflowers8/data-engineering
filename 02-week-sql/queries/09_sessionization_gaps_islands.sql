-- ============================================================
-- WEEK 2: SESSIONIZATION AND GAPS & ISLANDS
-- ============================================================

-- ============================================================
-- 1. SESSIONIZATION
-- ============================================================

-- Sessionization groups user events into sessions.
-- In this example, a new session begins when the gap between
-- two events is greater than 30 minutes.

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


-- ============================================================
-- SESSIONIZATION LOGIC
-- ============================================================

-- Example event times:
--
-- 09:00
-- 09:10
-- 09:20
-- 11:30
-- 11:40
--
-- Sessions:
--
-- Session 1 → 09:00, 09:10, 09:20
-- Session 2 → 11:30, 11:40
--
-- The gap between 09:20 and 11:30 is greater than 30 minutes,
-- therefore 11:30 starts a new session.


-- ============================================================
-- 2. GAPS AND ISLANDS
-- ============================================================

-- Gaps and Islands identifies consecutive sequences.
--
-- Example:
--
-- 2026-01-01
-- 2026-01-02
-- 2026-01-03
-- 2026-01-07
-- 2026-01-08
--
-- Island 1 → Jan 1, Jan 2, Jan 3
-- Gap      → Jan 4, Jan 5, Jan 6
-- Island 2 → Jan 7, Jan 8


-- General pattern:

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


-- ============================================================
-- KEY PATTERN
-- ============================================================

-- LAG()
--     ↓
-- Compare current row with previous row
--     ↓
-- CASE
--     ↓
-- Mark beginning of new group as 1
--     ↓
-- Running SUM()
--     ↓
-- Generate session/island ID