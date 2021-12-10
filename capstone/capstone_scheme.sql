-- Scheme
CREATE TABLE IF NOT EXISTS "Users" (
    "user_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "first_name" TEXT NOT NULL,
    "last_name" TEXT NOT NULL,
    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT DEFAULT '1234',
    "active" INTEGER DEFAULT 1,
    "date_created" TEXT,
    "hire_date" TEXT,
    "user_type" TEXT DEFAULT "user"
);

CREATE TABLE IF NOT EXISTS "Competencies" (
    "comp_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "date_created" TEXT
);

CREATE TABLE IF NOT EXISTS "Assessments"(
    "assessment_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "name" TEXT NOT NULL,
    "date_created" TEXT
);

CREATE TABLE IF NOT EXISTS "Assessments_results" (
    "result_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER,
    "comp_id" INTEGER,
    "assessment_id" INTEGER,
    "score" INTEGER DEFAULT 0,
    "date_taken" TEXT,
    "manager" TEXT,
    FOREIGN KEY ("user_id")
        REFERENCES "USERS" ("user_id"),
    FOREIGN KEY ("comp_id")
        REFERENCES "Competencies" ("comp_id"),
    FOREIGN KEY ("assessment_id")
        REFERENCES "Assessments" ("assessment_id")

);
