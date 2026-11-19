# -*- coding: utf-8 -*-
"""
Phase 3 Demo: Searching and Sorting Operations
Demonstrates:
1. Linear Search vs Binary Search with comparison metrics.
2. Sorting Techniques: Insertion Sort, Merge Sort, and Quick Sort.
3. Conceptual Complexity Analysis & Empirical Benchmarks.
4. Timetable Project Workflow: Course Priority Sorting & Best-Fit Room Allocation.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))

from data_models import Course, Classroom, Teacher
from searching import linear_search, binary_search
from sorting import insertion_sort, merge_sort, quick_sort
from analysis import display_conceptual_comparison, run_empirical_benchmark
from workflow import prioritize_courses_by_hours, allocate_rooms_best_fit, suggest_best_fit_room, audit_teacher_allocation


def banner():
    print("\n" + "=" * 65)
    print("   +-------------------------------------------------------+")
    print("   |   CLASH-FREE TIMETABLE GENERATOR                     |")
    print("   |   Phase 3 -- Searching and Sorting Operations         |")
    print("   +-------------------------------------------------------+")
    print("=" * 65 + "\n")


def section(title: str):
    print("\n  +-------------------------------------------------------+")
    print(f"  |  {title:<53}|")
    print("  +-------------------------------------------------------+")


def demo_searching():
    section("1. Searching Operations: Linear vs Binary Search")
    course_ids = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
    target = 107

    print(f"  Target Course ID to locate: {target}")
    print(f"  Dataset: {course_ids}")

    # Linear Search
    idx_lin, item_lin, comps_lin = linear_search(course_ids, target)
    print(f"\n  >> Linear Search:")
    print(f"     Found at Index: {idx_lin} | Comparisons: {comps_lin} (O(n) sequential scan)")

    # Binary Search
    idx_bin, item_bin, comps_bin = binary_search(course_ids, target)
    print(f"\n  >> Binary Search:")
    print(f"     Found at Index: {idx_bin} | Comparisons: {comps_bin} (O(log n) halving search)")
    print(f"     Efficiency Gain: Binary Search needed only {comps_bin} comparisons vs {comps_lin} in Linear Search!")


def demo_sorting():
    section("2. Sorting Techniques Comparison")
    raw_courses = [
        Course(104, "Computer Networks", "Mr. Arjun Mehta", 3),
        Course(101, "Data Structures", "Dr. Ananya Sharma", 5),
        Course(105, "Machine Learning", "Dr. Sunita Rao", 2),
        Course(102, "Operating Systems", "Prof. Ravi Kumar", 4),
        Course(103, "DBMS", "Ms. Priya Nair", 1),
    ]

    print("  Original Unsorted Course List:")
    for c in raw_courses:
        print(f"    ID {c.course_id}: {c.name:<22} | Hrs/Week: {c.hours_per_week}")

    # Insertion Sort
    ins_res, ins_comps, ins_moves = insertion_sort(raw_courses, key_func=lambda c: c.hours_per_week)
    print(f"\n  >> 1. Insertion Sort (by hours_per_week ascending):")
    print(f"     Comparisons: {ins_comps} | Moves: {ins_moves}")
    for c in ins_res:
        print(f"       {c.name:<22} -> {c.hours_per_week} hrs")

    # Merge Sort
    mrg_res, mrg_comps, mrg_moves = merge_sort(raw_courses, key_func=lambda c: c.hours_per_week, reverse=True)
    print(f"\n  >> 2. Merge Sort (by hours_per_week descending - Scheduling Priority):")
    print(f"     Comparisons: {mrg_comps} | Moves: {mrg_moves}")
    for c in mrg_res:
        print(f"       {c.name:<22} -> {c.hours_per_week} hrs")

    # Quick Sort
    qck_res, qck_comps, qck_swaps = quick_sort(raw_courses, key_func=lambda c: c.course_id)
    print(f"\n  >> 3. Quick Sort (by course_id ascending):")
    print(f"     Comparisons: {qck_comps} | Swaps: {qck_swaps}")
    for c in qck_res:
        print(f"       ID {c.course_id}: {c.name:<22}")


def demo_workflow():
    section("3. Timetable Project Workflow Application")

    # Workflow 1: Priority Sorting
    courses = [
        Course(101, "Data Structures", "Dr. Ananya", 4),
        Course(102, "Operating Systems", "Prof. Ravi", 3),
        Course(103, "DBMS", "Ms. Priya", 2),
        Course(104, "Networks Lab", "Mr. Arjun", 1),
        Course(105, "Advanced AI", "Dr. Sunita", 5),
    ]
    prioritized = prioritize_courses_by_hours(courses)
    print("\n  >> Workflow A: Prioritize Heavy Courses First (Merge Sort):")
    for rank, c in enumerate(prioritized, 1):
        print(f"     Priority #{rank}: {c.name:<20} ({c.hours_per_week} hrs/week)")

    # Workflow 2: Best-Fit Room Allocation (Quick Sort + Binary Search)
    # Real campus classrooms (portal_data.db):
    classrooms = [
        Classroom(1, "Room A-101", 60),
        Classroom(2, "Room B-202", 45),
        Classroom(3, "Room C-303", 30),
        Classroom(4, "Systems Lab-1", 25),
    ]

    # Section Strengths: MCA A (42 students), MCA B (36 students)
    enrollments = [
        (Course(101, "MCA A: Data Structures", "Dr. Ananya Sharma", 4), 42),
        (Course(102, "MCA B: Operating Systems", "Prof. Ravi Kumar", 3), 36),
    ]

    print("\n  >> Workflow B: Best-Fit Classroom Allocation (Quick Sort + Binary Search):")
    sorted_rooms, allocations = allocate_rooms_best_fit(classrooms, enrollments)
    print("     Classrooms sorted in ascending order of capacity (Quick Sort):")
    print("     " + " -> ".join(f"{r.room_number} ({r.capacity} seats)" for r in sorted_rooms))

    print("\n     Binary Search Best-Fit Allocations (minimizing unused seats):")
    for alloc in allocations:
        c = alloc["course"]
        r = alloc["allocated_room"]
        print(f"     Course: {c.name:<25} | Strength: {alloc['students']} students -> "
              f"Suggested Room: {r.room_number} ({r.capacity} seats) | "
              f"Unused Seats: {alloc['waste_seats']} | Comparisons: {alloc['search_comparisons']}")

    # Dynamic Scenario: Room B-202 is booked at a timeslot (e.g. 09:00 AM)
    print("\n  >> Workflow B2: Dynamic Available Room Suggestion under Slot Conflict:")
    print("     Scenario: Room B-202 is already booked by MCA A at 09:00 AM - 10:00 AM.")
    available_rooms = [r for r in classrooms if r.room_number != "Room B-202"]
    print("     Available Rooms: " + ", ".join(f"{r.room_number} ({r.capacity} seats)" for r in available_rooms))

    # Suggest room for MCA B (36 students) among remaining available rooms
    alt_room, alt_waste, alt_comps = suggest_best_fit_room(available_rooms, 36)
    print(f"     MCA B (36 students) Suggestion among available:")
    print(f"     -> Suggested: {alt_room.room_number} ({alt_room.capacity} seats) | "
          f"Unused Seats: {alt_waste} | Comparisons: {alt_comps} (Binary Search)")


def demo_analysis():
    section("4. Conceptual & Empirical Complexity Analysis")
    display_conceptual_comparison()
    print("\n  Running empirical benchmarking across dataset sizes [10, 50, 100, 250]:")
    run_empirical_benchmark([10, 50, 100, 250])


def run_all_demos():
    banner()
    demo_searching()
    demo_sorting()
    demo_workflow()
    demo_analysis()
    print("\n  " + "=" * 65)
    print("  Phase 3 Demonstrations Completed Successfully!")
    print("  " + "=" * 65 + "\n")


if __name__ == "__main__":
    run_all_demos()
