<!-- BANNER -->
<div align="center">

# 🌸 Personal Life Progress Tracker

*"I am becoming the woman I prayed to be."*

![Python](https://img.shields.io/badge/Python-3.14-9b59b6?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-f78fb3?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-74b9ff?style=for-the-badge&logo=postgresql&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-9b59b6?style=for-the-badge&logo=javascript&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-CSS3-f78fb3?style=for-the-badge&logo=html5&logoColor=white)

**A full-stack personal productivity system and portfolio-quality Data Engineering solution.**

</div>

---

## About This Project

This is not a generic todo app.

I built this as a personal productivity system designed around my actual life, balancing an MSc research degree, active Data Engineering, university laboratory sessions, weekly church commitments, and personal wellbeing.

The goal was twofold: build something I would actually use every day, and demonstrate end-to-end data engineering skills across the full BI development lifecycle, from raw data capture through ETL pipelines to dashboard insights.

Every feature in this app exists because I needed it.

---

## Features

### Personalised Home Page
- Displays current date and a personal motivational quote
- Two day-type selectors: **Lab Day** and **No-Lab Day**
- Profile picture 

### Smart Daily Check-Ins
- **Lab Day checklist** — tracks lab work, travel, notes, rest, and self-care
- **No-Lab Day checklist** — tracks applications, MSc writing, portfolio work, household tasks
- **Friday rules** — automatically adds Church (18:00–21:00) and GitHub/LinkedIn update tasks
- **Sunday rules** — adds Church, weekly planning, report review, and goal preparation
- **Day-aware labels** — Mon–Thu shows "Data Engineering class attended", Fri–Sun shows "Studying completed"
- Mood selector with buttons (Energised, Focused, Tired, Stressed, Happy, Overwhelmed, Sick)
- Live progress bar that fills as you tick items — confetti at 100% 🎉
- Free-text fields for achievements, tomorrow's priorities, and notes

### Dashboard
- Ring chart for weekly completion percentage
- KPI counters (tasks, job applications, MSc days, lab days, church, self-care, rest)
- Weekly productivity trend bar chart
- Rotating insights slideshow with auto-advance and dot navigation
- Best performing area and area needing attention cards
- Weekly consistency score

### Automated Email Reminder
- Sends a personalised HTML email every day at 22:00
- Warm, encouraging tone with a direct link to the tracker
- Automated via cron, no manual intervention required

### Weekly ETL Pipeline
- Runs automatically every Sunday at 21:00
- **Extracts** all check-ins from the past 7 days
- **Transforms** — calculates 10+ metrics and generates a natural-language insight summary
- **Loads** results into the `weekly_summary` table
- Dashboard reads live from `daily_checkins` and historical from `weekly_summary`

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                           │
│                                                                 │
│   Home Page  →  Lab Day / No-Lab Day Checklist  →  Dashboard    │
│   (index.html)      (lab_day / no_lab_day.html)  (dashboard)    │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP (Flask routes)
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       FLASK BACKEND                             │
│                                                                 │
│   app.py          → Route handling, form processing             │
│   database.py     → All PostgreSQL queries                      │
│   config.py       → Environment variable management             │
└──────────────┬──────────────────────────┬───────────────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────┐     ┌────────────────────────────────────┐
│   PostgreSQL DB      │     │         AUTOMATION LAYER           │
│                      │     │                                    │
│  daily_checkins      │     │  send_daily_reminder.py            │
│  weekly_summary      │◄────│  → cron: 22:00 daily               │
│                      │     │                                    │
│  Views:              │     │  etl_weekly_summary.py             │
│  vw_current_week     │◄────│  → cron: 21:00 every Sunday        │
│  vw_daily_completion │     │                                    │
│  vw_mood_this_week   │     │  Gmail SMTP                        │
└──────────────────────┘     │  → HTML email reminder             │
                             └────────────────────────────────────┘
```

---

## Project Mind Map

```
                        PERSONAL LIFE PROGRESS TRACKER
                                     │
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
     FRONTEND                    BACKEND                    DATA LAYER
          │                           │                          │
    ┌─────┴──────┐             ┌──────┴──────┐            ┌──────┴──────┐
    │  Pages     │             │   Flask     │            │ PostgreSQL  │
    │ ─ Home     │             │   Routes    │            │  Tables     │
    │ ─ Lab Day  │             │ ─ /         │            │ ─ daily_    │
    │ ─ No-Lab   │             │ ─ /lab-day  │            │   checkins  │
    │ ─ Dashboard│             │ ─ /no-lab   │            │ ─ weekly_   │
    │ ─ Report   │             │ ─ /dashboard│            │   summary   │
    └─────┬──────┘             │ ─ /submit   │            └──────┬──────┘
          │                    └──────┬──────┘                   │
    ┌─────┴──────┐                    │                   ┌──────┴──────┐
    │  Features  │             ┌──────┴──────┐            │   Views     │
    │ ─ Checklist│             │  database.py│            │ ─ current   │
    │ ─ Mood     │             │ ─ save      │            │   week      │
    │ ─ Progres s│             │ ─ stats     │            │ ─ daily     │
    │   bar      │             │ ─ trends    │            │   completion│
    │ ─ Confetti │             │ ─ reports   │            │ ─ mood      │
    └─────┬──────┘             └─────────────┘            └─────────────┘
          │
    ┌─────┴──────┐
    │ Animations │
    │ ─ Ring     │
    │   charts   │
    │ ─ Counters │
    │ ─ Bar chart│
    │ ─ Slider   │
    │ ─ Blobs    │
    └────────────┘
          
    AUTOMATION
         │
    ┌────┴────────────────────┐
    │         cron            │
    ├─────────────────────────┤
    │ 22:00 daily             │
    │ → send_daily_reminder   │
    │ → Gmail SMTP HTML email │
    ├─────────────────────────┤
    │ 21:00 every Sunday      │
    │ → etl_weekly_summary    │
    │ → Extract → Transform   │
    │ → Load → weekly_summary │
    └─────────────────────────┘
```

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | HTML5, CSS3, JavaScript (ES6) | UI, animations, interactivity |
| Backend | Python 3.14 + Flask | Server, routing, form handling |
| Database | PostgreSQL 18 | Data storage and reporting views |
| ORM / Driver | psycopg2-binary | Python ↔ PostgreSQL connection |
| Config | python-dotenv | Environment variable management |
| Email | Gmail SMTP | Automated HTML reminder emails |
| Automation | cron (macOS) | Scheduled email and ETL jobs |
| Editor | VS Code | Development environment |
| Version Control | Git + GitHub | Source control and portfolio |

---

##  Screenshots

### Home Page
<img width="1440" height="787" alt="homepahe" src="https://github.com/user-attachments/assets/53187b24-2258-4d73-963b-19e96c7f0c1e" />


---

## Project Structure

```
personal-life-progress-tracker/
├── app.py                      ← Flask routes and app entry point
├── config.py                   ← Environment configuration
├── database.py                 ← All PostgreSQL queries
├── etl_weekly_summary.py       ← Weekly ETL pipeline
├── send_daily_reminder.py      ← Automated email reminder
├── requirements.txt
├── sql/
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   └── 03_create_views.sql
├── static/
│   ├── css/style.css           ← Full theme and animations
│   ├── js/main.js              ← Dashboard charts and interactivity
│   └── images/
└── templates/
    ├── index.html              ← Home page
    ├── lab_day.html            ← Lab day checklist
    ├── no_lab_day.html         ← No-lab day checklist
    ├── dashboard.html          ← Analytics dashboard
    └── weekly_report.html      ← Weekly ETL report
```

---

## Phase 2 Roadmap

- [ ] Power BI dashboard integration
- [ ] PostgreSQL star schema data warehouse
- [ ] Monthly reports and trend analysis
- [ ] Achievement badges and streak tracking
- [ ] Mobile responsive design
- [ ] WhatsApp notifications
- [ ] Personal KPI score
- [ ] Calendar integration

---

<div align="center">

*Built with purpose, for purpose.*

**Tshifhiwa Tshikosi** · Data Analyst, BI developer & Junior Data Engineer

[![GitHub](https://img.shields.io/badge/GitHub-Portfolio-9b59b6?style=flat-square&logo=github)](https://github.com/https://github.com/tshikositshifhiwa4-cmyk)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-74b9ff?style=flat-square&logo=linkedin)](https://linkedin.com/in/www.linkedin.com/in/TshifhiwaTshikosi)

</div>
