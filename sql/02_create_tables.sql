-- 02_create_tables.sql
-- Personal Productivity Database

-- Daily check-ins 
CREATE TABLE IF NOT EXISTS daily_checkins (
    checkin_id                  SERIAL PRIMARY KEY,
    checkin_date                DATE        NOT NULL UNIQUE,
    day_type                    VARCHAR(10) NOT NULL CHECK (day_type IN ('lab', 'no_lab')),
    day_of_week                 VARCHAR(10),
    is_lab_day                  BOOLEAN     DEFAULT FALSE,
    church_required             BOOLEAN     DEFAULT FALSE,

    -- Checkbox fields
    lab_completed               SMALLINT    DEFAULT 0,
    class_completed             SMALLINT    DEFAULT 0,
    job_applications_completed  SMALLINT    DEFAULT 0,
    msc_completed               SMALLINT    DEFAULT 0,
    portfolio_completed         SMALLINT    DEFAULT 0,
    household_completed         SMALLINT    DEFAULT 0,
    selfcare_completed          SMALLINT    DEFAULT 0,
    rest_completed              SMALLINT    DEFAULT 0,
    church_completed            SMALLINT    DEFAULT 0,

    -- Text reflections
    main_achievement            TEXT,
    tomorrow_major_task         TEXT,
    mood                        VARCHAR(30),
    notes                       TEXT,

    -- Numeric
    job_applications_count      INTEGER     DEFAULT 0,

    created_at                  TIMESTAMP   DEFAULT CURRENT_TIMESTAMP
);

-- Weekly ETL summary
CREATE TABLE IF NOT EXISTS weekly_summary (
    summary_id              SERIAL PRIMARY KEY,
    week_start_date         DATE        NOT NULL,
    week_end_date           DATE        NOT NULL,

    total_tasks_completed   INTEGER     DEFAULT 0,
    total_possible_tasks    INTEGER     DEFAULT 0,
    completion_percentage   NUMERIC(5,2) DEFAULT 0,
    total_job_applications  INTEGER     DEFAULT 0,

    msc_days                INTEGER     DEFAULT 0,
    lab_days                INTEGER     DEFAULT 0,
    class_days              INTEGER     DEFAULT 0,
    church_days             INTEGER     DEFAULT 0,
    selfcare_days           INTEGER     DEFAULT 0,
    rest_days               INTEGER     DEFAULT 0,

    best_category           VARCHAR(50),
    area_needing_attention  VARCHAR(50),
    weekly_insight          TEXT,

    created_at              TIMESTAMP   DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (week_start_date, week_end_date)
);
