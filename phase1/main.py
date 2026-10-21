# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from data_models import Teacher, Course, Classroom, TimeSlot
from linked_list import LinkedList
from stack import Stack
from queue_ds import Queue
from expression_handler import run_expression_demo, validate_expression


SEED_TEACHERS = [
    Teacher(1, "Dr. Ananya Sharma", "Data Structures", 16),
    Teacher(2, "Prof. Ravi Kumar", "Operating Systems", 14),
    Teacher(3, "Ms. Priya Nair", "DBMS", 12),
    Teacher(4, "Mr. Arjun Mehta", "Computer Networks", 10),
    Teacher(5, "Dr. Sunita Rao", "Machine Learning", 18),
]

SEED_COURSES = [
    Course(101, "Data Structures & Algo", "Dr. Ananya Sharma", 4),
    Course(102, "Operating Systems", "Prof. Ravi Kumar", 3),
    Course(103, "Database Management", "Ms. Priya Nair", 3),
    Course(104, "Computer Networks", "Mr. Arjun Mehta", 3),
    Course(105, "Introduction to ML", "Dr. Sunita Rao", 2),
]

SEED_CLASSROOMS = [
    Classroom(201, "A-101", 60),
    Classroom(202, "B-202", 45),
    Classroom(203, "C-303", 30),
    Classroom(204, "Lab-1", 25),
]

SEED_TIMESLOTS = [
    TimeSlot(301, "Monday", "09:00", "10:00"),
    TimeSlot(302, "Monday", "10:00", "11:00"),
    TimeSlot(303, "Tuesday", "09:00", "10:00"),
    TimeSlot(304, "Wednesday", "11:00", "12:00"),
    TimeSlot(305, "Thursday", "14:00", "15:00"),
    TimeSlot(306, "Friday", "13:00", "14:00"),
]


def banner():
    print("\n" + "=" * 62)
    print("   +--------------------------------------------------+")
    print("   |   CLASH-FREE TIMETABLE GENERATOR                |")
    print("   |   Phase 1 -- Linear Data Structures Demo        |")
    print("   +--------------------------------------------------+")
    print("=" * 62 + "\n")


def section(title: str):
    print("\n  +-----------------------------------------------+")
    print(f"  |  {title:<45}|")
    print("  +-----------------------------------------------+")


def pause():
    if "--auto" not in sys.argv:
        input("\n  [Press ENTER to continue...]\n")


def demo_teachers():
    section("1 . LinkedList<Teacher>")

    tlist = LinkedList("Teacher")

    print("\n  >> insert_at_tail: loading seed teachers")
    for t in SEED_TEACHERS:
        tlist.insert_at_tail(t)

    print("\n  >> insert_at_head: adding a new teacher at front")
    tlist.insert_at_head(Teacher(6, "Dr. Neha Gupta", "Compiler Design", 12))

    print("\n  >> insert_at_position(3): inserting at position 3")
    tlist.insert_at_position(Teacher(7, "Mr. Vivek Joshi", "Software Eng.", 10), 3)

    print("\n  >> traverse: full teacher list")
    tlist.traverse()

    print("\n  >> search(ID=3)")
    result = tlist.search(3)
    if result:
        print(f"     Found: {result}")

    print("\n  >> search(ID=99) -- does not exist")
    tlist.search(99)

    print("\n  >> delete_by_id(6) -- remove head teacher")
    tlist.delete_by_id(6)

    print("\n  >> delete_at_position(2) -- remove 2nd record")
    tlist.delete_at_position(2)

    print("\n  >> delete_by_id(99) -- non-existent ID")
    tlist.delete_by_id(99)

    print(f"\n  >> traverse: final state  (size = {tlist.get_size()})")
    tlist.traverse()

    pause()


def demo_courses():
    section("2 . LinkedList<Course>")

    clist = LinkedList("Course")

    print("\n  >> insert_at_tail: loading seed courses")
    for c in SEED_COURSES:
        clist.insert_at_tail(c)

    print("\n  >> insert_at_head: priority course at front")
    clist.insert_at_head(Course(100, "Engineering Mathematics", "Prof. Ravi Kumar", 5))

    print("\n  >> traverse: full course list")
    clist.traverse()

    print("\n  >> search(ID=103)")
    r = clist.search(103)
    if r:
        print(f"     Found: {r}")

    print("\n  >> delete_by_id(102)")
    clist.delete_by_id(102)

    print(f"\n  >> traverse: after deletion  (size = {clist.get_size()})")
    clist.traverse()

    pause()


def demo_classrooms():
    section("3 . LinkedList<Classroom>")

    rlist = LinkedList("Classroom")

    print("\n  >> insert_at_tail: loading seed classrooms")
    for r in SEED_CLASSROOMS:
        rlist.insert_at_tail(r)

    print("\n  >> insert_at_position(2): new room at position 2")
    rlist.insert_at_position(Classroom(205, "D-404", 80), 2)

    print("\n  >> traverse: full classroom list")
    rlist.traverse()

    print("\n  >> search(ID=204)")
    r = rlist.search(204)
    if r:
        print(f"     Found: {r}")

    print("\n  >> delete_at_position(1): remove first room")
    rlist.delete_at_position(1)

    print(f"\n  >> traverse: after deletion  (size = {rlist.get_size()})")
    rlist.traverse()

    pause()


