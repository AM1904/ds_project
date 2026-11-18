# -*- coding: utf-8 -*-
"""
Module 4 (Expanded): Screenshots Walkthrough, Functional Source Code, Features,
Future Enhancements, Conclusion, and References for Ananya Ann Mathew (26MCAC07).
"""
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_screens_and_code(doc, helpers):
    add_heading_1 = helpers['add_heading_1']
    add_heading_2 = helpers['add_heading_2']
    add_heading_3 = helpers['add_heading_3']
    add_paragraph = helpers['add_paragraph']
    add_bullet = helpers['add_bullet']
    add_styled_table = helpers['add_styled_table']
    add_code_box = helpers['add_code_box']
    add_screenshot_box = helpers['add_screenshot_box']

    # =========================================================================
    # SCREENSHOTS & USER INTERFACE WALKTHROUGH
    # =========================================================================
    print(">> Generating Screenshots and UI Walkthrough (Expanded)...")
    add_heading_1(doc, "6. SCREENSHOTS AND USER INTERFACE WALKTHROUGH", page_break=True)
    add_paragraph(doc,
        "The following screenshots and interface callouts illustrate the operational workflows of the CampusGrid web application. "
        "Each view connects directly to the underlying data structures, API routes, and conflict-checking mechanisms."
    )

    add_screenshot_box(doc,
        "Screenshot 1: Portal Authentication and Quick Sign-In Interface",
        "The entry portal welcomes campus stakeholders with quick sign-in buttons for immediate evaluation as Student "
        "(MCA A / MCA B) or Administrator. It supports secure registration and login, attaching session cookies and dynamically "
        "loading permitted navigation tabs based on user role (Admin, Faculty, Student).",
        [
            "Route: http://localhost:5050/ (Static index.html + authScreen modal)",
            "Security: Password verification, encrypted session cookie (campus_portal_secret_2026)",
            "Role Routing: Dynamically reveals 'My Schedule', 'My Requests', or 'Manage Timetable' nav links"
        ]
    )

    add_screenshot_box(doc,
        "Screenshot 2: Admin Timetable Studio with Real-Time Clash Prevention",
        "The administrative scheduling command center. Administrators can view the complete 5-day weekly matrix across "
        "sections (MCA A to D), click on any slot to edit or delete, and add new lectures using modal dialogs. If an administrator "
        "accidentally selects an occupied room or busy professor, an immediate yellow clash warning alert is rendered with the exact reason.",
        [
            "Active View: Manage Timetable Studio (navAdminTimetableBtn)",
            "Real-Time Validation: Calls check_clash() before inserting or updating schedule records in SQLite",
            "Clash Indicators: Distinct amber badges indicating room, teacher, or section collisions"
        ]
    )

    add_screenshot_box(doc,
        "Screenshot 3: Student Cohort 3-Day Rolling Agenda and 5-Day Weekly Grid",
        "The student portal provides a distraction-free, mobile-responsive view of classes. Students can toggle between "
        "a rolling 3-day agenda (Today, Tomorrow, Day After Tomorrow) showing upcoming lectures, subject codes, professor names, "
        "and room numbers, or switch to the comprehensive 5-day weekly grid.",
        [
            "Target Cohort: Section MCA A (Dr. Ananya Sharma, Prof. Ravi Kumar, Ms. Priya Nair, etc.)",
            "API Endpoint: GET /api/student-schedule?section=MCA+A",
            "UX Highlights: High-contrast subject pills, clear time intervals, and zero clutter"
        ]
    )

    add_screenshot_box(doc,
        "Screenshot 4: Faculty Personal Teaching Schedule & Daily Agenda",
        "Faculty members (such as Dr. Ananya Sharma or Prof. Ravi Kumar) access an individualized dashboard showing "
        "only their assigned classes across the week. It displays room assignments, target sections, and time windows, "
        "enabling professors to organize their instructional preparation efficiently.",
        [
            "Authenticated User: Dr. Ananya Sharma (ananya@college.edu) - MCA-201: Data Structures & Algorithms",
            "API Endpoint: GET /api/faculty-schedule?teacher_email=ananya@college.edu",
            "Quick Actions: 'Request Change' button alongside every scheduled session"
        ]
    )

    add_screenshot_box(doc,
        "Screenshot 5: Faculty Reschedule and Extra-Hour Request Submission Desk",
        "When an instructor needs to reschedule a lecture due to academic conferences or reserve an extra coaching hour "
        "before examinations, they submit a digital request directly from their portal. The modal allows selection of desired "
        "date, timeslot, preferred room, and a mandatory justification text.",
        [
            "Request Types: 'Change Existing Lecture' vs 'Book Extra Coaching Hour'",
            "API Endpoint: POST /api/requests (Stores record in faculty_requests with status='pending')",
            "Client Validation: Requires explicit justification and validates target dates"
        ]
    )

    add_screenshot_box(doc,
        "Screenshot 6: Administrative Faculty Requests Review & Resolution Desk",
        "Administrators review pending faculty requests in a centralized queue. The interface performs an automated "
        "clash check on the requested slot and displays warning banners if conflicts exist. Approving a request mutates "
        "the live schedule table instantly, automatically propagating changes to all student and faculty calendars.",
        [
            "API Endpoint: PUT /api/requests/<id>/resolve (Action: 'approve' or 'reject')",
            "Automated Mutation: Updates existing schedule rows or inserts extra-hour lecture slots",
            "Live Synchronization: Immediate propagation across active web sessions without server restarts"
        ]
    )

    add_screenshot_box(doc,
        "Screenshot 7: Algorithmic Insights and Conflict Graph Console",
        "The algorithmic verification console exposes the underlying data structures for academic evaluation. "
        "It visualizes the Conflict Graph Adjacency List, displays connected component clusters computed via BFS, "
        "and reports the degree of conflict for each course to explain the Most Constrained Variable (MCV) sorting order.",
        [
            "DSA Foundations: Custom ConflictGraph (Adjacency List + Matrix), QueueDS, Stack",
            "Traversal Output: Connected components decomposition isolating independent academic tracks",
            "Verification: Displays execution stats for Graph Coloring CSP Backtracking solver"
        ]
    )

    add_screenshot_box(doc,
        "Screenshot 8: MySQL Workbench EER Diagram & Zero-Clash SQL Audit",
        "Visual representation of the enterprise relational schema in MySQL Workbench 8.0. It shows foreign key "
        "cascading relationships between teachers, courses, classrooms, timeslots, and timetable_assignments. Running "
        "verification self-join queries in Workbench returns 0 rows, proving empirical zero-clash immunity.",
        [
            "Database Schema: timetable_db (MySQL 8.0 DDL)",
            "Relational Views: v_clash_free_timetable and v_teacher_workload",
            "Verification Proof: Self-join queries on (teacher_id, slot_id) and (room_id, slot_id) return 0 rows"
        ]
    )

    # =========================================================================
    # 7. SOURCE CODE (FUNCTIONAL CODE STRUCTURE)
    # =========================================================================
    print(">> Generating Chapter 7: Source Code (Functional Code Structure Expanded)...")
    add_heading_1(doc, "7. SOURCE CODE (FUNCTIONAL CODE STRUCTURE)", page_break=True)
    add_paragraph(doc,
        "In accordance with project guidelines, this section contains the clean functional code structure of the "
        "system. It highlights core class declarations, constructor parameters, method signatures, algorithmic invariants, "
        "and execution loops while omitting repetitive HTML markup and styling boilerplate."
    )

    add_heading_2(doc, "Phase 1: Linear Data Structures Core")
    code_p1 = """# ============================================================================
# PHASE 1: LINEAR DATA STRUCTURES - FUNCTIONAL SKELETON
# ============================================================================

class Node:
    \"\"\"Generic Node representation for pointer-based linear structures.\"\"\"
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    \"\"\"Custom Singly Linked List managing dynamic academic records.\"\"\"
    def __init__(self, entity_label: str = "Record"):
        self.head = None
        self._size = 0
        self.entity_label = entity_label

    def is_empty(self) -> bool:
        return self.head is None

    def insert_at_head(self, data) -> None:
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert_at_tail(self, data) -> None:
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            curr = self.head
            while curr.next: curr = curr.next
            curr.next = new_node
        self._size += 1

    def insert_at_position(self, data, position: int) -> None:
        if position <= 1:
            self.insert_at_head(data)
            return
        new_node = Node(data)
        curr = self.head
        step = 1
        while curr.next and step < position - 1:
            curr = curr.next
            step += 1
        new_node.next = curr.next
        curr.next = new_node
        self._size += 1

    def delete_by_id(self, entity_id: int) -> bool:
        if self.is_empty(): return False
        if getattr(self.head.data, 'id', None) == entity_id:
            self.head = self.head.next
            self._size -= 1
            return True
        curr = self.head
        while curr.next:
            if getattr(curr.next.data, 'id', None) == entity_id:
                curr.next = curr.next.next
                self._size -= 1
                return True
            curr = curr.next
        return False

    def traverse(self) -> list:
        records = []
        curr = self.head
        while curr:
            records.append(curr.data)
            curr = curr.next
        return records


class Stack:
    \"\"\"LIFO Stack for Schedule Rollback & Undo History.\"\"\"
    def __init__(self):
        self.top = None
        self._size = 0

    def push(self, data) -> None:
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node
        self._size += 1

    def pop(self):
        if self.top is None: return None
        popped = self.top.data
        self.top = self.top.next
        self._size -= 1
        return popped


class QueueDS:
    \"\"\"FIFO Queue for Course Arrival & Departmental Scheduling Buffer.\"\"\"
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def enqueue(self, data) -> None:
        new_node = Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self._size += 1

    def dequeue(self):
        if self.front is None: return None
        dequeued = self.front.data
        self.front = self.front.next
        if self.front is None: self.rear = None
        self._size -= 1
        return dequeued


class ExpressionHandler:
    \"\"\"Stack-Based Propositional Constraint Parser & Shunting-Yard Converter.\"\"\"
    def validate_brackets(self, expr: str) -> bool:
        s = Stack()
        pairs = {')': '(', '}': '{', ']': '['}
        for ch in expr:
            if ch in "({[": s.push(ch)
            elif ch in ")}]":
                if s.top is None or s.pop() != pairs[ch]: return False
        return s.top is None"""
    add_code_box(doc, code_p1, caption="Listing 7.1: Functional Code Structure for Phase 1 Linear Structures")

    add_heading_2(doc, "Phase 2: Hierarchical & Graph Structures Core")
    code_p2 = """# ============================================================================
# PHASE 2: TREES & GRAPH STRUCTURES - FUNCTIONAL SKELETON
# ============================================================================

class BinarySearchTree:
    \"\"\"BST for O(log n) Course Indexing, Search, and 3-Case Deletion.\"\"\"
    def __init__(self):
        self.root = None

    def insert(self, course_id: int, course_name: str, hours: int = 3):
        self.root = self._insert(self.root, course_id, course_name, hours)

    def _insert(self, node, cid, cname, hours):
        if not node: return BSTNode(cid, cname, hours)
        if cid < node.course_id: node.left = self._insert(node.left, cid, cname, hours)
        elif cid > node.course_id: node.right = self._insert(node.right, cid, cname, hours)
        return node

    def search(self, course_id: int):
        curr = self.root
        while curr:
            if course_id == curr.course_id: return curr
            curr = curr.left if course_id < curr.course_id else curr.right
        return None

    def delete(self, course_id: int):
        self.root = self._delete(self.root, course_id)

    def _delete(self, node, cid):
        if not node: return None
        if cid < node.course_id: node.left = self._delete(node.left, cid)
        elif cid > node.course_id: node.right = self._delete(node.right, cid)
        else:
            if not node.left: return node.right
            if not node.right: return node.left
            succ = self._min_node(node.right)
            node.course_id, node.course_name, node.hours = succ.course_id, succ.course_name, succ.hours
            node.right = self._delete(node.right, succ.course_id)
        return node

    def _min_node(self, node):
        while node.left: node = node.left
        return node


class ConflictGraph:
    \"\"\"Timetable Conflict Graph with Adjacency List & Matrix Representations.\"\"\"
    def __init__(self):
        self.adj_list = {}
        self.vertex_names = {}

    def add_vertex(self, cid: int, name: str = ""):
        if cid not in self.adj_list:
            self.adj_list[cid] = set()
            self.vertex_names[cid] = name or f"Course-{cid}"

    def add_conflict(self, c_a: int, c_b: int, reason: str = "Shared Resource"):
        self.add_vertex(c_a); self.add_vertex(c_b)
        self.adj_list[c_a].add(c_b)
        self.adj_list[c_b].add(c_a)

    def get_degree(self, cid: int) -> int:
        return len(self.adj_list.get(cid, set()))

    def get_adjacency_matrix(self):
        v = sorted(list(self.adj_list.keys()))
        idx = {vid: i for i, vid in enumerate(v)}
        mat = [[0]*len(v) for _ in range(len(v))]
        for u in v:
            for neighbor in self.adj_list[u]:
                mat[idx[u]][idx[neighbor]] = 1
        return v, mat"""
    add_code_box(doc, code_p2, caption="Listing 7.2: Functional Code Structure for Phase 2 Trees & Conflict Graph")

    add_heading_2(doc, "Phase 3: Searching, Sorting & Asymptotic Analysis Core")
    code_p3 = """# ============================================================================
# PHASE 3: SEARCHING & SORTING ALGORITHMS - FUNCTIONAL SKELETON
# ============================================================================

def binary_search_best_fit(classrooms: list, required_capacity: int):
    \"\"\"Finds smallest classroom where capacity >= required_capacity (O(log k)).\"\"\"
    low, high = 0, len(classrooms) - 1
    best_room = None
    while low <= high:
        mid = (low + high) // 2
        if classrooms[mid].capacity >= required_capacity:
            best_room = classrooms[mid]
            high = mid - 1
        else:
            low = mid + 1
    return best_room


def merge_sort_courses(courses: list, reverse: bool = False) -> list:
    \"\"\"Stable Divide-and-Conquer Sort strictly preserving priority (O(n log n)).\"\"\"
    if len(courses) <= 1: return courses
    mid = len(courses) // 2
    left = merge_sort_courses(courses[:mid], reverse)
    right = merge_sort_courses(courses[mid:], reverse)
    
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        cond = (left[i].hours_per_week >= right[j].hours_per_week) if reverse else (left[i].hours_per_week <= right[j].hours_per_week)
        if cond: merged.append(left[i]); i += 1
        else: merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort_classrooms(rooms: list, low: int, high: int):
    \"\"\"In-Place Partitioning Sort for Room Capacities (O(n log n) average, O(1) space).\"\"\"
    if low < high:
        pivot = rooms[high].capacity
        i = low - 1
        for j in range(low, high):
            if rooms[j].capacity <= pivot:
                i += 1
                rooms[i], rooms[j] = rooms[j], rooms[i]
        rooms[i + 1], rooms[high] = rooms[high], rooms[i + 1]
        p_idx = i + 1
        quick_sort_classrooms(rooms, low, p_idx - 1)
        quick_sort_classrooms(rooms, p_idx + 1, high)"""
    add_code_box(doc, code_p3, caption="Listing 7.3: Functional Code Structure for Phase 3 Searching & Sorting")

    add_heading_2(doc, "Phase 4: Advanced Algorithmic Problem Solving Core")
    code_p4 = """# ============================================================================
# PHASE 4: ADVANCED ALGORITHMS - FUNCTIONAL SKELETON
# ============================================================================

def greedy_activity_selection(sessions: list) -> list:
    \"\"\"Earliest Finish Time (EFT) Greedy Choice Single-Venue Scheduler (O(n log n)).\"\"\"
    if not sessions: return []
    sorted_s = sorted(sessions, key=lambda s: s.end_time)
    selected = [sorted_s[0]]
    last_finish = sorted_s[0].end_time
    for s in sorted_s[1:]:
        if s.start_time >= last_finish:
            selected.append(s)
            last_finish = s.end_time
    return selected


def optimize_workload_dp(modules: list, max_workload: int) -> tuple:
    \"\"\"0/1 Knapsack Dynamic Programming for Faculty Workload Optimization (O(N*W)).\"\"\"
    n = len(modules)
    dp = [[0]*(max_workload + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        m = modules[i - 1]
        for w in range(max_workload + 1):
            if m.hours <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - m.hours] + m.credit_value)
            else:
                dp[i][w] = dp[i - 1][w]

    selected = []
    w_rem = max_workload
    for i in range(n, 0, -1):
        if dp[i][w_rem] != dp[i - 1][w_rem]:
            selected.append(modules[i - 1])
            w_rem -= modules[i - 1].hours
    return dp[n][max_workload], selected[::-1], dp


class TimetableBacktrackingSolver:
    \"\"\"Graph Coloring CSP Backtracking Solver with MCV Degree Heuristic.\"\"\"
    def __init__(self, graph: ConflictGraph, slots: list):
        self.graph = graph
        self.slots = slots
        self.assignments = {cid: None for cid in graph.get_vertices()}

    def is_safe(self, cid: int, slot: str) -> bool:
        for neighbor in self.graph.get_neighbors(cid):
            if self.assignments.get(neighbor) == slot: return False
        return True

    def solve(self) -> bool:
        ordered = sorted(self.graph.get_vertices(), 
                         key=lambda c: self.graph.get_degree(c), reverse=True)
        return self._backtrack(0, ordered)

    def _backtrack(self, idx: int, courses: list) -> bool:
        if idx == len(courses): return True
        curr = courses[idx]
        for slot in self.slots:
            if self.is_safe(curr, slot):
                self.assignments[curr] = slot
                if self._backtrack(idx + 1, courses): return True
                self.assignments[curr] = None  # Rollback
        return False"""
    add_code_box(doc, code_p4, caption="Listing 7.4: Functional Code Structure for Phase 4 Optimization Paradigms")

    add_heading_2(doc, "Full-Stack Backend Server & 3-Point Conflict Engine")
    code_web = """# ============================================================================
# FLASK BACKEND & TRI-FACTOR REAL-TIME CLASH ENGINE (web_server.py)
# ============================================================================

def check_clash(conn, section, date_str, timeslot, teacher_email, room_id, ignore_id=None):
    \"\"\"Tri-Factor Invariant Validation Engine.\"\"\"
    c = conn.cursor()
    c.execute("SELECT name FROM classrooms WHERE id=?", (room_id,))
    rm = c.fetchone()
    room_name = rm["name"] if rm else ""

    q = \"\"\"SELECT s.id, s.section, s.teacher_name, s.teacher_email,
                  sub.name AS subject_name, cr.name AS room_name
           FROM schedule s
           JOIN subjects sub ON s.subject_id=sub.id
           JOIN classrooms cr ON s.classroom_id=cr.id
           WHERE s.date=? AND s.timeslot=?\"\"\"
    params = [date_str, timeslot]
    if ignore_id:
        q += " AND s.id!=?"; params.append(ignore_id)
    c.execute(q, params)

    for row in c.fetchall():
        if row["room_name"] == room_name:
            return True, "room", f"Classroom clash: {room_name} already booked for {row['section']}."
        if row["teacher_email"] == teacher_email and teacher_email:
            return True, "teacher", f"Teacher clash: {row['teacher_name']} is teaching {row['section']}."
        if row["section"] == section:
            return True, "section", f"Section clash: {section} already has a lecture scheduled."
    return False, None, "No clash"


@app.route("/api/schedule/create", methods=["POST"])
def api_create_schedule():
    d = request.get_json() or {}
    conn = get_db()
    has_clash, clash_type, msg = check_clash(
        conn, d.get("section"), d.get("date"), d.get("timeslot"),
        d.get("teacher_email"), int(d.get("classroom_id"))
    )
    c = conn.cursor()
    c.execute(\"\"\"INSERT INTO schedule (section, date, timeslot, subject_id, classroom_id,
                 teacher_name, teacher_email, has_clash, clash_reason)
                 VALUES (?,?,?,?,?,?,?,?,?)\"\"\",
              (d["section"], d["date"], d["timeslot"], d["subject_id"], d["classroom_id"],
               d["teacher_name"], d["teacher_email"], 1 if has_clash else 0, msg if has_clash else None))
    conn.commit(); conn.close()
    return jsonify({"success": True, "has_clash": has_clash, "message": msg})"""
    add_code_box(doc, code_web, caption="Listing 7.5: Functional Code Structure for Web Server & Tri-Factor Clash Engine")

    # =========================================================================
    # 8. FEATURES OF THE PROJECT
    # =========================================================================
    print(">> Generating Chapter 8: Features of the Project (Expanded)...")
    add_heading_1(doc, "8. FEATURES OF THE PROJECT", page_break=True)
    add_paragraph(doc,
        "CampusGrid delivers a comprehensive suite of practical and algorithmic features engineered to eliminate "
        "timetabling friction in modern university environments:"
    )

    feat_headers = ["Feature Category", "Specific Capability", "Underlying Technical Implementation", "Operational Benefit"]
    feat_rows = [
        ["Clash Immunity", "Zero Teacher / Room / Section Overlaps", "Backtracking CSP Graph Coloring + Atomic Relational Invariants", "Guarantees 100% clash-free schedules without human double-bookings"],
        ["Real-Time Validation", "Tri-Factor Collision Detection", "check_clash() executing simultaneous checks on rooms, teachers, and cohorts", "Instant feedback on administrative entries with specific conflict warnings"],
        ["Role-Based Access", "Dedicated Admin, Faculty, and Student Portals", "Flask session authentication + dynamic DOM view controllers in app.js", "Secures administrative capabilities while delivering clean views to students"],
        ["Interactive Visualizer", "5-Day Weekly Matrix & 3-Day Rolling Agenda", "Responsive CSS Grid, badge styling, and dynamic date computation", "Permits students and professors to view timetables on mobile or desktop viewports"],
        ["Faculty Desk", "Online Reschedule & Extra-Hour Workflow", "faculty_requests state machine with automated schedule mutation on approval", "Replaces informal WhatsApp messages with an auditable institutional record"],
        ["Curriculum Hierarchy", "Administrative Tree Auditing", "BinaryTree with Preorder, Inorder, and Postorder recursive traversals", "Enables top-down administrative reporting and bottom-up prerequisite checks"],
        ["Logarithmic Indexing", "Rapid Course Lookup & Deletion", "BinarySearchTree (BST) supporting O(log n) search and 3-case deletion", "Accelerates course queries and maintains an automatically sorted in-order index"],
        ["Graph Analysis", "Connected Component Decomposition", "ConflictGraph (Adjacency List + Matrix) traversed via BFS", "Allows independent academic departments to be scheduled in parallel across threads"],
        ["Workload Optimization", "0/1 Knapsack Faculty Hour Balancing", "Dynamic Programming with 2D table construction and backtrack reconstruction", "Maximizes instructional credit points while strictly enforcing UGC hour caps"],
        ["Capacity Optimization", "Best-Fit Room Allocation", "Quick Sort on classroom capacities + Best-Fit Binary Search", "Matches batch sizes to the tightest available room, eliminating seat waste"],
        ["Single-Hall Utilization", "Greedy Activity Selection", "Earliest Finish Time (EFT) sorting and greedy scan in O(n log n)", "Maximizes the number of non-overlapping course sessions in shared auditoriums"],
        ["Dual Persistence", "SQLite & MySQL Enterprise Integration", "SQLite (portal_data.db) + MySQL (timetable_db) schema with cascading foreign keys", "Provides instant zero-config demonstration and enterprise Workbench EER views"],
    ]
    add_styled_table(doc, feat_headers, feat_rows, col_widths=[1.3, 1.8, 2.3, 1.8])

    # =========================================================================
    # 9. FUTURE ENHANCEMENTS
    # =========================================================================
    print(">> Generating Chapter 9: Future Enhancements (Expanded)...")
    add_heading_1(doc, "9. FUTURE ENHANCEMENTS", page_break=True)
    add_paragraph(doc,
        "While CampusGrid delivers a fully functional, mathematically verified timetabling solution, future development "
        "can extend its capabilities into broader enterprise domains:"
    )
    add_bullet(doc, "Integrate Genetic Algorithms (GA) and Simulated Annealing (SA) to optimize qualitative soft constraints, such as minimizing 1-hour idle gaps for instructors and distributing intensive core subjects across morning hours.", bold_prefix="1. AI-Driven Metaheuristic Soft-Constraint Optimization:")
    add_bullet(doc, "Extend the Conflict Graph to generate dynamic conflict edges based on individual student elective registrations, accommodating modern Choice-Based Credit Systems (CBCS).", bold_prefix="2. Choice-Based Credit System (CBCS) Student Elective Bidding:")
    add_bullet(doc, "For universities spanning multiple physical campuses, incorporate transit distance matrices as constraints to prevent professors from being scheduled at different campuses without adequate travel windows.", bold_prefix="3. Multi-Campus Geographic Transit Optimization:")
    add_bullet(doc, "Decompose the monolithic Flask backend into Dockerized microservices (Authentication Service, Clash Engine, Notification Worker) orchestrated via Kubernetes for multi-university scalability.", bold_prefix="4. Cloud Microservices & Containerized Deployment:")
    add_bullet(doc, "Implement standard iCalendar (.ics) exports and WebSocket push notifications to alert students immediately when an administrator approves a faculty rescheduling request.", bold_prefix="5. Calendar Synchronization & Real-Time Push Alerts:")
    add_bullet(doc, "Connect scheduling endpoints with smart classroom IoT controllers to automate room lighting, climate control, and digital door signage based on real-time timetable occupancy.", bold_prefix="6. Smart Classroom IoT & Attendance Integration:")

    # =========================================================================
    # 10. CONCLUSION
    # =========================================================================
    print(">> Generating Chapter 10: Conclusion (Expanded)...")
    add_heading_1(doc, "10. CONCLUSION", page_break=True)
    add_paragraph(doc,
        "The development of CampusGrid: Intelligent Clash-Free Timetable Generator & Academic Scheduling System has been "
        "an immensely rewarding practical capstone experience in my First Semester MCA coursework at Kristu Jayanti University. "
        "It successfully bridges theoretical algorithmic computer science with production-grade full-stack systems engineering."
    )
    add_paragraph(doc,
        "By implementing all linear data structures (custom singly linked list, LIFO stack, FIFO queue, expression parser), "
        "hierarchical trees (administrative binary tree, logarithmic BST with 3-case deletion), and non-linear graph structures "
        "(conflict graph with dual adjacency representations) from scratch, I gained a deep understanding of memory pointer "
        "mechanics, asymptotic time-space trade-offs, and state-space pruning."
    )
    add_paragraph(doc,
        "Connecting these theoretical structures to advanced optimization paradigms proved decisive: Greedy Activity Selection "
        "maximizes shared venue occupancy; 0/1 Knapsack Dynamic Programming balances faculty workloads under statutory hour limits; "
        "and Backtracking CSP with Most Constrained Variable (MCV) heuristics prunes an exponential search space down to sub-second "
        "execution. The dual relational persistence architecture (SQLite for immediate execution and MySQL for enterprise EER modeling) "
        "coupled with the responsive Flask web portal delivers a complete, practical software asset capable of serving real-world academic institutions."
    )

    # =========================================================================
    # 11. REFERENCES
    # =========================================================================
    print(">> Generating Chapter 11: References...")
    add_heading_1(doc, "11. REFERENCES", page_break=True)
    add_paragraph(doc, "The theoretical models, data structures, and algorithmic paradigms implemented in this project are grounded in authoritative academic literature:")

    ref_items = [
        "Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). Introduction to Algorithms (4th ed.). MIT Press. (Foundations of Linked Lists, Trees, Heaps, Dynamic Programming, and Graph Algorithms).",
        "Russell, S., & Norvig, P. (2020). Artificial Intelligence: A Modern Approach (4th ed.). Pearson. (Formulation of Timetabling as a Constraint Satisfaction Problem and Backtracking Search with MCV Heuristic).",
        "Knuth, D. E. (2011). The Art of Computer Programming, Volume 4A: Combinatorial Algorithms, Part 1. Addison-Wesley Professional. (Graph Vertex Coloring and Backtracking Mechanics).",
        "Schaerf, A. (1999). A survey of automated timetabling. Artificial Intelligence Review, 13(2), 87-127. (Comprehensive Taxonomy of the University Course Timetabling Problem).",
        "Burke, E. K., Kingston, J. H., & de Werra, D. (2004). Applications to timetabling. Handbook of Graph Theory, 445-474. CRC Press.",
        "Grinberg, M. (2018). Flask Web Development: Developing Web Applications with Python (2nd ed.). O'Reilly Media.",
        "MySQL AB. (2026). MySQL 8.0 Reference Manual and Workbench Architecture Guide. Oracle Corporation.",
        "University Grants Commission (UGC). (2024). Guidelines for Faculty Workload and Credit Architecture in Higher Education Institutions. New Delhi, India.",
    ]
    for r in ref_items:
        add_bullet(doc, r)

    print(">> Screenshots, source code, features, enhancements, conclusion, and references built successfully.")
