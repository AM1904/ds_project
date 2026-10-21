# -*- coding: utf-8 -*-
"""
Phase 4: Greedy Technique - Interval Scheduling & Activity Selection
Problem:
1. Maximum Non-Overlapping Course Sessions in a Shared Classroom (Activity Selection).
   Strategy: Earliest Finish Time (EFT) greedy choice property.
2. Minimum Classrooms Required (Interval Partitioning).
   Finds the minimal number of physical rooms needed so no two concurrent classes clash.
"""
from typing import List, Dict, Any


class CourseSession:
    """Represents a scheduled class session with start and end times in military 24-hr format (minutes)."""
    def __init__(self, session_id: str, course_name: str, start_time: int, end_time: int):
        self.session_id = session_id
        self.course_name = course_name
        self.start_time = start_time  # e.g., 540 = 09:00 AM
        self.end_time = end_time      # e.g., 600 = 10:00 AM

    @staticmethod
    def format_time(minutes: int) -> str:
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    def __str__(self):
        return (f"[{self.session_id}] {self.course_name:<20} "
                f"({self.format_time(self.start_time)} - {self.format_time(self.end_time)})")


def greedy_activity_selection(sessions: List[CourseSession]) -> List[CourseSession]:
    """
    Greedy Activity Selection:
    Selects the maximum possible number of mutually compatible course sessions
    that can take place in a single venue without clash.
    Greedy Choice: Pick the session that finishes earliest (EFT).
    Time Complexity: O(n log n) sorting + O(n) greedy scan.
    """
    if not sessions:
        return []

    # Sort sessions by finish time in ascending order
    sorted_sessions = sorted(sessions, key=lambda s: s.end_time)

    selected: List[CourseSession] = []
    # The first activity always belongs to an optimal solution
    selected.append(sorted_sessions[0])
    last_finish = sorted_sessions[0].end_time

    for curr in sorted_sessions[1:]:
        if curr.start_time >= last_finish:
            selected.append(curr)
            last_finish = curr.end_time

    return selected


def greedy_room_partitioning(sessions: List[CourseSession]) -> Dict[str, List[CourseSession]]:
    """
    Interval Partitioning / Greedy Room Allocator:
    Finds the minimum number of classrooms required to schedule ALL requested sessions
    without any time clashes.
    Strategy: Sort all sessions by start time. Greedily assign to an existing room if free;
              otherwise open a new classroom.
    """
    if not sessions:
        return {}

    sorted_sessions = sorted(sessions, key=lambda s: s.start_time)
    rooms: Dict[str, List[CourseSession]] = {}
    room_last_finish: Dict[str, int] = {}
    room_counter = 1

    for session in sorted_sessions:
        allocated = False
        # Try to fit into an existing room whose previous session finishes before this start
        for room_name, finish_time in room_last_finish.items():
            if session.start_time >= finish_time:
                rooms[room_name].append(session)
                room_last_finish[room_name] = session.end_time
                allocated = True
                break

        # If no room is free, open a new room
        if not allocated:
            new_room = f"Room-{room_counter}"
            room_counter += 1
            rooms[new_room] = [session]
            room_last_finish[new_room] = session.end_time

    return rooms
