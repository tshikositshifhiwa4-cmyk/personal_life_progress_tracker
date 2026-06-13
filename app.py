"""
Personal Life Progress Tracker
Flask Application — app.py
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_db_connection, save_checkin, get_weekly_stats, get_latest_weekly_report, get_daily_trend
from datetime import date, timedelta
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'princess-tracker-secret-2024')


def today_context():
    """Returns helpful day-of-week flags for templates."""
    today = date.today()
    dow = today.weekday()  # Monday=0, Sunday=6
    return {
        'is_friday': dow == 4,
        'is_sunday': dow == 6,
        'today':     today
    }


# ── HOME ──────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


# ── LAB DAY CHECKLIST ─────────────────────────
@app.route('/lab-day')
def lab_day():
    ctx = today_context()
    ctx['today'] = date.today()
    return render_template('lab_day.html', **ctx)


# ── NO-LAB DAY CHECKLIST ──────────────────────
@app.route('/no-lab-day')
def no_lab_day():
    ctx = today_context()
    ctx['today'] = date.today()
    return render_template('no_lab_day.html', **ctx)


# ── SUBMIT CHECK-IN ───────────────────────────
@app.route('/submit-checkin', methods=['POST'])
def submit_checkin():
    form = request.form
    today = date.today()
    dow   = today.weekday()

    data = {
        'checkin_date':              today,
        'day_type':                  form.get('day_type', 'no_lab'),
        'day_of_week':               today.strftime('%A'),
        'is_lab_day':                form.get('day_type') == 'lab',
        'church_required':           dow in (4, 6),   # Friday or Sunday

        # Checkboxes — presence = 1, absence = 0
        'lab_completed':             int(bool(form.get('lab_completed'))),
        'class_completed':           int(bool(form.get('class_completed'))),
        'job_applications_completed':int(bool(form.get('job_applications_completed'))),
        'msc_completed':             int(bool(form.get('msc_completed'))),
        'portfolio_completed':       int(bool(form.get('portfolio_completed'))),
        'household_completed':       int(bool(form.get('household_completed'))),
        'selfcare_completed':        int(bool(form.get('selfcare_completed'))),
        'rest_completed':            int(bool(form.get('rest_completed'))),
        'church_completed':          int(bool(form.get('church_completed'))),

        # Text fields
        'main_achievement':          form.get('main_achievement', '').strip(),
        'tomorrow_major_task':       form.get('tomorrow_major_task', '').strip(),
        'mood':                      form.get('mood', '').strip(),
        'notes':                     form.get('notes', '').strip(),

        # Numeric
        'job_applications_count':    int(form.get('job_applications_count') or 0),
    }

    try:
        save_checkin(data)
        flash('✨ Check-in saved! You showed up today — that counts.', 'success')
    except Exception as e:
        flash(f'Something went wrong: {str(e)}', 'error')

    return redirect(url_for('index'))


# ── DASHBOARD ─────────────────────────────────
@app.route('/dashboard')
def dashboard():
    today      = date.today()
    week_start = today - timedelta(days=today.weekday())   # Monday
    week_end   = week_start + timedelta(days=6)            # Sunday

    stats       = get_weekly_stats(week_start, week_end) or {}
    daily_trend = get_daily_trend(week_start, week_end)

    # Build insight sentences from stats
    insights = []
    pct = stats.get('completion_percentage', 0)
    if pct:
        insights.append(f"You completed {pct}% of planned activities this week.")
    if stats.get('best_category'):
        insights.append(f"Strongest area: {stats['best_category']}.")
    if stats.get('area_needing_attention'):
        insights.append(f"Area requiring attention: {stats['area_needing_attention']}.")
    if stats.get('total_job_applications'):
        insights.append(f"You submitted {stats['total_job_applications']} job application(s).")
    if stats.get('class_days'):
        insights.append(f"You attended {stats['class_days']} Data Engineering class session(s).")
    if not insights:
        insights = ["Complete your first check-in to see personalised insights here. You've got this, Princess! 🌸"]

    return render_template(
        'dashboard.html',
        stats=stats,
        insights=insights,
        daily_trend=daily_trend,
        week_start=week_start.strftime('%d %b %Y'),
        week_end=week_end.strftime('%d %b %Y'),
    )


# ── WEEKLY REPORT ─────────────────────────────
@app.route('/weekly-report')
def weekly_report():
    report = get_latest_weekly_report() or {}
    return render_template('weekly_report.html', report=report)


# ── RUN ───────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
