-- Table for employees
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    position TEXT,
    salary INTEGER DEFAULT 0,
    role TEXT DEFAULT 'staff'
);

-- Table for salary reports
CREATE TABLE IF NOT EXISTS salary_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    total_salary REAL NOT NULL,
    report_date TEXT NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);

CREATE TABLE IF NOT EXISTS shifts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    shift_date TEXT NOT NULL, -- Format: YYYY-MM-DD
    shift_type TEXT NOT NULL, -- Examples: 'A', 'B', 'C', 'AB', 'BC'
    note TEXT,                -- Optional: for special remarks like x2, A/2, etc.
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS shift_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    shift TEXT NOT NULL,
    employee_id INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    phone TEXT,
    date TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT, -- Nullable for flexible durations
    number_of_people INT NOT NULL,
    room_type TEXT NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

