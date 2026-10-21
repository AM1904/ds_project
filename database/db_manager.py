# -*- coding: utf-8 -*-
"""
Database Management Layer for MySQL & MySQL Workbench.
Bridges MySQL Database with Phase 1, Phase 2, Phase 3, and Phase 4 Data Structures & Algorithms.
Connects using pymysql or mysql.connector.
"""
import os
import sys
from typing import Dict, List, Optional, Any

# Ensure project paths are resolvable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase1"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase2"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase3"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "phase4"))

from data_models import Teacher, Course, Classroom, TimeSlot
from linked_list import LinkedList
from bst import BinarySearchTree
from graph import ConflictGraph

try:
    import pymysql
    import pymysql.cursors
    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False


class DatabaseManager:
    """
    Manages MySQL connections, database initialization, and data serialization
    between MySQL relational tables and Project Data Structures.
    """
    def __init__(self, host: str = "localhost", port: int = 3306,
                 user: str = "root", password: str = "root123",
                 database: str = "timetable_db"):
        self.host = os.getenv("MYSQL_HOST", host)
        self.port = int(os.getenv("MYSQL_PORT", port))
        self.user = os.getenv("MYSQL_USER", user)
        self.password = os.getenv("MYSQL_PASSWORD", password)
        self.database = os.getenv("MYSQL_DATABASE", database)

    def get_server_connection(self):
        """Connects to MySQL server without selecting a database (for DB creation)."""
        if not HAS_PYMYSQL:
            raise RuntimeError("pymysql is required. Run 'pip install pymysql'.")
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def get_db_connection(self):
        """Connects directly to the timetable_db database."""
        if not HAS_PYMYSQL:
            raise RuntimeError("pymysql is required. Run 'pip install pymysql'.")
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def initialize_database(self) -> bool:
        """Creates database and tables from schema.sql and seed_data.sql."""
        schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
        seed_path = os.path.join(os.path.dirname(__file__), "seed_data.sql")

        print(f"  [DB] Connecting to MySQL at {self.host}:{self.port} as '{self.user}'...")
        try:
            conn = self.get_server_connection()
            with conn.cursor() as cursor:
                # 1. Execute schema.sql
                print("  [DB] Executing schema.sql to create database and tables...")
                with open(schema_path, "r", encoding="utf-8") as f:
                    schema_sql = f.read()
                # Split and execute individual statements
                for statement in schema_sql.split(";"):
                    stmt = statement.strip()
                    if stmt:
                        cursor.execute(stmt)

                # 2. Execute seed_data.sql
                print("  [DB] Executing seed_data.sql to populate initial records...")
                with open(seed_path, "r", encoding="utf-8") as f:
                    seed_sql = f.read()
                for statement in seed_sql.split(";"):
                    stmt = statement.strip()
                    if stmt:
                        cursor.execute(stmt)

            conn.close()
            print("  [DB] SUCCESS: Database and initial tables populated successfully!")
            return True
        except Exception as e:
            print(f"  [!] MySQL Error during initialization: {e}")
            return False

    def load_teachers(self) -> List[Teacher]:
        """Fetches teachers from MySQL and returns as domain Teacher objects."""
        conn = self.get_db_connection()
        teachers = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT teacher_id, name, subject, max_hours FROM teachers ORDER BY teacher_id")
            for row in cursor.fetchall():
                teachers.append(Teacher(
                    teacher_id=row["teacher_id"],
                    name=row["name"],
                    subject=row["subject"],
                    max_hours=row["max_hours"]
                ))
        conn.close()
        return teachers

    def load_teachers_to_linked_list(self) -> LinkedList:
        """Phase 1 Bridge: Loads teachers from MySQL directly into Phase 1 LinkedList."""
        t_list = LinkedList("Teacher")
        teachers = self.load_teachers()
        for t in teachers:
            t_list.insert_at_tail(t)
        return t_list

    def load_courses(self) -> List[Course]:
        """Fetches courses with joined teacher names."""
        conn = self.get_db_connection()
        courses = []
        with conn.cursor() as cursor:
            query = """
                SELECT c.course_id, c.name, t.name AS teacher_name, c.hours_per_week
                FROM courses c
                JOIN teachers t ON c.teacher_id = t.teacher_id
                ORDER BY c.course_id
            """
            cursor.execute(query)
            for row in cursor.fetchall():
                courses.append(Course(
                    course_id=row["course_id"],
                    name=row["name"],
                    teacher_name=row["teacher_name"],
                    hours_per_week=row["hours_per_week"]
                ))
        conn.close()
        return courses

    def load_courses_to_bst(self) -> BinarySearchTree:
        """Phase 2 Bridge: Loads courses from MySQL directly into Phase 2 BST."""
        bst = BinarySearchTree("Course")
        courses = self.load_courses()
        for c in courses:
            bst.insert(c.course_id, c)
        return bst

    def load_classrooms(self) -> List[Classroom]:
        """Fetches classrooms from MySQL."""
        conn = self.get_db_connection()
        classrooms = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT room_id, room_number, capacity FROM classrooms ORDER BY room_id")
            for row in cursor.fetchall():
                classrooms.append(Classroom(
                    room_id=row["room_id"],
                    room_number=row["room_number"],
                    capacity=row["capacity"]
                ))
        conn.close()
        return classrooms

    def load_timeslots(self) -> List[TimeSlot]:
        """Fetches timeslots from MySQL."""
        conn = self.get_db_connection()
        timeslots = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT slot_id, day, start_time, end_time FROM timeslots ORDER BY slot_id")
            for row in cursor.fetchall():
                timeslots.append(TimeSlot(
                    slot_id=row["slot_id"],
                    day=row["day"],
                    start_time=row["start_time"],
                    end_time=row["end_time"]
                ))
        conn.close()
        return timeslots

    def load_conflict_graph(self) -> ConflictGraph:
        """Phase 2 & 4 Bridge: Loads vertices and conflict edges from MySQL into ConflictGraph."""
        conn = self.get_db_connection()
        graph = ConflictGraph()
        courses = self.load_courses()
        for c in courses:
            graph.add_vertex(c.course_id, c.name)

        with conn.cursor() as cursor:
            cursor.execute("SELECT course_id_1, course_id_2, reason FROM course_conflicts")
            for row in cursor.fetchall():
                graph.add_conflict(row["course_id_1"], row["course_id_2"], row["reason"])
        conn.close()
        return graph

    def save_timetable_assignments(self, schedule_records: List[Dict[str, Any]]) -> int:
        """
        Saves the generated clash-free timetable from Phase 4 into MySQL table timetable_assignments.
        """
        conn = self.get_db_connection()
        inserted_count = 0
        with conn.cursor() as cursor:
            # Clear old generated timetable
            cursor.execute("TRUNCATE TABLE timetable_assignments")

            # Lookups for IDs
            cursor.execute("SELECT course_id, name, teacher_id FROM courses")
            course_map = {row["name"]: (row["course_id"], row["teacher_id"]) for row in cursor.fetchall()}
            # Also map by course_id directly
            cursor.execute("SELECT course_id, teacher_id FROM courses")
            cid_map = {row["course_id"]: row["teacher_id"] for row in cursor.fetchall()}

            cursor.execute("SELECT room_id, room_number FROM classrooms")
            room_map = {row["room_number"]: row["room_id"] for row in cursor.fetchall()}

            cursor.execute("SELECT slot_id, day, start_time, end_time FROM timeslots")
            slots = cursor.fetchall()

            insert_sql = """
                INSERT INTO timetable_assignments (course_id, teacher_id, room_id, slot_id, is_clash_free)
                VALUES (%s, %s, %s, %s, %s)
            """

            for item in schedule_records:
                cid = item.get("course_id")
                tid = cid_map.get(cid, 1)

                r_num = item.get("classroom", "")
                rid = room_map.get(r_num, 201)

                # Match slot or pick first
                slot_id = 301
                slot_str = item.get("timeslot", "")
                for s in slots:
                    if s["day"] in slot_str and s["start_time"] in slot_str:
                        slot_id = s["slot_id"]
                        break

                cursor.execute(insert_sql, (cid, tid, rid, slot_id, item.get("is_clash_free", True)))
                inserted_count += 1

        conn.close()
        return inserted_count

    def fetch_master_timetable(self) -> List[Dict[str, Any]]:
        """Queries the view v_clash_free_timetable from MySQL."""
        conn = self.get_db_connection()
        results = []
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM v_clash_free_timetable")
            results = cursor.fetchall()
        conn.close()
        return results
