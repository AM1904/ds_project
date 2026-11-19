# -*- coding: utf-8 -*-
"""
Phase 3: Domain Workflow Integration
Applies Sorting and Searching within the Timetable Scheduling Workflow:
1. Sort Courses by Weekly Hours (Priority Scheduling via Merge Sort).
2. Sort Classrooms by Capacity (via Quick Sort) + Optimal Room Allocation (via Binary Search Best-Fit).
3. Search and Audit Teacher Workload Allocation.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))

from data_models import Course, Classroom, Teacher
from sorting import merge_sort, quick_sort, insertion_sort
from searching import binary_search, linear_search, binary_search_best_fit


def prioritize_courses_by_hours(courses: list[Course]) -> list[Course]:
    """
    Sorts courses descending by hours_per_week using Merge Sort.
    Rationale: In scheduling algorithms (Greedy & Backtracking), allocating
    the most resource-intensive courses first drastically reduces dead-ends and clashes!
    """
    sorted_courses, comparisons, _ = merge_sort(courses, key_func=lambda c: c.hours_per_week, reverse=True)
    return sorted_courses


def allocate_rooms_best_fit(classrooms: list[Classroom], course_enrollments: list[tuple[Course, int]]):
    """
    1. Sorts classrooms in ascending order of capacity using Quick Sort.
    2. For each course and student count, uses Binary Search Best-Fit to find
       the minimal adequate room without wasting seats.
    """
    sorted_rooms, _, _ = quick_sort(classrooms, key_func=lambda r: r.capacity)
    allocations = []

    for course, students in course_enrollments:
        idx, room, comps = binary_search_best_fit(sorted_rooms, students, capacity_func=lambda r: r.capacity)
        allocations.append({
            "course": course,
            "students": students,
            "allocated_room": room,
            "waste_seats": (room.capacity - students) if room else None,
            "search_comparisons": comps
        })
    return sorted_rooms, allocations


def suggest_best_fit_room(available_rooms: list[Classroom], student_count: int):
    """
    Given currently available (unbooked) classrooms:
    1. Sorts classrooms in ascending order of seating capacity via Quick Sort.
    2. Identifies the smallest classroom accommodating student_count via Binary Search.
    Minimizes unused seating capacity.
    """
    if not available_rooms:
        return None, None, 0
    sorted_rooms, _, _ = quick_sort(available_rooms, key_func=lambda r: r.capacity)
    idx, room, comps = binary_search_best_fit(sorted_rooms, student_count, capacity_func=lambda r: r.capacity)
    waste = (room.capacity - student_count) if room else None
    return room, waste, comps


def audit_teacher_allocation(teachers: list[Teacher], target_subject: str):
    """
    Uses Linear Search to locate teachers by specialized subject.
    """
    idx, teacher, comps = linear_search(teachers, target_subject, key_func=lambda t: t.subject)
    return teacher, comps
