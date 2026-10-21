# -*- coding: utf-8 -*-
"""
================================================================================
 CLASH-FREE TIMETABLE GENERATOR & ACADEMIC SCHEDULING SYSTEM
 Master Project Runner (Phases 1 - 4 + MySQL Database Backend)
================================================================================
"""
import sys
import os

# Set up module resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "phase1"))
sys.path.insert(0, os.path.join(BASE_DIR, "phase2"))
sys.path.insert(0, os.path.join(BASE_DIR, "phase3"))
sys.path.insert(0, os.path.join(BASE_DIR, "phase4"))
sys.path.insert(0, os.path.join(BASE_DIR, "database"))

import phase1.main as p1_main
import phase2.main as p2_main
import phase3.main as p3_main
import phase4.main as p4_main
from database.db_manager import DatabaseManager
from phase4.pipeline import TimetablePipeline


BANNER = """
================================================================================
          CLASH-FREE TIMETABLE GENERATOR & ACADEMIC SCHEDULER
                 Data Structures & Algorithms Project
================================================================================
  Phase 1: Linear Data Structures (LinkedList, Stack, Queue, Expression Checker)
  Phase 2: Hierarchical & Graph Structures (Binary Tree, BST, Conflict Graph, BFS/DFS)
  Phase 3: Searching & Sorting Operations (Linear/Binary Search, Merge/Quick Sort)
  Phase 4: Basic Algorithmic Problem Solving (Greedy, DP Knapsack, Backtracking CSP)
  Backend: MySQL Database & MySQL Workbench Integration
================================================================================
"""

MENU = """
  +--------------------------------------------------------------------------+
  |                        MASTER CONTROL PANEL                              |
  +--------------------------------------------------------------------------+
  |  1. Phase 1 Demo -- Linear Data Structures                               |
  |  2. Phase 2 Demo -- Hierarchical & Graph Structures                      |
  |  3. Phase 3 Demo -- Searching & Sorting Operations                       |
  |  4. Phase 4 Demo -- Basic Algorithmic Problem Solving                    |
  |  5. Run Complete End-to-End Timetable Pipeline                           |
  |  6. MySQL Backend -- Initialize Database & Seed Data                     |
  |  7. MySQL Backend -- Run Pipeline & Save Timetable to MySQL Database     |
  |  8. MySQL Backend -- View Saved Timetable from MySQL View                |
  |  9. Run ALL Phases Sequentially (Full Automated Demonstration)           |
  | 10. Launch Web Frontend Dashboard (Interactive Web UI)                   |
  |  0. Exit                                                                 |
  +--------------------------------------------------------------------------+
  Enter Choice [0-10]: """


def run_pipeline_with_mysql():
    print("\n  ================ RUNNING PIPELINE WITH MYSQL BACKEND ================")
    db = DatabaseManager()
    try:
        teachers = db.load_teachers()
        courses = db.load_courses()
        classrooms = db.load_classrooms()
        timeslots = db.load_timeslots()

        print(f"  [1] Loaded from MySQL: {len(teachers)} Teachers, {len(courses)} Courses, "
              f"{len(classrooms)} Classrooms, {len(timeslots)} TimeSlots.")

        pipeline = TimetablePipeline(teachers, courses, classrooms, timeslots)
        results = pipeline.run_pipeline()

        print(f"  [2] Solved with Backtracking & Greedy Allocation! Status: "
              f"{'SUCCESS' if results['backtracking_solved'] else 'FAILED'}")

        # Save back to MySQL
        count = db.save_timetable_assignments(results["final_schedule"])
        print(f"  [3] Saved {count} generated schedule records into MySQL table 'timetable_assignments'!")

        # Query and display from MySQL View
        records = db.fetch_master_timetable()
        print(f"\n  ================ MYSQL MASTER VIEW: v_clash_free_timetable ================")
        print(f"  {'Course':<24} | {'Teacher':<18} | {'Room':<8} | {'Day & Time':<24} | {'Status'}")
        print("  " + "-" * 88)
        for r in records:
            status = "[CLASH-FREE]" if r["is_clash_free"] else "[CLASH!]"
            day_time = f"{r['day']} {r['time_window']}"
            print(f"  {r['course_name']:<24} | {r['teacher_name']:<18} | "
                  f"{r['room_number']:<8} | {day_time:<24} | {status}")
        print("  ===========================================================================")
        print("  >> You can now open MySQL Workbench and run: SELECT * FROM v_clash_free_timetable;\n")
    except Exception as e:
        print(f"  [!] MySQL Error: {e}")
        print("  Ensure MySQL is running (default port 3306, user 'root', password 'root123').")


