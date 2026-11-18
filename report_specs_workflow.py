# -*- coding: utf-8 -*-
"""
Module 2 (Expanded): Software Specifications and Project Workflows for Ananya Ann Mathew (26MCAC07).
Contains High-Level Architecture, Folder Structure, Detailed Database Schema Specifications,
User Roles, and complete step-by-step Operational Workflows with REST API contracts.
"""
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_specs_and_workflow(doc, helpers):
    add_heading_1 = helpers['add_heading_1']
    add_heading_2 = helpers['add_heading_2']
    add_heading_3 = helpers['add_heading_3']
    add_paragraph = helpers['add_paragraph']
    add_bullet = helpers['add_bullet']
    add_styled_table = helpers['add_styled_table']
    add_code_box = helpers['add_code_box']

    # =========================================================================
    # 5. SOFTWARE SPECIFICATIONS
    # =========================================================================
    print(">> Generating Chapter 5: Software Specifications (Expanded)...")
    add_heading_1(doc, "5. SOFTWARE SPECIFICATIONS", page_break=True)
    add_paragraph(doc,
        "The engineering design of CampusGrid balances algorithmic rigor (custom scratch data structures) with "
        "production usability (a modern, responsive web application). Below are the hardware configurations, runtime "
        "frameworks, high-level architecture, directory layout, database schema specifications, and user authorization tiers."
    )

    add_heading_2(doc, "Hardware Specifications")
    add_paragraph(doc, "The system was implemented, profiled, and benchmarked on a standard academic workstation:")
    hw_headers = ["Subsystem", "Development Workstation Configuration", "Minimal Target Requirement"]
    hw_rows = [
        ["Processor (CPU)", "11th Gen Intel® Core™ i5-1135G7 @ 2.40 GHz (4 Cores, 8 Threads)", "Dual-Core x86_64 or ARM64 @ 1.8 GHz"],
        ["Primary Memory (RAM)", "16.0 GB DDR4 @ 3200 MHz High-Speed Memory", "2.0 GB System Memory"],
        ["Secondary Storage", "512 GB PCIe NVMe M.2 Solid State Drive (SSD)", "250 MB Free Disk Space"],
        ["Display Resolution", "1920 × 1080 Full HD (60 Hz Standard Refresh)", "1366 × 768 WXGA Desktop / Mobile Viewport"],
        ["Network Adapter", "Integrated Gigabit Ethernet & Intel Wi-Fi 6 AX201", "Standard Local Loopback (127.0.0.1) / LAN"],
    ]
    add_styled_table(doc, hw_headers, hw_rows, col_widths=[1.5, 3.2, 2.5])

    add_heading_2(doc, "Software Runtime & Framework Specifications")
    sw_headers = ["Layer / Subsystem", "Technology / Framework", "Version / Standard", "Operational Role"]
    sw_rows = [
        ["Programming Language", "Python", "3.12.x", "Core DSA implementation and Flask backend server"],
        ["Web Microframework", "Flask", "3.0.x (>= 2.0.0)", "RESTful API routes, routing controller, session auth"],
        ["Relational Driver", "PyMySQL", ">= 1.0.0", "Database client for MySQL 8.0 Workbench integration"],
        ["Embedded Database", "SQLite3", "3.42.0 (Standard Lib)", "Local zero-configuration persistent storage (portal_data.db)"],
        ["Enterprise RDBMS", "MySQL Community Server", "8.0.36+", "Relational DDL, foreign key cascading, EER diagrams"],
        ["Frontend Presentation", "Vanilla HTML5 / CSS3 / ES6", "W3C Standards", "Single Page Application (SPA), responsive glassmorphic UI"],
        ["Typography", "Plus Jakarta Sans / Consolas", "Google Fonts / Monospace", "Modern academic styling and code formatting"],
        ["Database Modeling Tool", "MySQL Workbench", "8.0.36 CE", "Interactive EER diagram generation and SQL script testing"],
        ["Code Editor & VCS", "Visual Studio Code / Git", "1.87+ / Git 2.43", "Source development, debugging, and version control"],
    ]
    add_styled_table(doc, sw_headers, sw_rows, col_widths=[1.4, 1.8, 1.6, 2.4])

    add_heading_2(doc, "High-Level Architecture")
    add_paragraph(doc,
        "CampusGrid is organized according to a decoupled Three-Tier Architecture, guaranteeing separation of concerns "
        "between presentation, algorithmic processing, and relational persistence:"
    )
    add_bullet(doc, 
        "A responsive Single Page Application (SPA) providing role-based interfaces for Administrators, Faculty, and Students. "
        "It communicates with the server entirely via asynchronous JSON fetch calls, eliminating full-page browser reloads.",
        bold_prefix="1. Tier 1: Client Presentation Layer (Web SPA):"
    )
    add_bullet(doc,
        "Driven by web_server.py using Python Flask. It serves API routes, executes real-time 3-point clash verification, "
        "enforces session security, and orchestrates the four-phase algorithmic core (custom Linked Lists, Trees, Sorters, "
        "Greedy Selectors, DP Knapsack, and CSP Backtracking).",
        bold_prefix="2. Tier 2: Application & Algorithmic Middleware:"
    )
    add_bullet(doc,
        "A dual-persistence engine. For instant out-of-the-box demonstration, SQLite (portal_data.db) persists live accounts, "
        "schedules, and faculty requests. Concurrently, production MySQL scripts (database/schema.sql, seed_data.sql, queries.sql) "
        "support enterprise deployment and reverse-engineering into Enhanced Entity-Relationship (EER) diagrams in MySQL Workbench.",
        bold_prefix="3. Tier 3: Relational Persistence Layer:"
    )

    add_heading_2(doc, "Folder Structure and Modular Responsibilities")
    add_paragraph(doc,
        "The repository maintains a clean, modular directory structure where each folder corresponds to a discrete "
        "computational phase or architectural tier:"
    )

    folder_tree = """DS_Project/
├── phase1/                    # Phase 1: Linear Data Structures
│   ├── node.py                # Generic pointer-based Node
│   ├── data_models.py         # Domain models (Teacher, Course, Classroom, TimeSlot)
│   ├── linked_list.py         # Custom Singly Linked List (insert, delete, search, traverse)
│   ├── stack.py               # LIFO Stack for schedule mutation rollback / undo
│   ├── queue_ds.py            # FIFO Queue for departmental course scheduling buffer
│   ├── expression_handler.py  # Stack-based bracket & propositional constraint parser
│   └── main.py                # Phase 1 Interactive Terminal Demo
├── phase2/                    # Phase 2: Hierarchical and Graph Structures
│   ├── binary_tree.py         # Institutional curriculum tree (Pre/In/Postorder traversals)
│   ├── bst.py                 # Binary Search Tree for O(log n) Course ID indexing & deletion
│   ├── graph.py               # Conflict Graph (Adjacency List & 2D Adjacency Matrix)
│   ├── traversals.py          # BFS (connected components) & DFS (prerequisite cycles)
│   └── main.py                # Phase 2 Interactive Terminal Demo
├── phase3/                    # Phase 3: Searching, Sorting & Asymptotic Analysis
│   ├── searching.py           # Linear Search, Binary Search, Best-Fit Room Search
│   ├── sorting.py             # Insertion Sort, Merge Sort (stable), Quick Sort (in-place)
│   ├── analysis.py            # Empirical benchmarking suite (N=10 to 250) & Big-O matrix
│   ├── workflow.py            # Course prioritization & Best-Fit venue allocation workflow
│   └── main.py                # Phase 3 Interactive Terminal Demo
├── phase4/                    # Phase 4: Basic Algorithmic Problem Solving
│   ├── greedy_scheduler.py    # Greedy Activity Selection (EFT) & Interval Partitioning
│   ├── dp_workload.py         # 0/1 Knapsack DP Faculty Workload Optimizer
│   ├── backtracking_timetable.py # Graph-Coloring CSP Backtracking Solver (MCV heuristic)
│   ├── pipeline.py            # Integrated End-to-End Algorithmic Orchestrator
│   └── main.py                # Phase 4 Interactive Terminal Demo
├── database/                  # Enterprise Relational Database Module
│   ├── schema.sql             # MySQL DDL Tables, Constraints, Cascades & Relational Views
│   ├── seed_data.sql          # Realistic Academic Seed Data (Teachers, Rooms, Slots, Conflicts)
│   ├── queries.sql            # Analytical & Zero-Clash Self-Join Verification Queries
│   ├── db_manager.py          # PyMySQL Access Layer & Custom Data Structure Bridges
│   └── setup_db.py            # Automated Database Initialization & Verification Script
├── web/                       # Full-Stack Web Application Frontend
│   ├── index.html             # Responsive Single Page Application structure
│   ├── styles.css             # Custom CSS design system, glassmorphism, responsive tables
│   └── app.js                 # Frontend state controller, REST API calls, dynamic views
├── portal_data.db             # Pre-seeded SQLite database for zero-config web launch
├── web_server.py              # Flask REST backend & Real-Time 3-Point Conflict Engine
├── run_web.py                 # One-click web portal launcher (starts Flask & opens browser)
├── run_project.py             # Master CLI control panel for terminal demonstrations
└── requirements.txt           # Project dependencies (flask, pymysql)"""
    add_code_box(doc, folder_tree, caption="Figure 5.1: Complete CampusGrid Repository Architecture & File Responsibilities")

    add_heading_2(doc, "Relational Database Schema Design (MySQL & SQLite)")
    add_paragraph(doc,
        "The relational database schema is normalized to Third Normal Form (3NF) to eliminate data redundancy while "
        "enforcing referential integrity via foreign key constraints with cascading deletes (`ON DELETE CASCADE`):"
    )

    t1_headers = ["Column Name", "Data Type", "Constraint", "Description"]
    t1_rows = [
        ["teacher_id", "INT", "PRIMARY KEY", "Unique numeric identifier for faculty member"],
        ["name", "VARCHAR(100)", "NOT NULL", "Full official name (e.g. Dr. Ananya Sharma)"],
        ["subject", "VARCHAR(100)", "NOT NULL", "Core specialization subject domain"],
        ["max_hours", "INT", "NOT NULL DEFAULT 16", "Statutory maximum weekly lecture hours"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Audit timestamp of record creation"],
    ]
    add_styled_table(doc, t1_headers, t1_rows, col_widths=[1.5, 1.5, 1.8, 2.4])

    t2_headers = ["Column Name", "Data Type", "Constraint", "Description"]
    t2_rows = [
        ["room_id", "INT", "PRIMARY KEY", "Unique physical room identifier"],
        ["room_number", "VARCHAR(50)", "NOT NULL UNIQUE", "Classroom label (e.g. Room A-101, Systems Lab-1)"],
        ["capacity", "INT", "NOT NULL", "Seating capacity for enrolled students"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Audit timestamp of venue addition"],
    ]
    add_styled_table(doc, t2_headers, t2_rows, col_widths=[1.5, 1.5, 1.8, 2.4])

    t3_headers = ["Column Name", "Data Type", "Constraint", "Description"]
    t3_rows = [
        ["slot_id", "INT", "PRIMARY KEY", "Unique timeslot identifier"],
        ["day", "VARCHAR(20)", "NOT NULL", "Day of the week (Monday - Friday)"],
        ["start_time", "VARCHAR(10)", "NOT NULL", "Starting time window (e.g. 09:00 AM)"],
        ["end_time", "VARCHAR(10)", "NOT NULL", "Ending time window (e.g. 10:00 AM)"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp of timeslot generation"],
    ]
    add_styled_table(doc, t3_headers, t3_rows, col_widths=[1.5, 1.5, 1.8, 2.4])

    t4_headers = ["Column Name", "Data Type", "Constraint", "Description"]
    t4_rows = [
        ["course_id", "INT", "PRIMARY KEY", "Unique course offering identifier"],
        ["name", "VARCHAR(100)", "NOT NULL", "Course title (e.g. MCA-201: DSA)"],
        ["teacher_id", "INT", "NOT NULL, FOREIGN KEY", "References teachers(teacher_id) ON DELETE CASCADE"],
        ["hours_per_week", "INT", "NOT NULL DEFAULT 3", "Required weekly instructional contact hours"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp of course creation"],
    ]
    add_styled_table(doc, t4_headers, t4_rows, col_widths=[1.5, 1.5, 1.8, 2.4])

    t5_headers = ["Column Name", "Data Type", "Constraint", "Description"]
    t5_rows = [
        ["conflict_id", "INT AUTO_INCREMENT", "PRIMARY KEY", "Unique conflict record identifier"],
        ["course_id_1", "INT", "NOT NULL, FOREIGN KEY", "First course in conflict pair (references courses)"],
        ["course_id_2", "INT", "NOT NULL, FOREIGN KEY", "Second course in conflict pair (references courses)"],
        ["reason", "VARCHAR(255)", "NOT NULL", "Reason for clash (Shared Faculty / Shared Cohort)"],
        ["created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Audit timestamp of edge creation"],
    ]
    add_styled_table(doc, t5_headers, t5_rows, col_widths=[1.5, 1.5, 1.8, 2.4])

    t6_headers = ["Column Name", "Data Type", "Constraint", "Description"]
    t6_rows = [
        ["assignment_id", "INT AUTO_INCREMENT", "PRIMARY KEY", "Unique scheduled assignment identifier"],
        ["course_id", "INT", "NOT NULL, FOREIGN KEY", "References courses(course_id) ON DELETE CASCADE"],
        ["teacher_id", "INT", "NOT NULL, FOREIGN KEY", "References teachers(teacher_id) ON DELETE CASCADE"],
        ["room_id", "INT", "NOT NULL, FOREIGN KEY", "References classrooms(room_id) ON DELETE CASCADE"],
        ["slot_id", "INT", "NOT NULL, FOREIGN KEY", "References timeslots(slot_id) ON DELETE CASCADE"],
        ["is_clash_free", "BOOLEAN", "DEFAULT TRUE", "Flag indicating verified clash immunity"],
        ["generated_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Timestamp of schedule assignment"],
    ]
    add_styled_table(doc, t6_headers, t6_rows, col_widths=[1.5, 1.5, 1.8, 2.4])

    add_heading_2(doc, "Data Model: User Accounts and Role-Based Access Control")
    add_paragraph(doc,
        "The web application enforces Role-Based Access Control (RBAC) across three distinct user categories stored "
        "in the `users` table of `portal_data.db`:"
    )
    user_headers = ["Role", "Typical Account", "Accessible Portals", "Operational Permissions"]
    user_rows = [
        ["Administrator", "admin@college.edu (Dean / HOD)", "Timetable Studio, Faculty Requests Desk, Master Grid", "Full CRUD on schedule, override clash warnings, approve/reject faculty requests, audit workload"],
        ["Faculty", "ananya@college.edu, ravi.k@college.edu, etc.", "Personal Daily Schedule, Weekly Teaching Grid, Request Desk", "View own assigned classes, submit slot rescheduling requests, request extra revision/lab hours"],
        ["Student", "MCA Section Students (e.g. MCA A, MCA B)", "3-Day Rolling Agenda, 5-Day Weekly Section Timetable", "Read-only access to section schedule, view rescheduled class notifications in real time"],
    ]
    add_styled_table(doc, user_headers, user_rows, col_widths=[1.2, 1.8, 2.0, 2.2])

    # =========================================================================
    # 6. WORKFLOW OF THE PROJECT
    # =========================================================================
    print(">> Generating Chapter 6: Project Workflows (Expanded)...")
    add_heading_1(doc, "6. WORKFLOW OF THE PROJECT", page_break=True)
    add_paragraph(doc,
        "The interaction between users, the Flask routing controller, custom algorithmic data structures, and relational "
        "databases is organized into seven core operational workflows:"
    )

    add_heading_2(doc, "1. Registration and Authentication Workflow")
    add_paragraph(doc,
        "When an unauthenticated user navigates to `http://localhost:5050`, the single-page application displays the auth modal. "
        "The user can toggle between 'Sign In' and 'Create Account'. Quick login buttons are provided for instant evaluation as "
        "Student (MCA A / B) or Administrator. Upon form submission:"
    )
    add_bullet(doc, "The frontend serializes user credentials and issues an HTTP POST to `/api/auth/login` or `/api/auth/register`.", bold_prefix="Step 1 (Client):")
    add_bullet(doc, "The Flask controller checks credentials against the `users` table in `portal_data.db`, verifies passwords, and stores the user record in an encrypted HTTP session cookie (`campus_portal_secret_2026`).", bold_prefix="Step 2 (Backend):")
    add_bullet(doc, "Upon receiving a success response, `app.js` updates `currentUser`, hides `authScreen`, unhides `appScreen`, and dynamically renders the navigation tabs permitted for that specific role.", bold_prefix="Step 3 (UI State):")

    add_heading_2(doc, "2. Create, Read, Update, and Delete (CRUD) Timetable Slot Workflow")
    add_paragraph(doc,
        "Administrators construct and modify the master schedule using the Timetable Studio. When creating or editing an entry:"
    )
    add_bullet(doc, "The admin selects the target section, date, timeslot, course subject, classroom venue, and assigned professor.", bold_prefix="• Entry Creation:")
    add_bullet(doc, "Before inserting into SQLite, the backend executes `check_clash()`. If the classroom is already occupied, the professor is teaching elsewhere, or the section has an existing class, a clash flag (`has_clash = 1`) and detailed reason are recorded.", bold_prefix="• Invariant Check:")
    add_bullet(doc, "When editing an existing slot (`PUT /api/schedule/<id>`), `check_clash()` is invoked with `ignore_id = eid` so the entry does not falsely clash with its own previous state.", bold_prefix="• Self-Exclusion:")
    add_bullet(doc, "Clicking the delete icon issues an HTTP DELETE call, instantly removing the record from persistent storage and triggering an asynchronous DOM refresh.", bold_prefix="• Slot Removal:")

    add_heading_2(doc, "3. RESTful API Interface Specification")
    add_paragraph(doc, "The Flask backend exposes resource-oriented endpoints following strict REST conventions:")

    api_headers = ["HTTP Method", "Endpoint URI", "Required Role", "Purpose", "Response Status"]
    api_rows = [
        ["POST", "/api/auth/login", "Public", "Authenticates credentials and establishes session", "200 OK / 401 Unauthorized"],
        ["POST", "/api/auth/register", "Public", "Registers new Student, Faculty, or Admin account", "200 OK / 400 Bad Request"],
        ["GET", "/api/auth/me", "Any", "Validates current session and returns active user profile", "200 OK"],
        ["POST", "/api/auth/logout", "Any", "Terminates session and clears session cookie", "200 OK"],
        ["GET", "/api/schedule", "Any", "Retrieves schedule entries filtered by section and date", "200 OK"],
        ["POST", "/api/schedule/create", "Admin", "Creates schedule slot with real-time 3-point clash check", "200 OK / 400 Bad Request"],
        ["PUT", "/api/schedule/<id>", "Admin", "Updates schedule slot with self-exclusion clash validation", "200 OK / 400 Bad Request"],
        ["DELETE", "/api/schedule/<id>", "Admin", "Deletes schedule slot permanently from storage", "200 OK"],
        ["GET", "/api/weekly-schedule", "Any", "Returns complete 5-day weekly matrix for section/faculty", "200 OK"],
        ["GET", "/api/faculty-schedule", "Faculty", "Returns personalized day/week schedule for logged-in professor", "200 OK"],
        ["GET", "/api/student-schedule", "Student", "Returns 3-day rolling agenda for target cohort section", "200 OK"],
        ["POST", "/api/requests", "Faculty", "Submits slot rescheduling or extra-hour coaching request", "200 OK / 400 Bad Request"],
        ["GET", "/api/requests", "Admin", "Retrieves all pending/resolved faculty requests", "200 OK"],
        ["PUT", "/api/requests/<id>/resolve", "Admin", "Approves/rejects request; mutates live schedule on approval", "200 OK / 404 Not Found"],
    ]
    add_styled_table(doc, api_headers, api_rows, col_widths=[1.1, 2.0, 1.1, 2.1, 1.1])

    add_heading_2(doc, "4. Faculty Reschedule and Extra-Hour Approval State Machine")
    add_paragraph(doc,
        "When an instructor requires a lecture change or wishes to book an extra coaching hour:"
    )
    add_bullet(doc, "The professor submits a request via the Faculty Desk, specifying target date, desired timeslot, preferred room, and mandatory reason. The request is stored in `faculty_requests` with status `pending`.", bold_prefix="1. Submission:")
    add_bullet(doc, "The administrator reviews the pending request in the Faculty Requests Desk. The system runs an automated clash check against the requested timeslot and displays any warnings.", bold_prefix="2. Review & Clash Audit:")
    add_bullet(doc, "If approved, the backend automatically mutates the live `schedule` table—updating existing dates/times for reschedule requests or inserting a new record for extra hours. If rejected, an administrative note is recorded.", bold_prefix="3. Resolution & Mutation:")
    add_bullet(doc, "The student and faculty weekly grids update immediately upon next fetch, ensuring all stakeholders are synchronized without manual notifications.", bold_prefix="4. Propagation:")

    print(">> Software specifications and workflows (expanded) built successfully.")
