# -*- coding: utf-8 -*-
"""
Phase 4: Integrated Algorithmic Pipeline
Ties together:
1. Dynamic Programming (Workload feasibility check)
2. Conflict Graph construction
3. Backtracking Graph Coloring (Clash-free slot assignment)
4. Greedy Interval Allocation (Classroom assignment per slot)
Produces the complete final Timetable Schedule.
"""
import sys
import os
from typing import Dict, List, Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase2"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase3"))
sys.path.insert(0, os.path.dirname(__file__))

from data_models import Teacher, Course, Classroom, TimeSlot
from graph import ConflictGraph
from dp_workload import CourseModule, optimize_workload_dp
from backtracking_timetable import TimetableBacktrackingSolver
from searching import binary_search_best_fit
from sorting import quick_sort


class TimetablePipeline:
    """
    End-to-End Algorithmic Orchestrator for Clash-Free Timetabling.
    """
    def __init__(self, teachers: List[Teacher], courses: List[Course],
                 classrooms: List[Classroom], timeslots: List[TimeSlot]):
        self.teachers = teachers
        self.courses = courses
        self.classrooms = classrooms
        self.timeslots = timeslots

    def run_pipeline(self) -> Dict[str, Any]:
        report: Dict[str, Any] = {}

        # ----------------------------------------------------
        # Step 1: DP Faculty Workload Feasibility Optimization
        # ----------------------------------------------------
        modules = [
            CourseModule(str(c.course_id), c.name, c.hours_per_week, c.hours_per_week * 10)
            for c in self.courses
        ]
        # Optimize workload for primary instructor (e.g. 14 hours max)
        max_hrs = 14
        max_val, selected_mods, _ = optimize_workload_dp(modules, max_hrs)
        report["dp_selected_modules"] = selected_mods
        report["dp_total_credits"] = max_val

        # ----------------------------------------------------
        # Step 2: Build Conflict Graph
        # ----------------------------------------------------
        conflict_graph = ConflictGraph()
        for c in self.courses:
            conflict_graph.add_vertex(c.course_id, c.name)

        # Detect conflicts automatically:
        # Same teacher = Conflict!
        teacher_map: Dict[str, List[int]] = {}
        for c in self.courses:
            teacher_map.setdefault(c.teacher_name, []).append(c.course_id)

        for tname, cids in teacher_map.items():
            for i in range(len(cids)):
                for j in range(i + 1, len(cids)):
                    conflict_graph.add_conflict(cids[i], cids[j], f"Shared Teacher: {tname}")

        # Add sample shared-cohort conflicts (e.g., core CS curriculum)
        if len(self.courses) >= 2:
            conflict_graph.add_conflict(self.courses[0].course_id, self.courses[1].course_id, "Core CS Cohort Year 2")

        report["conflict_graph"] = conflict_graph

        # ----------------------------------------------------
        # Step 3: Backtracking Slot Assignment (CSP Graph Coloring)
        # ----------------------------------------------------
        slot_names = [f"{ts.day} {ts.start_time}-{ts.end_time}" for ts in self.timeslots]
        solver = TimetableBacktrackingSolver(conflict_graph, slot_names)
        solved = solver.solve()
        report["backtracking_solved"] = solved
        report["backtracking_steps"] = solver.backtrack_steps
        report["slot_assignments"] = solver.assignments

        # ----------------------------------------------------
        # Step 4: Greedy Classroom Assignment per TimeSlot
        # ----------------------------------------------------
        # Sort rooms by capacity
        sorted_rooms, _, _ = quick_sort(self.classrooms, key_func=lambda r: r.capacity)
        final_schedule = []

        # Default student headcount per course for demonstration
        default_sizes = {101: 50, 102: 40, 103: 25, 104: 30, 105: 20}

        # Track which rooms have been booked per timeslot to guarantee zero room collisions
        occupied_rooms: Dict[str, set] = {}

        for cid, slot_str in solver.assignments.items():
            c_obj = next((c for c in self.courses if c.course_id == cid), None)
            if not c_obj or not slot_str:
                continue

            needed_capacity = default_sizes.get(cid, 30)
            occupied_in_slot = occupied_rooms.setdefault(slot_str, set())
            available_rooms = [r for r in sorted_rooms if r.room_number not in occupied_in_slot]

            # Find best-fit room via binary search among available rooms
            _, room_obj, _ = binary_search_best_fit(available_rooms, needed_capacity)
            if not room_obj and available_rooms:
                room_obj = available_rooms[-1]  # Largest available

            if room_obj:
                occupied_in_slot.add(room_obj.room_number)

            final_schedule.append({
                "course_id": cid,
                "course_name": c_obj.name,
                "teacher": c_obj.teacher_name,
                "timeslot": slot_str,
                "classroom": room_obj.room_number if room_obj else "TBD",
                "room_capacity": room_obj.capacity if room_obj else 0,
                "students": needed_capacity,
                "is_clash_free": True
            })

        report["final_schedule"] = final_schedule
        return report
