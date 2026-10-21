-- ====================================================================
-- SEED DATA FOR TIMETABLE GENERATOR
-- Execute in MySQL Workbench after schema.sql
-- ====================================================================

USE timetable_db;

-- Clear previous data
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE timetable_assignments;
TRUNCATE TABLE course_conflicts;
TRUNCATE TABLE courses;
TRUNCATE TABLE classrooms;
TRUNCATE TABLE timeslots;
TRUNCATE TABLE teachers;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. Insert Teachers
INSERT INTO teachers (teacher_id, name, subject, max_hours) VALUES
(1, 'Dr. Ananya Sharma', 'Data Structures', 16),
(2, 'Prof. Ravi Kumar', 'Operating Systems', 14),
(3, 'Ms. Priya Nair', 'DBMS', 12),
(4, 'Mr. Arjun Mehta', 'Computer Networks', 10),
(5, 'Dr. Sunita Rao', 'Machine Learning', 18);

-- 2. Insert Classrooms
INSERT INTO classrooms (room_id, room_number, capacity) VALUES
(201, 'A-101', 60),
(202, 'B-202', 45),
(203, 'C-303', 30),
(204, 'Lab-1', 25);

-- 3. Insert TimeSlots
INSERT INTO timeslots (slot_id, day, start_time, end_time) VALUES
(301, 'Monday', '09:00', '10:00'),
(302, 'Monday', '10:00', '11:00'),
(303, 'Tuesday', '09:00', '10:00'),
(304, 'Wednesday', '11:00', '12:00'),
(305, 'Thursday', '14:00', '15:00'),
(306, 'Friday', '13:00', '14:00');

-- 4. Insert Courses
INSERT INTO courses (course_id, name, teacher_id, hours_per_week) VALUES
(101, 'Data Structures & Algo', 1, 4),
(102, 'Operating Systems', 2, 3),
(103, 'Database Management', 3, 3),
(104, 'Computer Networks', 4, 3),
(105, 'Introduction to ML', 5, 2);

-- 5. Insert Course Conflicts (Graph Edges)
INSERT INTO course_conflicts (course_id_1, course_id_2, reason) VALUES
(101, 102, 'Shared Year 2 Cohort Section A'),
(101, 103, 'Shared Core CS Curriculum'),
(102, 104, 'Shared Lab Facility (Systems Lab)'),
(103, 105, 'Shared Elective Batch');

-- 6. Insert Initial Master Clash-Free Schedule (Algorithmic Output)
INSERT INTO timetable_assignments (course_id, teacher_id, room_id, slot_id, is_clash_free) VALUES
(101, 1, 201, 301, TRUE),
(102, 2, 202, 302, TRUE),
(103, 3, 204, 301, TRUE),
(104, 4, 203, 301, TRUE),
(105, 5, 204, 303, TRUE);
