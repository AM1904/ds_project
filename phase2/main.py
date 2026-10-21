# -*- coding: utf-8 -*-
"""
Phase 2 Demo: Hierarchical and Graph Structures
Covers:
1. Binary Tree for structured curriculum/department hierarchy + Inorder, Preorder, Postorder traversals.
2. Binary Search Tree (BST) for O(log n) Course storage, search, deletion, and min/max.
3. Timetable Conflict Graph (Adjacency List & Adjacency Matrix).
4. Graph Traversals (BFS and DFS) & Connected Components discovery.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))

from binary_tree import BinaryTree, TreeNode
from bst import BinarySearchTree
from graph import ConflictGraph
from traversals import bfs_traversal, dfs_traversal, find_connected_components
from data_models import Course


def banner():
    print("\n" + "=" * 65)
    print("   +-------------------------------------------------------+")
    print("   |   CLASH-FREE TIMETABLE GENERATOR                     |")
    print("   |   Phase 2 -- Hierarchical and Graph Structures        |")
    print("   +-------------------------------------------------------+")
    print("=" * 65 + "\n")


def section(title: str):
    print("\n  +-------------------------------------------------------+")
    print(f"  |  {title:<53}|")
    print("  +-------------------------------------------------------+")


def demo_binary_tree():
    section("1. Binary Tree: Academic Department Hierarchy")
    print("  Building curriculum hierarchy:")
    print("               [Faculty of Engineering]")
    print("                 /                  \\")
    print("     [Computer Science]          [Data Science]")
    print("       /          \\                 /         \\")
    print("  [Core Systems] [AI Stream]    [Analytics]  [Big Data]")

    tree = BinaryTree("Faculty of Engineering", "Dean Office")
    tree.root.left = TreeNode("Computer Science", "Dept A")
    tree.root.right = TreeNode("Data Science", "Dept B")

    tree.root.left.left = TreeNode("Core Systems", "CS-101/102")
    tree.root.left.right = TreeNode("AI Stream", "CS-105")

    tree.root.right.left = TreeNode("Analytics", "DS-201")
    tree.root.right.right = TreeNode("Big Data", "DS-202")

    print("\n  >> Tree Structure Visualization:")
    tree.display()

    print("\n  >> 1. Preorder Traversal (Root -> Left -> Right):")
    print("     Useful for top-down administrative breakdown:")
    for item in tree.preorder():
        print(f"     * {item}")

    print("\n  >> 2. Inorder Traversal (Left -> Root -> Right):")
    print("     Useful for symmetric curriculum inspection:")
    for item in tree.inorder():
        print(f"     * {item}")

    print("\n  >> 3. Postorder Traversal (Left -> Right -> Root):")
    print("     Useful for prerequisite resolution / bottom-up resource closing:")
    for item in tree.postorder():
        print(f"     * {item}")


def demo_bst():
    section("2. Binary Search Tree (BST): Course ID Indexing")
    bst = BinarySearchTree("Course")

    sample_courses = [
        Course(103, "Database Management", "Ms. Priya Nair", 3),
        Course(101, "Data Structures & Algo", "Dr. Ananya Sharma", 4),
        Course(105, "Introduction to ML", "Dr. Sunita Rao", 2),
        Course(102, "Operating Systems", "Prof. Ravi Kumar", 3),
        Course(104, "Computer Networks", "Mr. Arjun Mehta", 3),
        Course(106, "Compiler Design", "Dr. Neha Gupta", 3),
    ]

    print("\n  >> Inserting courses into BST by course_id:")
    for c in sample_courses:
        bst.insert(c.course_id, c)
        print(f"     Inserted Course ID {c.course_id}: {c.name}")

    print("\n  >> BST Hierarchy Display:")
    bst.display()

    print("\n  >> In-order Sorted Traversal (Guaranteed Sorted Order by Key):")
    sorted_courses = bst.inorder_sorted()
    for c in sorted_courses:
        print(f"     ID {c.course_id:>3}: {c.name:<25} ({c.teacher_name})")

    print("\n  >> BST Search vs Comparisons:")
    for target in [104, 101, 109]:
        record, comps = bst.search(target)
        if record:
            print(f"     Search ID {target}: FOUND in {comps} comparison(s) -> {record.name}")
        else:
            print(f"     Search ID {target}: NOT FOUND after {comps} comparison(s)")

    print("\n  >> Find Min and Max Course IDs:")
    min_node = bst.find_min()
    max_node = bst.find_max()
    print(f"     Minimum Course ID: {min_node.key} ({min_node.data.name})")
    print(f"     Maximum Course ID: {max_node.key} ({max_node.data.name})")

    print("\n  >> Deleting Course ID 103 (Node with two children):")
    bst.delete(103)
    print("     Deleted ID 103. In-order traversal after deletion:")
    for c in bst.inorder_sorted():
        print(f"     ID {c.course_id:>3}: {c.name:<25}")


def build_sample_conflict_graph() -> ConflictGraph:
    graph = ConflictGraph()
    # Add Courses
    graph.add_vertex(101, "Data Structures")
    graph.add_vertex(102, "Operating Systems")
    graph.add_vertex(103, "Database Management")
    graph.add_vertex(104, "Computer Networks")
    graph.add_vertex(105, "Machine Learning")
    graph.add_vertex(106, "Web Technologies")  # Component 2 (Evening / Elective)
    graph.add_vertex(107, "Mobile App Dev")     # Component 2

    # Add Conflicts
    graph.add_conflict(101, 102, "Shared Cohort (Year 2 Section A)")
    graph.add_conflict(101, 103, "Shared Teacher (Dr. Ananya)")
    graph.add_conflict(102, 104, "Shared Lab Equipment (Systems Lab)")
    graph.add_conflict(103, 105, "Shared Cohort (Year 2 Electives)")
    graph.add_conflict(104, 105, "Shared Teacher (Prof. Ravi)")

    # Separate component conflicts
    graph.add_conflict(106, 107, "Shared Lab (Web & App Lab)")
    return graph


def demo_graph():
    section("3. Timetable Conflict Graph (Adjacency List & Matrix)")
    graph = build_sample_conflict_graph()

    print("\n  Conflict edges represent courses that CANNOT share the same timeslot.")
    graph.display_adjacency_list()
    graph.display_adjacency_matrix()


def demo_traversals():
    section("4. Graph Traversals (BFS and DFS) & Conflict Analysis")
    graph = build_sample_conflict_graph()

    start_node = 101
    print(f"\n  >> 1. Breadth-First Search (BFS) from Course {start_node} ({graph.vertex_names[start_node]}):")
    bfs_order, levels = bfs_traversal(graph, start_node)
    print(f"     BFS Visit Sequence: {' -> '.join(str(c) for c in bfs_order)}")
    print("     Conflict Distance from Start:")
    for cid in bfs_order:
        print(f"       Course {cid} ({graph.vertex_names[cid]}): Conflict Distance Level {levels[cid]}")

    print(f"\n  >> 2. Depth-First Search (DFS) from Course {start_node}:")
    dfs_order = dfs_traversal(graph, start_node)
    print(f"     DFS Visit Sequence: {' -> '.join(str(c) for c in dfs_order)}")

    print("\n  >> 3. Discovered Connected Components (Independent Timetable Clusters):")
    components = find_connected_components(graph)
    for i, comp in enumerate(components, 1):
        names = [f"{cid} ({graph.vertex_names[cid]})" for cid in comp]
        print(f"     Cluster #{i} ({len(comp)} courses): {', '.join(names)}")
    print("     Insight: Cluster #1 and Cluster #2 can be scheduled in parallel without conflicts!")


def run_all_demos():
    banner()
    demo_binary_tree()
    demo_bst()
    demo_graph()
    demo_traversals()
    print("\n  " + "=" * 65)
    print("  Phase 2 Demonstrations Completed Successfully!")
    print("  " + "=" * 65 + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        run_all_demos()
    else:
        run_all_demos()
