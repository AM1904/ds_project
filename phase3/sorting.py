# -*- coding: utf-8 -*-
"""
Phase 3: Sorting Operations
Implements 3 fundamental sorting algorithms:
1. Insertion Sort: O(n^2), in-place, adaptive, stable.
2. Merge Sort: O(n log n), divide-and-conquer, stable.
3. Quick Sort: O(n log n) average, divide-and-conquer, in-place.
All functions accept a key_func extractor and return (sorted_list, comparisons, swaps_or_moves).
"""
from typing import Any, Callable, List, Tuple


def insertion_sort(
    items: List[Any],
    key_func: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> Tuple[List[Any], int, int]:
    """
    Insertion Sort:
    Builds the sorted array one element at a time by shifting elements.
    Best: O(n) nearly sorted, Worst/Avg: O(n^2). Stable.
    """
    arr = list(items)
    n = len(arr)
    comparisons = 0
    moves = 0

    for i in range(1, n):
        key_item = arr[i]
        key_val = key_func(key_item)
        j = i - 1

        while j >= 0:
            comparisons += 1
            curr_val = key_func(arr[j])
            should_move = (curr_val < key_val) if reverse else (curr_val > key_val)

            if should_move:
                arr[j + 1] = arr[j]
                moves += 1
                j -= 1
            else:
                break

        arr[j + 1] = key_item
        moves += 1

    return arr, comparisons, moves


def merge_sort(
    items: List[Any],
    key_func: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> Tuple[List[Any], int, int]:
    """
    Merge Sort:
    Divide-and-conquer algorithm. Guaranteed O(n log n) in all cases.
    Stable.
    """
    arr = list(items)
    comparisons = 0
    moves = 0

    def _merge_sort_helper(sub: List[Any]) -> List[Any]:
        nonlocal comparisons, moves
        if len(sub) <= 1:
            return sub

        mid = len(sub) // 2
        left = _merge_sort_helper(sub[:mid])
        right = _merge_sort_helper(sub[mid:])

        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            comparisons += 1
            l_val = key_func(left[i])
            r_val = key_func(right[j])

            take_left = (l_val >= r_val) if reverse else (l_val <= r_val)
            if take_left:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
            moves += 1

        while i < len(left):
            merged.append(left[i])
            i += 1
            moves += 1

        while j < len(right):
            merged.append(right[j])
            j += 1
            moves += 1

        return merged

    sorted_arr = _merge_sort_helper(arr)
    return sorted_arr, comparisons, moves


def quick_sort(
    items: List[Any],
    key_func: Callable[[Any], Any] = lambda x: x,
    reverse: bool = False
) -> Tuple[List[Any], int, int]:
    """
    Quick Sort:
    Divide-and-conquer partitioning around a pivot.
    Average: O(n log n), Worst: O(n^2). In-place / memory efficient.
    """
    arr = list(items)
    comparisons = 0
    swaps = 0

    def _quick_sort_helper(low: int, high: int):
        nonlocal comparisons, swaps
        if low < high:
            pivot_idx = _partition(low, high)
            _quick_sort_helper(low, pivot_idx - 1)
            _quick_sort_helper(pivot_idx + 1, high)

    def _partition(low: int, high: int) -> int:
        nonlocal comparisons, swaps
        pivot_val = key_func(arr[high])
        i = low - 1

        for j in range(low, high):
            comparisons += 1
            curr_val = key_func(arr[j])
            condition = (curr_val > pivot_val) if reverse else (curr_val < pivot_val)
            if condition:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                swaps += 1

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        swaps += 1
        return i + 1

    _quick_sort_helper(0, len(arr) - 1)
    return arr, comparisons, swaps
