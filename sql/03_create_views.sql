-- 03_create_views.sql
-- Reporting Views

-- Current week overview
CREATE OR REPLACE VIEW vw_current_week AS
SELECT
    DATE_TRUNC('week', CURRENT_DATE)::DATE            AS week_start,
    (DATE_TRUNC('week', CURRENT_DATE) + 6)::DATE      AS week_end,
    COUNT(*)                                           AS check_ins,
    SUM(lab_completed)                                 AS lab_days,
    SUM(class_completed)                               AS class_days,
    SUM(msc_completed)                                 AS msc_days,
    SUM(job_applications_completed)                    AS job_days,
    SUM(selfcare_completed)                            AS selfcare_days,
    SUM(rest_completed)                                AS rest_days,
    SUM(church_completed)                              AS church_days,
    SUM(COALESCE(job_applications_count, 0))           AS total_job_apps
FROM daily_checkins
WHERE checkin_date >= DATE_TRUNC('week', CURRENT_DATE)
  AND checkin_date <  DATE_TRUNC('week', CURRENT_DATE) + 7;


-- Mood frequency this week
CREATE OR REPLACE VIEW vw_mood_this_week AS
SELECT
    mood,
    COUNT(*) AS occurrences
FROM daily_checkins
WHERE checkin_date >= DATE_TRUNC('week', CURRENT_DATE)
  AND mood IS NOT NULL
  AND mood <> ''
GROUP BY mood
ORDER BY occurrences DESC;


-- Daily completion % 
CREATE OR REPLACE VIEW vw_daily_completion AS
SELECT
    checkin_date,
    day_of_week,
    (
        lab_completed + class_completed + job_applications_completed +
        msc_completed + portfolio_completed + household_completed +
        selfcare_completed + rest_completed +
        CASE WHEN church_required THEN church_completed ELSE 0 END
    )::NUMERIC / 8.0 * 100  AS completion_pct,
    mood
FROM daily_checkins
ORDER BY checkin_date DESC;
