# -*- coding: utf-8 -*-
"""
Phase 3: Searching Operations
1. Linear Search: O(n) scan, works on unsorted collections.
2. Binary Search: O(log n) divide-and-conquer search on sorted collections.
3. Best-Fit Binary Search: O(log n) search for optimal capacity match (e.g. Classrooms).
"""
from typing import Any, Callable, List, Optional, Tuple


def linear_search(
    items: List[Any],
    target_val: Any,
    key_func: Callable[[Any], Any] = lambda x: x
) -> Tuple[int, Optional[Any], int]:
    """
    Performs Linear Search across items.
    Returns: (index, found_item, comparison_count)
    If not found, returns (-1, None, comparison_count).
    Time Complexity: O(n) worst/average, O(1) best.
    """
    comparisons = 0
    for idx, item in enumerate(items):
        comparisons += 1
        if key_func(item) == target_val:
            return idx, item, comparisons
    return -1, None, comparisons


def binary_search(
    sorted_items: List[Any],
    target_val: Any,
    key_func: Callable[[Any], Any] = lambda x: x
) -> Tuple[int, Optional[Any], int]:
    """
    Performs Binary Search across sorted items.
    Returns: (index, found_item, comparison_count)
    If not found, returns (-1, None, comparison_count).
    Time Complexity: O(log n) worst/average, O(1) best.
    Requires list to be sorted by key_func in ascending order.
    """
    low = 0
    high = len(sorted_items) - 1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        mid_val = key_func(sorted_items[mid])

        if mid_val == target_val:
            return mid, sorted_items[mid], comparisons
        elif mid_val < target_val:
            low = mid + 1
        else:
            high = mid - 1

    return -1, None, comparisons


def binary_search_best_fit(
    sorted_rooms: List[Any],
    required_capacity: int,
    capacity_func: Callable[[Any], int] = lambda r: r.capacity
) -> Tuple[int, Optional[Any], int]:
    """
    Finds the optimal classroom (smallest room whose capacity >= required_capacity).
    Prevents classroom waste by avoiding allocating a 100-seat auditorium to a 20-student elective.
    Returns: (index, room, comparison_count)
    """
    low = 0
    high = len(sorted_rooms) - 1
    best_idx = -1
    comparisons = 0

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        mid_cap = capacity_func(sorted_rooms[mid])

        if mid_cap >= required_capacity:
            best_idx = mid
            high = mid - 1  # Look for a smaller fitting room on the left
        else:
            low = mid + 1   # Room too small, look right

    if best_idx != -1:
        return best_idx, sorted_rooms[best_idx], comparisons
    return -1, None, comparisons
