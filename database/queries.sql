-- ====================================================================
-- HANDY ANALYTICAL QUERIES FOR MYSQL WORKBENCH
-- Execute these queries in MySQL Workbench query tab!
-- ====================================================================

USE timetable_db;

-- 1. View Complete Generated Timetable with all details
SELECT * FROM v_clash_free_timetable;

-- 2. Verify Clash-Free Status (Must return 0 rows for 100% clash-free!)
-- Checks if any teacher is scheduled in two different rooms at the same time slot:
SELECT 
    ta1.assignment_id AS assign_1,
    ta2.assignment_id AS assign_2,
    t.name AS teacher_name,
    ts.day,
    CONCAT(ts.start_time, ' - ', ts.end_time) AS slot,
    c1.name AS course_1,
    c2.name AS course_2
FROM timetable_assignments ta1
JOIN timetable_assignments ta2 
    ON ta1.teacher_id = ta2.teacher_id 
    AND ta1.slot_id = ta2.slot_id 
    AND ta1.assignment_id < ta2.assignment_id
JOIN teachers t ON ta1.teacher_id = t.teacher_id
JOIN timeslots ts ON ta1.slot_id = ts.slot_id
JOIN courses c1 ON ta1.course_id = c1.course_id
JOIN courses c2 ON ta2.course_id = c2.course_id;

-- 3. Room Double-Booking Check (Must return 0 rows for 100% clash-free!)
SELECT 
    ta1.assignment_id AS assign_1,
    ta2.assignment_id AS assign_2,
    cr.room_number,
    ts.day,
    ts.start_time,
    c1.name AS course_1,
    c2.name AS course_2
FROM timetable_assignments ta1
JOIN timetable_assignments ta2 
    ON ta1.room_id = ta2.room_id 
    AND ta1.slot_id = ta2.slot_id 
    AND ta1.assignment_id < ta2.assignment_id
JOIN classrooms cr ON ta1.room_id = cr.room_id
JOIN timeslots ts ON ta1.slot_id = ts.slot_id
JOIN courses c1 ON ta1.course_id = c1.course_id
JOIN courses c2 ON ta2.course_id = c2.course_id;

-- 4. Audit Teacher Assigned Hours vs Workload Limits
SELECT * FROM v_teacher_workload;

-- 5. Inspect Graph Conflict Edges stored in Database
SELECT 
    cf.conflict_id,
    c1.name AS course_a,
    c2.name AS course_b,
    cf.reason
FROM course_conflicts cf
JOIN courses c1 ON cf.course_id_1 = c1.course_id
JOIN courses c2 ON cf.course_id_2 = c2.course_id;
