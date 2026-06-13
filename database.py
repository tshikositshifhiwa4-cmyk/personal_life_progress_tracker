"""
database.py — PostgreSQL connection, queries, helpers
"""
import psycopg2
import psycopg2.extras
from config import DB_CONFIG
from datetime import date, timedelta
import os


def get_db_connection():
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        return psycopg2.connect(database_url)
    return psycopg2.connect(**DB_CONFIG)


# ── SAVE DAILY CHECK-IN ───────────────────────
def save_checkin(data: dict):
    sql = """
        INSERT INTO daily_checkins (
            checkin_date, day_type, day_of_week, is_lab_day, church_required,
            lab_completed, class_completed, job_applications_completed,
            msc_completed, portfolio_completed, household_completed,
            selfcare_completed, rest_completed, church_completed,
            main_achievement, tomorrow_major_task, mood, notes,
            job_applications_count
        ) VALUES (
            %(checkin_date)s, %(day_type)s, %(day_of_week)s, %(is_lab_day)s, %(church_required)s,
            %(lab_completed)s, %(class_completed)s, %(job_applications_completed)s,
            %(msc_completed)s, %(portfolio_completed)s, %(household_completed)s,
            %(selfcare_completed)s, %(rest_completed)s, %(church_completed)s,
            %(main_achievement)s, %(tomorrow_major_task)s, %(mood)s, %(notes)s,
            %(job_applications_count)s
        )
        ON CONFLICT (checkin_date) DO UPDATE SET
            day_type = EXCLUDED.day_type,
            lab_completed = EXCLUDED.lab_completed,
            class_completed = EXCLUDED.class_completed,
            job_applications_completed = EXCLUDED.job_applications_completed,
            msc_completed = EXCLUDED.msc_completed,
            portfolio_completed = EXCLUDED.portfolio_completed,
            household_completed = EXCLUDED.household_completed,
            selfcare_completed = EXCLUDED.selfcare_completed,
            rest_completed = EXCLUDED.rest_completed,
            church_completed = EXCLUDED.church_completed,
            main_achievement = EXCLUDED.main_achievement,
            tomorrow_major_task = EXCLUDED.tomorrow_major_task,
            mood = EXCLUDED.mood,
            notes = EXCLUDED.notes,
            job_applications_count = EXCLUDED.job_applications_count;
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, data)
        conn.commit()
    finally:
        conn.close()


# ── WEEKLY STATS FOR DASHBOARD ────────────────
def get_weekly_stats(week_start: date, week_end: date) -> dict:
    sql = """
        SELECT
            COUNT(*) AS total_checkins,
            SUM(
                lab_completed + class_completed + job_applications_completed +
                msc_completed + portfolio_completed + household_completed +
                selfcare_completed + rest_completed +
                CASE WHEN church_required THEN church_completed ELSE 0 END
            ) AS total_tasks_completed,
            SUM(COALESCE(job_applications_count, 0)) AS total_job_applications,
            SUM(msc_completed)         AS msc_days,
            SUM(lab_completed)         AS lab_days,
            SUM(class_completed)       AS class_days,
            SUM(church_completed)      AS church_days,
            SUM(selfcare_completed)    AS selfcare_days,
            SUM(rest_completed)        AS rest_days
        FROM daily_checkins
        WHERE checkin_date BETWEEN %(start)s AND %(end)s;
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql, {'start': week_start, 'end': week_end})
            row = cur.fetchone()
            if not row or row['total_checkins'] == 0:
                return {}

            result = dict(row)

            # Possible tasks: 7 days × ~8 tasks each
            total_possible = int(row['total_checkins']) * 8
            completed      = int(row['total_tasks_completed'] or 0)
            result['total_possible_tasks']   = total_possible
            result['completion_percentage']  = round((completed / total_possible * 100) if total_possible else 0, 1)
            result['consistency_score']      = round((int(row['total_checkins']) / 7 * 100), 1)

            # Best & worst category
            cats = {
                'MSc Progress':      int(row['msc_days'] or 0),
                'Lab Work':          int(row['lab_days'] or 0),
                'DE Classes':        int(row['class_days'] or 0),
                'Church':            int(row['church_days'] or 0),
                'Self-Care':         int(row['selfcare_days'] or 0),
                'Rest':              int(row['rest_days'] or 0),
                'Job Applications':  int(row['total_job_applications'] or 0),
            }
            filled_cats = {k: v for k, v in cats.items() if v > 0}
            if filled_cats:
                result['best_category']          = max(filled_cats, key=filled_cats.get)
                result['area_needing_attention']  = min(cats, key=cats.get)
            else:
                result['best_category']          = None
                result['area_needing_attention']  = None

            return result
    finally:
        conn.close()


# ── DAILY TREND (for bar chart) ───────────────
def get_daily_trend(week_start: date, week_end: date) -> list:
    sql = """
        SELECT
            checkin_date,
            (
                lab_completed + class_completed + job_applications_completed +
                msc_completed + portfolio_completed + household_completed +
                selfcare_completed + rest_completed +
                CASE WHEN church_required THEN church_completed ELSE 0 END
            ) AS tasks_done
        FROM daily_checkins
        WHERE checkin_date BETWEEN %(start)s AND %(end)s
        ORDER BY checkin_date;
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql, {'start': week_start, 'end': week_end})
            rows = {r['checkin_date']: int(r['tasks_done'] or 0) for r in cur.fetchall()}
    finally:
        conn.close()

    labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    trend  = []
    for i, label in enumerate(labels):
        d    = week_start + timedelta(days=i)
        done = rows.get(d, 0)
        pct  = round(done / 8 * 100)   # out of ~8 tasks
        trend.append({'label': label, 'pct': min(pct, 100)})
    return trend


# ── LATEST WEEKLY REPORT ──────────────────────
def get_latest_weekly_report() -> dict:
    sql = """
        SELECT * FROM weekly_summary
        ORDER BY week_end_date DESC
        LIMIT 1;
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql)
            row = cur.fetchone()
            if row:
                r = dict(row)
                r['week_start'] = r['week_start_date'].strftime('%d %b %Y')
                r['week_end']   = r['week_end_date'].strftime('%d %b %Y')
                return r
            return {}
    finally:
        conn.close()