def view_mysql_timetable():
    db = DatabaseManager()
    try:
        records = db.fetch_master_timetable()
        if not records:
            print("\n  [!] No timetable records found in MySQL. Run Option 6 or 7 first.\n")
            return
        print(f"\n  ================ CURRENT MYSQL MASTER TIMETABLE ================")
        print(f"  {'ID':<4} | {'Course':<24} | {'Teacher':<18} | {'Room':<8} | {'Day & Time':<24}")
        print("  " + "-" * 88)
        for r in records:
            day_time = f"{r['day']} {r['time_window']}"
            print(f"  {r['assignment_id']:<4} | {r['course_name']:<24} | {r['teacher_name']:<18} | "
                  f"{r['room_number']:<8} | {day_time:<24}")
        print("  ================================================================\n")
    except Exception as e:
        print(f"  [!] MySQL Error: {e}\n")


def run_all_phases():
    print(BANNER)
    print("\n  >>> EXECUTING PHASE 1: LINEAR DATA STRUCTURES <<<")
    p1_main.main()

    print("\n  >>> EXECUTING PHASE 2: HIERARCHICAL & GRAPH STRUCTURES <<<")
    p2_main.run_all_demos()

    print("\n  >>> EXECUTING PHASE 3: SEARCHING & SORTING OPERATIONS <<<")
    p3_main.run_all_demos()

    print("\n  >>> EXECUTING PHASE 4: BASIC ALGORITHMIC PROBLEM SOLVING <<<")
    p4_main.run_all_demos()

    print("\n  >>> EXECUTING MYSQL DATABASE SYNCHRONIZATION <<<")
    run_pipeline_with_mysql()

    print("\n" + "=" * 80)
    print("  ALL PHASES AND MYSQL INTEGRATION COMPLETED SUCCESSFULLY!")
    print("=" * 80 + "\n")


def main():
    if "--all" in sys.argv:
        sys.argv.append("--auto")
        run_all_phases()
        return

    print(BANNER)
    while True:
        try:
            choice = input(MENU).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  Exiting...\n")
            break

        if choice == "0":
            print("\n  Exiting Clash-Free Timetable Generator. Goodbye!\n")
            break
        elif choice == "1":
            p1_main.main()
        elif choice == "2":
            p2_main.run_all_demos()
        elif choice == "3":
            p3_main.run_all_demos()
        elif choice == "4":
            p4_main.run_all_demos()
        elif choice == "5":
            p4_main.demo_pipeline()
        elif choice == "6":
            from database.setup_db import main as db_setup_main
            db_setup_main()
        elif choice == "7":
            run_pipeline_with_mysql()
        elif choice == "8":
            view_mysql_timetable()
        elif choice == "9":
            sys.argv.append("--auto")
            run_all_phases()
        elif choice in ("10", "w", "W"):
            import run_web
            from web_server import app
            import threading
            threading.Thread(target=run_web.open_browser, daemon=True).start()
            app.run(host="0.0.0.0", port=5050, debug=False)
        else:
            print("  Invalid selection. Please choose an option from 0 to 10.")


if __name__ == "__main__":
    main()