def demo_timeslots():
    section("4 . LinkedList<TimeSlot>")

    slist = LinkedList("TimeSlot")

    print("\n  >> insert_at_tail: loading seed time slots")
    for s in SEED_TIMESLOTS:
        slist.insert_at_tail(s)

    print("\n  >> traverse: full time slot list")
    slist.traverse()

    print("\n  >> search(ID=305)")
    r = slist.search(305)
    if r:
        print(f"     Found: {r}")

    print("\n  >> delete_by_id(303)")
    slist.delete_by_id(303)

    print(f"\n  >> traverse: after deletion  (size = {slist.get_size()})")
    slist.traverse()

    pause()


def demo_stack():
    section("5 . Stack<TimeSlot>  --  Slot Assignment Undo History")

    undo_stack = Stack(label="UndoSlots")

    print("\n  Scenario: Scheduler assigns 3 time slots; each assignment")
    print("  is pushed onto the stack so it can be undone in reverse order.\n")

    slots_to_assign = [SEED_TIMESLOTS[0], SEED_TIMESLOTS[2], SEED_TIMESLOTS[4]]

    for s in slots_to_assign:
        print(f"  Assigning -> {s}")
        undo_stack.push(s)

    print("\n  >> Stack state after 3 assignments:")
    undo_stack.display()

    print(f"\n  >> peek (top of stack, no removal):")
    top = undo_stack.peek()
    print(f"     {top}")

    print("\n  >> pop (undo last assignment):")
    undone = undo_stack.pop()
    print(f"     Undone: {undone}")

    print("\n  >> pop (undo again):")
    undone = undo_stack.pop()
    print(f"     Undone: {undone}")

    print("\n  >> Stack state after 2 undos:")
    undo_stack.display()

    print("\n  >> pop remaining + attempt empty pop:")
    undo_stack.pop()
    undo_stack.pop()

    pause()


def demo_queue():
    section("6 . Queue<Course>  --  Pending Scheduling Queue")

    pending = Queue(label="PendingCourses")

    print("\n  Scenario: Courses arrive and are enqueued; the scheduler")
    print("  dequeues them one at a time to assign rooms & slots.\n")

    for c in SEED_COURSES[:4]:
        print(f"  Enqueuing -> {c}")
        pending.enqueue(c)

    print("\n  >> Queue state (4 pending courses):")
    pending.display()

    print(f"\n  >> front() -- next course to schedule:")
    f = pending.front()
    print(f"     {f}")

    print("\n  >> dequeue (scheduling course 1):")
    scheduled = pending.dequeue()
    print(f"     Scheduled: {scheduled}")

    print("\n  >> dequeue (scheduling course 2):")
    scheduled = pending.dequeue()
    print(f"     Scheduled: {scheduled}")

    print(f"\n  >> Queue state after 2 dequeues  (size = {pending.get_size()}):")
    pending.display()

    pause()


def demo_expression():
    section("7 . Stack-Based Constraint Expression Validator")
    print("\n  Purpose: Before the scheduler evaluates a constraint rule,")
    print("  it first checks whether the expression string is syntactically")
    print("  valid (all brackets balanced) using the custom Stack.\n")
    run_expression_demo()

    if "--auto" not in sys.argv:
        print("\n  >> Interactive check -- enter your own expression:")
        user_expr = input("     Expression: ").strip()
        result = validate_expression(user_expr)
        print(f"     Result: {'[VALID]' if result else '[INVALID]'}")

    pause()


MENU = """
  +-------------------------------------------------------+
  |              PHASE 1 -- MAIN MENU                     |
  +-------------------------------------------------------+
  |  1. LinkedList<Teacher>   - insert/delete/traverse    |
  |  2. LinkedList<Course>    - insert/delete/traverse    |
  |  3. LinkedList<Classroom> - insert/delete/traverse    |
  |  4. LinkedList<TimeSlot>  - insert/delete/traverse    |
  |  5. Stack Demo            - undo slot assignment      |
  |  6. Queue Demo            - pending course queue      |
  |  7. Expression Validator  - stack bracket checker     |
  |  8. Run ALL demos in sequence                         |
  |  0. Exit                                              |
  +-------------------------------------------------------+
  Choice: """

DEMOS = {
    "1": demo_teachers,
    "2": demo_courses,
    "3": demo_classrooms,
    "4": demo_timeslots,
    "5": demo_stack,
    "6": demo_queue,
    "7": demo_expression,
}


def main():
    banner()
    if "--auto" in sys.argv:
        for fn in DEMOS.values():
            fn()
        print("\n  Phase 1 Demo Complete (--auto mode)\n")
        return

    while True:
        choice = input(MENU).strip()

        if choice == "0":
            print("\n  Goodbye! -- Clash-Free Timetable Generator, Phase 1\n")
            break
        elif choice in DEMOS:
            DEMOS[choice]()
        elif choice == "8":
            for fn in DEMOS.values():
                fn()
        else:
            print("  Invalid choice -- please enter 0-8.\n")


if __name__ == "__main__":
    main()
