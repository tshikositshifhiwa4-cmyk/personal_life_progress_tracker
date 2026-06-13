"""
etl_weekly_summary.py
Run every Sunday evening to extract, transform, and load the week's data.
Schedule with Windows Task Scheduler: python etl_weekly_summary.py
"""

import psycopg2
import psycopg2.extras
from datetime import date, timedelta
from config import DB_CONFIG


def get_week_range():
    """Returns Monday–Sunday for the just-completed week."""
    today      = date.today()
    week_end   = today
    week_start = today - timedelta(days=today.weekday())  # Monday
    return week_start, week_end


def extract(conn, week_start, week_end):
    sql = """
        SELECT * FROM daily_checkins
        WHERE checkin_date BETWEEN %s AND %s
        ORDER BY checkin_date;
    """
    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(sql, (week_start, week_end))
        return cur.fetchall()


def transform(rows, week_start, week_end):
    if not rows:
        return None

    total_tasks     = 0
    total_possible  = len(rows) * 8
    job_apps        = 0
    msc_days        = 0
    lab_days        = 0
    class_days      = 0
    church_days     = 0
    selfcare_days   = 0
    rest_days       = 0

    for r in rows:
        total_tasks += (
            r['lab_completed'] + r['class_completed'] +
            r['job_applications_completed'] + r['msc_completed'] +
            r['portfolio_completed'] + r['household_completed'] +
            r['selfcare_completed'] + r['rest_completed'] +
            (r['church_completed'] if r['church_required'] else 0)
        )
        job_apps      += r['job_applications_count'] or 0
        msc_days      += r['msc_completed']
        lab_days      += r['lab_completed']
        class_days    += r['class_completed']
        church_days   += r['church_completed']
        selfcare_days += r['selfcare_completed']
        rest_days     += r['rest_completed']

    completion_pct = round(total_tasks / total_possible * 100, 1) if total_possible else 0

    cats = {
        'MSc Progress':     msc_days,
        'Lab Work':         lab_days,
        'DE Classes':       class_days,
        'Church':           church_days,
        'Self-Care':        selfcare_days,
        'Rest':             rest_days,
        'Job Applications': job_apps,
    }
    best_cat  = max(cats, key=cats.get)
    worst_cat = min(cats, key=cats.get)

    # Build natural-language insight
    lines = [
        f"You completed {completion_pct}% of planned activities this week.",
        f"Strongest area: {best_cat}.",
        f"Area requiring attention: {worst_cat}.",
    ]
    if job_apps:
        lines.append(f"You submitted {job_apps} job application(s).")
    if class_days:
        lines.append(f"You attended {class_days} Data Engineering class session(s).")
    if completion_pct == 100:
        lines.append("You achieved 100% — phenomenal week, Princess! 🌸")
    elif completion_pct >= 80:
        lines.append("Excellent consistency this week. Keep the momentum going.")
    elif completion_pct < 50:
        lines.append("It was a tough week. Be gentle with yourself — you still showed up.")

    insight = ' '.join(lines)

    return {
        'week_start_date':        week_start,
        'week_end_date':          week_end,
        'total_tasks_completed':  total_tasks,
        'total_possible_tasks':   total_possible,
        'completion_percentage':  completion_pct,
        'total_job_applications': job_apps,
        'msc_days':               msc_days,
        'lab_days':               lab_days,
        'class_days':             class_days,
        'church_days':            church_days,
        'selfcare_days':          selfcare_days,
        'rest_days':              rest_days,
        'best_category':          best_cat,
        'area_needing_attention': worst_cat,
        'weekly_insight':         insight,
    }


def load(conn, summary):
    sql = """
        INSERT INTO weekly_summary (
            week_start_date, week_end_date,
            total_tasks_completed, total_possible_tasks, completion_percentage,
            total_job_applications, msc_days, lab_days, class_days,
            church_days, selfcare_days, rest_days,
            best_category, area_needing_attention, weekly_insight
        ) VALUES (
            %(week_start_date)s, %(week_end_date)s,
            %(total_tasks_completed)s, %(total_possible_tasks)s, %(completion_percentage)s,
            %(total_job_applications)s, %(msc_days)s, %(lab_days)s, %(class_days)s,
            %(church_days)s, %(selfcare_days)s, %(rest_days)s,
            %(best_category)s, %(area_needing_attention)s, %(weekly_insight)s
        )
        ON CONFLICT (week_start_date, week_end_date) DO UPDATE SET
            total_tasks_completed  = EXCLUDED.total_tasks_completed,
            completion_percentage  = EXCLUDED.completion_percentage,
            total_job_applications = EXCLUDED.total_job_applications,
            best_category          = EXCLUDED.best_category,
            area_needing_attention = EXCLUDED.area_needing_attention,
            weekly_insight         = EXCLUDED.weekly_insight;
    """
    with conn.cursor() as cur:
        cur.execute(sql, summary)
    conn.commit()


def run_etl():
    week_start, week_end = get_week_range()
    print(f"🔄  Running ETL for {week_start} → {week_end}")

    conn = psycopg2.connect(**DB_CONFIG)
    try:
        rows    = extract(conn, week_start, week_end)
        print(f"📥  Extracted {len(rows)} check-in(s).")

        summary = transform(rows, week_start, week_end)
        if not summary:
            print("⚠️   No data found for this week. ETL skipped.")
            return

        load(conn, summary)
        print(f"  Weekly summary loaded successfully.")
        print(f"  Completion: {summary['completion_percentage']}%")
        print(f"  Best area: {summary['best_category']}")
        print(f"  Needs attention: {summary['area_needing_attention']}")
        print(f"\n  {summary['weekly_insight']}")
    finally:
        conn.close()


if __name__ == '__main__':
    run_etl()
