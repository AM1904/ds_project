# -*- coding: utf-8 -*-
"""
Phase 4: Backtracking Technique - Clash-Free Timetable Graph Coloring (CSP)
Formulates timetable generation as a Graph Coloring Constraint Satisfaction Problem:
- Vertices: Courses
- Edges: Conflicts (Shared Teacher or Student Batch)
- Colors: Available TimeSlots (1 .. K)
Constraint: Adjacent conflicting courses cannot be assigned the same time slot!
Uses Recursive Backtracking with state rollback.
"""
import sys
import os
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase2"))
from graph import ConflictGraph


class TimetableBacktrackingSolver:
    """
    Backtracking Constraint Satisfaction Solver for Timetable Scheduling.
    """
    def __init__(self, graph: ConflictGraph, available_slots: List[str]):
        self.graph = graph
        self.available_slots = available_slots
        self.course_list = graph.get_vertices()
        # Assignment state: { course_id: slot_name }
        self.assignments: Dict[int, Optional[str]] = {cid: None for cid in self.course_list}
        self.backtrack_steps = 0
        self.successful_states = 0

    def is_safe(self, course_id: int, candidate_slot: str) -> bool:
        """
        Safety check: Ensures no neighbor (conflicting course) has already
        been assigned the same candidate time slot.
        """
        for neighbor in self.graph.get_neighbors(course_id):
            if self.assignments.get(neighbor) == candidate_slot:
                return False  # Clash detected!
        return True

    def solve(self) -> bool:
        """Public entry point for backtracking solver."""
        self.backtrack_steps = 0
        self.successful_states = 0
        # Sort courses by degree descending (Most Constrained First heuristic)
        # This speeds up backtracking dramatically!
        sorted_courses = sorted(self.course_list, key=lambda c: self.graph.get_degree(c), reverse=True)
        return self._backtrack(0, sorted_courses)

    def _backtrack(self, index: int, courses: List[int]) -> bool:
        # Base Case: All courses have been successfully assigned a clash-free slot!
        if index == len(courses):
            return True

        current_course = courses[index]

        for slot in self.available_slots:
            if self.is_safe(current_course, slot):
                # Tentatively assign slot
                self.assignments[current_course] = slot
                self.successful_states += 1

                # Recurse to assign the next course
                if self._backtrack(index + 1, courses):
                    return True

                # If assigning this slot led to a dead-end, BACKTRACK (rollback state)
                self.assignments[current_course] = None
                self.backtrack_steps += 1

        return False

    def get_schedule(self) -> Dict[str, List[Tuple[int, str]]]:
        """Groups assigned courses by their assigned time slot."""
        schedule_by_slot: Dict[str, List[Tuple[int, str]]] = {s: [] for s in self.available_slots}
        for cid, slot in self.assignments.items():
            if slot:
                cname = self.graph.vertex_names.get(cid, f"Course {cid}")
                schedule_by_slot[slot].append((cid, cname))
        return schedule_by_slot
