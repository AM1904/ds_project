-- ====================================================================
-- CLASH-FREE TIMETABLE GENERATOR DATABASE SCHEMA
-- Compatible with MySQL 8.0+ and MySQL Workbench
-- ====================================================================

CREATE DATABASE IF NOT EXISTS timetable_db;
USE timetable_db;

-- 1. Teachers Table
CREATE TABLE IF NOT EXISTS teachers (
    teacher_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    max_hours INT NOT NULL DEFAULT 16,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Classrooms Table
CREATE TABLE IF NOT EXISTS classrooms (
    room_id INT PRIMARY KEY,
    room_number VARCHAR(50) NOT NULL UNIQUE,
    capacity INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. TimeSlots Table
CREATE TABLE IF NOT EXISTS timeslots (
    slot_id INT PRIMARY KEY,
    day VARCHAR(20) NOT NULL,
    start_time VARCHAR(10) NOT NULL,
    end_time VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Courses Table
CREATE TABLE IF NOT EXISTS courses (
    course_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    teacher_id INT NOT NULL,
    hours_per_week INT NOT NULL DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_courses_teacher FOREIGN KEY (teacher_id) 
        REFERENCES teachers(teacher_id) ON DELETE CASCADE
);

-- 5. Course Conflicts Table (Represents edges in the Graph Structure)
CREATE TABLE IF NOT EXISTS course_conflicts (
    conflict_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id_1 INT NOT NULL,
    course_id_2 INT NOT NULL,
    reason VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_conflict_c1 FOREIGN KEY (course_id_1) REFERENCES courses(course_id) ON DELETE CASCADE,
    CONSTRAINT fk_conflict_c2 FOREIGN KEY (course_id_2) REFERENCES courses(course_id) ON DELETE CASCADE,
    CONSTRAINT uq_course_conflict UNIQUE (course_id_1, course_id_2)
);

-- 6. Timetable Assignments Table (Output of Algorithmic Pipeline)
CREATE TABLE IF NOT EXISTS timetable_assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    teacher_id INT NOT NULL,
    room_id INT NOT NULL,
    slot_id INT NOT NULL,
    is_clash_free BOOLEAN DEFAULT TRUE,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_assign_course FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    CONSTRAINT fk_assign_teacher FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE,
    CONSTRAINT fk_assign_room FOREIGN KEY (room_id) REFERENCES classrooms(room_id) ON DELETE CASCADE,
    CONSTRAINT fk_assign_slot FOREIGN KEY (slot_id) REFERENCES timeslots(slot_id) ON DELETE CASCADE
);

-- View: Complete Clash-Free Master Timetable
CREATE OR REPLACE VIEW v_clash_free_timetable AS
SELECT 
    ta.assignment_id,
    c.name AS course_name,
    t.name AS teacher_name,
    cr.room_number,
    cr.capacity AS room_capacity,
    ts.day,
    CONCAT(ts.start_time, ' - ', ts.end_time) AS time_window,
    ta.is_clash_free
FROM timetable_assignments ta
JOIN courses c ON ta.course_id = c.course_id
JOIN teachers t ON ta.teacher_id = t.teacher_id
JOIN classrooms cr ON ta.room_id = cr.room_id
JOIN timeslots ts ON ta.slot_id = ts.slot_id
ORDER BY ts.slot_id, cr.room_number;

-- View: Teacher Workload Audit
CREATE OR REPLACE VIEW v_teacher_workload AS
SELECT 
    t.teacher_id,
    t.name AS teacher_name,
    t.max_hours,
    COALESCE(SUM(c.hours_per_week), 0) AS assigned_hours,
    (t.max_hours - COALESCE(SUM(c.hours_per_week), 0)) AS remaining_capacity
FROM teachers t
LEFT JOIN courses c ON t.teacher_id = c.teacher_id
GROUP BY t.teacher_id, t.name, t.max_hours;
