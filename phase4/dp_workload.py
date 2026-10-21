# -*- coding: utf-8 -*-
"""
Phase 4: Dynamic Programming - Faculty Workload & Course Credit Optimizer
Solves the 0/1 Knapsack Problem for academic course allocations:
Maximize total instructional credit / value subject to the Faculty Maximum Workload constraint (W hours/week).
Builds the 2D DP Table and reconstructs the optimal set of courses selected.
"""
from typing import List, Dict, Tuple, Any


class CourseModule:
    """A course module requiring teaching hours with an associated curriculum credit value."""
    def __init__(self, code: str, title: str, hours: int, credit_value: int):
        self.code = code
        self.title = title
        self.hours = hours            # Knapsack weight
        self.credit_value = credit_value  # Knapsack profit/value

    def __str__(self):
        return f"[{self.code}] {self.title:<24} | {self.hours} hrs/wk | {self.credit_value} pts"


def optimize_workload_dp(
    modules: List[CourseModule],
    max_workload_hours: int
) -> Tuple[int, List[CourseModule], List[List[int]]]:
    """
    0/1 Knapsack Dynamic Programming:
    dp[i][w] = Maximum credit points achievable using a subset of first i modules
               within total workload limit w.

    Recurrence Relation:
      If module[i-1].hours <= w:
        dp[i][w] = max(dp[i-1][w], dp[i-1][w - module[i-1].hours] + module[i-1].credit_value)
      Else:
        dp[i][w] = dp[i-1][w]

    Time Complexity: O(N * W)
    Space Complexity: O(N * W)
    Returns: (max_credits, selected_modules, dp_table)
    """
    n = len(modules)
    W = max_workload_hours

    # Initialize (n + 1) x (W + 1) table with 0s
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Fill DP table
    for i in range(1, n + 1):
        curr = modules[i - 1]
        for w in range(W + 1):
            if curr.hours <= w:
                dp[i][w] = max(
                    dp[i - 1][w],
                    dp[i - 1][w - curr.hours] + curr.credit_value
                )
            else:
                dp[i][w] = dp[i - 1][w]

    # Reconstruct optimal selection
    selected: List[CourseModule] = []
    rem_w = W
    for i in range(n, 0, -1):
        if dp[i][rem_w] != dp[i - 1][rem_w]:
            selected.append(modules[i - 1])
            rem_w -= modules[i - 1].hours

    selected.reverse()
    max_credits = dp[n][W]
    return max_credits, selected, dp


def print_dp_table(modules: List[CourseModule], dp: List[List[int]], max_w: int) -> None:
    """Displays the Dynamic Programming matrix."""
    print("\n  ===================== 2D DYNAMIC PROGRAMMING TABLE =====================")
    header = "Module \\ Hours | " + " ".join(f"{w:>3}" for w in range(max_w + 1))
    print(f"  {header}")
    print("  " + "-" * len(header))

    print(f"  {'[Initial]':<14} | " + " ".join(f"{dp[0][w]:>3}" for w in range(max_w + 1)))
    for i, mod in enumerate(modules, 1):
        row_str = " ".join(f"{dp[i][w]:>3}" for w in range(max_w + 1))
        print(f"  {mod.code:<14} | {row_str}")
    print("  ========================================================================\n")
