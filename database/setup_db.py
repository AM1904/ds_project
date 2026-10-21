# -*- coding: utf-8 -*-
"""
One-click script to set up MySQL Database schema and seed data.
Can be executed from terminal or imported directly.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from db_manager import DatabaseManager


def main():
    print("\n" + "=" * 65)
    print("   +-------------------------------------------------------+")
    print("   |   MYSQL DATABASE SETUP & WORKBENCH SYNCHRONIZATION   |")
    print("   +-------------------------------------------------------+")
    print("=" * 65 + "\n")

    db = DatabaseManager()
    success = db.initialize_database()

    if success:
        print("\n  >> Testing Data Fetch from MySQL:")
        teachers = db.load_teachers()
        courses = db.load_courses()
        classrooms = db.load_classrooms()
        timeslots = db.load_timeslots()

        print(f"     [OK] Loaded {len(teachers)} Teachers from MySQL")
        print(f"     [OK] Loaded {len(courses)} Courses from MySQL")
        print(f"     [OK] Loaded {len(classrooms)} Classrooms from MySQL")
        print(f"     [OK] Loaded {len(timeslots)} TimeSlots from MySQL")

        print("\n  >> Testing Bridge to Phase 1 LinkedList:")
        t_list = db.load_teachers_to_linked_list()
        print(f"     [OK] Successfully populated LinkedList<Teacher> with {t_list.get_size()} nodes!")

        print("\n  >> Testing Bridge to Phase 2 BST:")
        bst = db.load_courses_to_bst()
        print(f"     [OK] Successfully indexed {bst.get_size()} Courses into Binary Search Tree!")

        print("\n  >> Testing Bridge to Phase 2/4 Conflict Graph:")
        graph = db.load_conflict_graph()
        print(f"     [OK] Successfully built ConflictGraph with {len(graph.get_vertices())} course nodes!")

        print("\n" + "=" * 65)
        print("  Database is 100% Ready! You can now open MySQL Workbench.")
        print("=" * 65 + "\n")
    else:
        print("\n  [!] Could not connect to MySQL. Ensure MySQL server is running.")


if __name__ == "__main__":
    main()
