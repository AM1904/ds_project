# -*- coding: utf-8 -*-
"""
Phase 2: Graph Traversals - BFS and DFS
1. Breadth-First Search (BFS): Level-order conflict exploration, connected components.
2. Depth-First Search (DFS): Deep conflict branch exploration, cycle detection.
"""
from typing import Dict, List, Set, Tuple
from collections import deque
from graph import ConflictGraph


def bfs_traversal(graph: ConflictGraph, start_vertex: int) -> Tuple[List[int], Dict[int, int]]:
    """
    Breadth-First Search (BFS) starting from a specific course node.
    Explores conflict neighbors level-by-level using a FIFO queue.
    Returns:
      - traversal_order: list of course IDs in BFS visit sequence.
      - levels: dict mapping course_id to distance/depth level from start.
    """
    if start_vertex not in graph.adj_list:
        return [], {}

    visited: Set[int] = set()
    queue = deque([start_vertex])
    visited.add(start_vertex)

    traversal_order: List[int] = []
    levels: Dict[int, int] = {start_vertex: 0}

    while queue:
        curr = queue.popleft()
        traversal_order.append(curr)

        for neighbor in sorted(graph.get_neighbors(curr)):
            if neighbor not in visited:
                visited.add(neighbor)
                levels[neighbor] = levels[curr] + 1
                queue.append(neighbor)

    return traversal_order, levels


def dfs_traversal(graph: ConflictGraph, start_vertex: int) -> List[int]:
    """
    Depth-First Search (DFS) starting from a specific course node.
    Explores conflict paths as deeply as possible before backtracking.
    Returns list of course IDs in DFS visit sequence.
    """
    if start_vertex not in graph.adj_list:
        return []

    visited: Set[int] = set()
    traversal_order: List[int] = []

    def _dfs(node: int):
        visited.add(node)
        traversal_order.append(node)
        for neighbor in sorted(graph.get_neighbors(node)):
            if neighbor not in visited:
                _dfs(neighbor)

    _dfs(start_vertex)
    return traversal_order


def find_connected_components(graph: ConflictGraph) -> List[List[int]]:
    """
    Discovers all independent connected components in the timetable graph.
    Significance: Independent components do NOT conflict with each other at all,
    meaning their timetables can be generated and solved completely in parallel!
    """
    visited: Set[int] = set()
    components: List[List[int]] = []

    for vertex in graph.get_vertices():
        if vertex not in visited:
            component_order, _ = bfs_traversal(graph, vertex)
            visited.update(component_order)
            components.append(component_order)

    return components


# Type alias helper
Tuple_List = tuple[List[int], Dict[int, int]]
