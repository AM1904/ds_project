# -*- coding: utf-8 -*-
"""
Phase 2: Graph Structures - Conflict & Relationship Graph
Represents timetable course conflicts using both:
1. Adjacency List representation
2. Adjacency Matrix representation
"""
from typing import Dict, List, Set, Tuple, Optional


class ConflictGraph:
    """
    Timetable Conflict Graph.
    - Vertices: Courses / Sections.
    - Edges: Conflicts (Courses that share a teacher, room, or student batch
             and cannot be held at the same timeslot).
    """
    def __init__(self):
        # Adjacency List: { course_id: set of conflicting course_ids }
        self.adj_list: Dict[int, Set[int]] = {}
        # Course metadata cache: { course_id: course_name }
        self.vertex_names: Dict[int, str] = {}
        # Edge reasons: { (u, v): reason_string }
        self.edge_reasons: Dict[Tuple[int, int], str] = {}

    def add_vertex(self, course_id: int, course_name: str = "") -> None:
        """Add a course vertex to the graph."""
        if course_id not in self.adj_list:
            self.adj_list[course_id] = set()
            self.vertex_names[course_id] = course_name or f"Course-{course_id}"

    def add_conflict(self, course_a: int, course_b: int, reason: str = "Shared Resource") -> None:
        """Add an undirected edge representing a scheduling conflict between two courses."""
        if course_a not in self.adj_list:
            self.add_vertex(course_a)
        if course_b not in self.adj_list:
            self.add_vertex(course_b)

        self.adj_list[course_a].add(course_b)
        self.adj_list[course_b].add(course_a)

        edge_key = (min(course_a, course_b), max(course_a, course_b))
        self.edge_reasons[edge_key] = reason

    def get_vertices(self) -> List[int]:
        """Return sorted list of all vertex IDs."""
        return sorted(list(self.adj_list.keys()))

    def get_neighbors(self, course_id: int) -> Set[int]:
        """Return the set of conflicting neighbor courses."""
        return self.adj_list.get(course_id, set())

    def get_degree(self, course_id: int) -> int:
        """Return the conflict degree (number of conflicts) for a course."""
        return len(self.adj_list.get(course_id, set()))

    def display_adjacency_list(self) -> None:
        """Prints the Adjacency List representation."""
        print("\n  ================ ADJACENCY LIST REPRESENTATION ================")
        for course_id in sorted(self.adj_list.keys()):
            name = self.vertex_names.get(course_id, f"ID {course_id}")
            neighbors = sorted(list(self.adj_list[course_id]))
            neighbor_str = ", ".join(
                f"{nid} ({self.vertex_names.get(nid, '')})" for nid in neighbors
            ) if neighbors else "None (Independent)"
            print(f"  [Course {course_id:>3}] {name:<24} --> [{neighbor_str}]")
        print("  " + "=" * 63)

    def get_adjacency_matrix(self) -> Tuple[List[int], List[List[int]]]:
        """
        Builds the 2D Adjacency Matrix representation.
        Returns (vertex_ids, matrix).
        """
        vertices = sorted(list(self.adj_list.keys()))
        n = len(vertices)
        idx_map = {vid: i for i, vid in enumerate(vertices)}
        matrix = [[0] * n for _ in range(n)]

        for u in vertices:
            for v in self.adj_list[u]:
                matrix[idx_map[u]][idx_map[v]] = 1

        return vertices, matrix

    def display_adjacency_matrix(self) -> None:
        """Prints the Adjacency Matrix representation."""
        vertices, matrix = self.get_adjacency_matrix()
        print("\n  =============== ADJACENCY MATRIX REPRESENTATION ===============")
        header = "       " + " ".join(f"{v:>5}" for v in vertices)
        print(f"  {header}")
        print("  " + " " * 5 + "+" + "-----" * len(vertices) + "-+")

        for i, u in enumerate(vertices):
            row_str = " ".join(f"{matrix[i][j]:>5}" for j in range(len(vertices)))
            print(f"  {u:>5} | {row_str} |")
        print("  " + " " * 5 + "+" + "-----" * len(vertices) + "-+")
        print("  (1 = Conflict/Edge exists, 0 = No Conflict)")
        print("  " + "=" * 63)
