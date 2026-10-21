# -*- coding: utf-8 -*-
"""
Phase 4 Demo: Basic Algorithmic Problem Solving
Demonstrates:
1. Greedy Technique: Interval Scheduling (Activity Selection & Room Partitioning).
2. Dynamic Programming: Faculty Workload 0/1 Knapsack Optimizer & DP Table.
3. Backtracking Technique: Timetable Graph Coloring CSP Solver.
4. Integrated Pipeline Execution: End-to-end clash-free schedule creation.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase2"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase3"))

from greedy_scheduler import CourseSession, greedy_activity_selection, greedy_room_partitioning
from dp_workload import CourseModule, optimize_workload_dp, print_dp_table
from backtracking_timetable import TimetableBacktrackingSolver
from graph import ConflictGraph
from pipeline import TimetablePipeline
from data_models import Teacher, Course, Classroom, TimeSlot


def banner():
    print("\n" + "=" * 68)
    print("   +-------------------------------------------------------------+")
    print("   |   CLASH-FREE TIMETABLE GENERATOR                           |")
    print("   |   Phase 4 -- Basic Algorithmic Problem Solving              |")
    print("   +-------------------------------------------------------------+")
    print("=" * 68 + "\n")


def section(title: str):
    print("\n  +-------------------------------------------------------------+")
    print(f"  |  {title:<59}|")
    print("  +-------------------------------------------------------------+")


def demo_greedy():
    section("1. Greedy Technique: Interval Scheduling & Room Partitioning")

    # Sample candidate lab sessions in a day (minutes from midnight: 9:00 AM = 540)
    sessions = [
        CourseSession("S1", "DS Lab Batch A", 540, 630),     # 09:00 - 10:30
        CourseSession("S2", "OS Lab Batch B", 570, 690),     # 09:30 - 11:30
        CourseSession("S3", "Networks Lab", 630, 720),       # 10:30 - 12:00
        CourseSession("S4", "DBMS Practical", 660, 750),     # 11:00 - 12:30
        CourseSession("S5", "AI Project Viva", 720, 810),    # 12:00 - 13:30
        CourseSession("S6", "Web Tech Workshop", 780, 900),  # 13:00 - 15:00
    ]

    print("  Candidate Session Requests for Computer Lab 1:")
    for s in sessions:
        print(f"    {s}")

    # 1. Activity Selection (Single Room Max Sessions)
    selected = greedy_activity_selection(sessions)
    print(f"\n  >> A. Greedy Activity Selection (Max Sessions in Single Lab):")
    print(f"     Optimal Clash-Free Schedule ({len(selected)} sessions accommodated):")
    for s in selected:
        print(f"     * {s}")

    # 2. Interval Partitioning (Min Rooms needed for all sessions)
    room_allocs = greedy_room_partitioning(sessions)
    print(f"\n  >> B. Greedy Interval Partitioning (Minimum Labs Required for All):")
    print(f"     Minimum Laboratories Needed: {len(room_allocs)}")
    for room_name, r_sessions in room_allocs.items():
        print(f"     [{room_name}]:")
        for s in r_sessions:
            print(f"       - {s}")


def demo_dp():
    section("2. Dynamic Programming: 0/1 Knapsack Workload Optimizer")

    modules = [
        CourseModule("CS101", "Data Structures", 4, 45),
        CourseModule("CS102", "Operating Systems", 3, 35),
        CourseModule("CS103", "DBMS & SQL", 3, 30),
        CourseModule("CS104", "Computer Networks", 3, 28),
        CourseModule("CS105", "Machine Learning", 2, 25),
        CourseModule("CS106", "Advanced Algorithms", 4, 40),
    ]
    max_workload = 10  # Max weekly hours allowed for the faculty

    print(f"  Faculty Workload Budget Limit: {max_workload} hours/week")
    print("  Candidate Course Modules Available:")
    for m in modules:
        print(f"    {m}")

    max_credits, selected_mods, dp_table = optimize_workload_dp(modules, max_workload)

    print_dp_table(modules, dp_table, max_workload)

    print(f"  >> Optimal Selection Result:")
    print(f"     Max Total Credit Value Achieved: {max_credits} points")
    total_hrs = sum(m.hours for m in selected_mods)
    print(f"     Total Hours Allocated: {total_hrs} / {max_workload} hours")
    print(f"     Selected Modules:")
    for m in selected_mods:
        print(f"     * {m.code}: {m.title:<22} ({m.hours} hrs, {m.credit_value} pts)")


def demo_backtracking():
    section("3. Backtracking: Clash-Free Timetable Graph Coloring (CSP)")

    # Build conflict graph
    graph = ConflictGraph()
    courses = [
        (101, "Data Structures"),
        (102, "Operating Systems"),
        (103, "DBMS"),
        (104, "Computer Networks"),
        (105, "Machine Learning")
    ]
    for cid, name in courses:
        graph.add_vertex(cid, name)

    # Conflicts (Shared Teachers or Cohorts)
    graph.add_conflict(101, 102, "Shared Faculty (Dr. Sharma)")
    graph.add_conflict(101, 103, "Shared Class Cohort (Batch A)")
    graph.add_conflict(102, 104, "Shared Faculty (Prof. Kumar)")
    graph.add_conflict(103, 105, "Shared Class Cohort (Batch A)")
    graph.add_conflict(104, 105, "Shared Lab Resource")

    available_slots = ["Mon 09:00", "Mon 10:00", "Tue 09:00"]
    print(f"  Conflict Graph Courses: {len(courses)} courses")
    print(f"  Available TimeSlots (Colors): {available_slots}")

    solver = TimetableBacktrackingSolver(graph, available_slots)
    success = solver.solve()

    print(f"\n  >> Solver Status: {'SUCCESS (Clash-Free Schedule Found!)' if success else 'FAILED'}")
    print(f"     Backtracking Steps Taken: {solver.backtrack_steps}")
    print(f"     Successful State Transitions: {solver.successful_states}")

    schedule = solver.get_schedule()
    print("\n  >> Clash-Free Timetable Generated by Backtracking:")
    for slot, assigned in schedule.items():
        courses_str = ", ".join(f"{cid} ({name})" for cid, name in assigned) if assigned else "Empty"
        print(f"     [{slot}]: {courses_str}")


def demo_pipeline():
    section("4. Integrated Application Flow & Master Timetable")

    teachers = [
        Teacher(1, "Dr. Ananya Sharma", "Data Structures", 16),
        Teacher(2, "Prof. Ravi Kumar", "Operating Systems", 14),
        Teacher(3, "Ms. Priya Nair", "DBMS", 12),
        Teacher(4, "Mr. Arjun Mehta", "Computer Networks", 10),
        Teacher(5, "Dr. Sunita Rao", "Machine Learning", 18),
    ]
    courses = [
        Course(101, "Data Structures & Algo", "Dr. Ananya Sharma", 4),
        Course(102, "Operating Systems", "Prof. Ravi Kumar", 3),
        Course(103, "Database Management", "Ms. Priya Nair", 3),
        Course(104, "Computer Networks", "Mr. Arjun Mehta", 3),
        Course(105, "Introduction to ML", "Dr. Sunita Rao", 2),
    ]
    classrooms = [
        Classroom(201, "A-101", 60),
        Classroom(202, "B-202", 45),
        Classroom(203, "C-303", 30),
        Classroom(204, "Lab-1", 25),
    ]
    timeslots = [
        TimeSlot(301, "Monday", "09:00", "10:00"),
        TimeSlot(302, "Monday", "10:00", "11:00"),
        TimeSlot(303, "Tuesday", "09:00", "10:00"),
        TimeSlot(304, "Wednesday", "11:00", "12:00"),
        TimeSlot(305, "Thursday", "14:00", "15:00"),
    ]

    pipeline = TimetablePipeline(teachers, courses, classrooms, timeslots)
    results = pipeline.run_pipeline()

    print("\n  ==================== MASTER CLASH-FREE TIMETABLE ====================")
    print(f"  {'Course':<24} | {'Teacher':<18} | {'TimeSlot':<20} | {'Room':<8} | {'Status'}")
    print("  " + "-" * 82)
    for entry in results["final_schedule"]:
        status = "[CLASH-FREE]" if entry["is_clash_free"] else "[CLASH!]"
        print(f"  {entry['course_name']:<24} | {entry['teacher']:<18} | "
              f"{entry['timeslot']:<20} | {entry['classroom']:<8} | {status}")
    print("  =====================================================================")


def run_all_demos():
    banner()
    demo_greedy()
    demo_dp()
    demo_backtracking()
    demo_pipeline()
    print("\n  " + "=" * 68)
    print("  Phase 4 Demonstrations Completed Successfully!")
    print("  " + "=" * 68 + "\n")


if __name__ == "__main__":
    run_all_demos()
