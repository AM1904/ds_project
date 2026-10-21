# -*- coding: utf-8 -*-
"""
Phase 3: Conceptual & Empirical Performance Analysis
1. Conceptual Complexity Matrix (Theoretical Big-O comparison table).
2. Empirical Benchmarking (Measures actual execution time and operations across varying sizes).
"""
import random
import time
from typing import Dict, List
from searching import linear_search, binary_search
from sorting import insertion_sort, merge_sort, quick_sort


def display_conceptual_comparison():
    """Prints the comprehensive Big-O Complexity and Characteristics Matrix."""
    matrix = """
  ======================== CONCEPTUAL COMPLEXITY COMPARISON ========================
  Algorithm       | Best Time   | Average Time| Worst Time  | Space      | Stable?
  ----------------+-------------+-------------+-------------+------------+---------
  Linear Search   | O(1)        | O(n)        | O(n)        | O(1)       | N/A
  Binary Search   | O(1)        | O(log n)    | O(log n)    | O(1)       | N/A
  ----------------+-------------+-------------+-------------+------------+---------
  Insertion Sort  | O(n)        | O(n^2)      | O(n^2)      | O(1)       | YES
  Merge Sort      | O(n log n)  | O(n log n)  | O(n log n)  | O(n)       | YES
  Quick Sort      | O(n log n)  | O(n log n)  | O(n^2)      | O(log n)   | NO
  ==================================================================================

  Key Timetabling Domain Insights:
  1. Searching:
     - Linear Search is optimal for unsorted or dynamic lists with frequent inserts.
     - Binary Search reduces search time drastically (e.g. log2(1000) ~ 10 comparisons vs 1000).
  2. Sorting:
     - Insertion Sort is ideal for small batches or nearly-sorted incremental updates.
     - Merge Sort guarantees O(n log n) with stability (critical when maintaining secondary sort order,
       e.g., sorting courses by hours while preserving teacher alphabetization).
     - Quick Sort is the fastest in-place algorithm for large datasets without extra memory overhead.
  """
    print(matrix)


def run_empirical_benchmark(sizes: List[int] = [10, 50, 100, 300]) -> None:
    """
    Executes empirical benchmarks on randomly generated datasets of different sizes.
    Compares comparisons and elapsed time (microseconds).
    """
    print("\n  ===================== EMPIRICAL BENCHMARKING RESULTS =====================")
    print(f"  {'Size (N)':<10} | {'Algorithm':<16} | {'Comparisons':<14} | {'Time (us)':<12}")
    print("  " + "-" * 60)

    for n in sizes:
        dataset = [random.randint(1, 10000) for _ in range(n)]
        target = dataset[random.randint(0, n - 1)]

        # --- Search Benchmarks ---
        t0 = time.perf_counter()
        _, _, lin_comps = linear_search(dataset, target)
        t_lin = (time.perf_counter() - t0) * 1_000_000

        sorted_dataset = sorted(dataset)
        t0 = time.perf_counter()
        _, _, bin_comps = binary_search(sorted_dataset, target)
        t_bin = (time.perf_counter() - t0) * 1_000_000

        print(f"  {n:<10} | {'Linear Search':<16} | {lin_comps:<14} | {t_lin:<12.2f}")
        print(f"  {n:<10} | {'Binary Search':<16} | {bin_comps:<14} | {t_bin:<12.2f}")

        # --- Sorting Benchmarks ---
        # Insertion Sort
        t0 = time.perf_counter()
        _, ins_comps, _ = insertion_sort(dataset)
        t_ins = (time.perf_counter() - t0) * 1_000_000

        # Merge Sort
        t0 = time.perf_counter()
        _, mrg_comps, _ = merge_sort(dataset)
        t_mrg = (time.perf_counter() - t0) * 1_000_000

        # Quick Sort
        t0 = time.perf_counter()
        _, qck_comps, _ = quick_sort(dataset)
        t_qck = (time.perf_counter() - t0) * 1_000_000

        print(f"  {n:<10} | {'Insertion Sort':<16} | {ins_comps:<14} | {t_ins:<12.2f}")
        print(f"  {n:<10} | {'Merge Sort':<16} | {mrg_comps:<14} | {t_mrg:<12.2f}")
        print(f"  {n:<10} | {'Quick Sort':<16} | {qck_comps:<14} | {t_qck:<12.2f}")
        print("  " + "-" * 60)
