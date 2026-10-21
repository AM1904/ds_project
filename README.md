# 📅 Intelligent Clash-Free Timetable Generator & Academic Scheduling System

An end-to-end Data Structures and Algorithms capstone project that solves university course and classroom scheduling without faculty, room, or student cohort clashes. It features an algorithmic engine across 4 implementation phases, dual database support (SQLite persistent storage + MySQL Workbench schema), and a full-stack interactive Web Portal with role-based access for Admins, Faculty, and Students.

---

## 🌟 Highlights & Features

- **Algorithmic Engine**: Implements custom data structures from scratch (Linked Lists, Stacks, Queues, BST, Conflict Graphs) and algorithms (Merge/Quick Sort, Binary Search, Greedy Activity Selection, 0/1 Knapsack DP, and CSP Backtracking).
- **Interactive Web Portal**: Built using Flask and Vanilla HTML5/CSS/JavaScript with glassmorphic modern UI and responsive layouts.
- **3-Point Clash Detection Engine**: Real-time validation preventing Classroom clashes, Teacher clashes, and Section clashes.
- **Faculty Reschedule & Extra-Hour Workflow**: Faculty can request timeslot or classroom changes; once an Admin approves a request, changes instantly propagate across all student and faculty timetables.
- **Dual Database Architecture**: 
  - **SQLite (`portal_data.db`)**: Out-of-the-box persistent storage for web application users, schedules, and requests.
  - **MySQL (`database/`)**: Full DDL schema, views, relational constraints, and queries for MySQL Workbench integration and ER diagrams.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────┐
│     Frontend (SPA: Web UI)      │  HTML5 + Modern CSS + JavaScript
│  (Admin, Faculty & Student)     │  Subject Pickers, Clash Alerts, Requests
└────────────────▲────────────────┘
                 │ REST API (JSON)
┌────────────────▼────────────────┐
│      Backend Server (Flask)     │  web_server.py (Python)
│  (Auth, Clash Engine, APIs)     │  3-Point Clash Detection, RBAC
└────────────────▲────────────────┘
                 │ Database Driver
┌────────────────▼────────────────┐
│      Database Layer             │  SQLite (portal_data.db)
│   (Relational Persistence)      │  Users, Subjects, Classrooms, Schedule, Requests
└─────────────────────────────────┘
```

---

## 📂 Project Structure

```
DS_Project/
├── phase1/                       # Phase 1: Linear Data Structures
│   ├── node.py                   # Generic Linked Node
│   ├── data_models.py            # Teacher, Course, Classroom, TimeSlot entities
│   ├── linked_list.py            # Custom Singly Linked List (insert, delete, search, traverse)
│   ├── stack.py                  # LIFO Stack for schedule rollback / undo history
│   ├── queue_ds.py               # FIFO Queue for course scheduling pipeline
│   ├── expression_handler.py     # Stack-based bracket validator for constraint rules
│   └── main.py                   # Phase 1 CLI Demo
├── phase2/                       # Phase 2: Hierarchical and Graph Structures
│   ├── binary_tree.py            # Institutional curriculum/department tree
│   ├── bst.py                    # Binary Search Tree for O(log n) Course ID indexing
│   ├── graph.py                  # Conflict Graph (Adjacency List & Matrix)
│   ├── traversals.py             # BFS (connected components) & DFS (prerequisites)
│   └── main.py                   # Phase 2 CLI Demo
├── phase3/                       # Phase 3: Searching and Sorting Operations
│   ├── searching.py              # Linear Search, Binary Search, Best-Fit Room Search
│   ├── sorting.py                # Merge Sort (stable), Quick Sort (in-place)
│   ├── analysis.py               # Empirical benchmarking & Big-O comparison
│   ├── workflow.py               # Optimal room-fit and course priority workflow
│   └── main.py                   # Phase 3 CLI Demo
├── phase4/                       # Phase 4: Basic Algorithmic Problem Solving
│   ├── greedy_scheduler.py       # Greedy Interval Scheduling (Earliest Finish Time)
│   ├── dp_workload.py            # 0/1 Knapsack DP Faculty Workload Optimizer
│   ├── backtracking_timetable.py # Graph-Coloring CSP Backtracking Solver
│   ├── pipeline.py               # Integrated End-to-End Algorithmic Orchestrator
│   └── main.py                   # Phase 4 CLI Demo
├── database/                     # MySQL Relational Backend
│   ├── schema.sql                # DDL Table Definitions, Foreign Keys & Views
│   ├── seed_data.sql             # Realistic Academic Seed Data
│   ├── queries.sql               # Clash-Detection & Analytical Queries
│   ├── db_manager.py             # Python Database Access Layer & DS Bridges
│   └── setup_db.py               # Database Verification & Setup Script
├── web/                          # Web Application Frontend
│   ├── index.html                # Responsive Single Page Application
│   ├── styles.css                # Custom CSS Design System
│   └── app.js                    # UI logic, REST API calls, dynamic views
├── portal_data.db                # SQLite database with pre-seeded accounts & schedule
├── web_server.py                 # Flask REST API backend & static file server
├── run_web.py                    # One-click web portal launcher
├── run_project.py                # Master CLI Control Panel for all phases
└── requirements.txt              # Project dependencies
```

---

## 🔬 Four-Phase Technical Breakdown

| Phase | Core Concepts | What Was Built | Why Chosen |
|---|---|---|---|
| **Phase 1: Linear DS** | Linked List, Stack, Queue | Custom `LinkedList`, `Stack`, `Queue`, bracket validator | Linked List handles dynamic allocations without contiguous resizing; Stack provides LIFO for undo history; Queue guarantees fair FIFO course scheduling. |
| **Phase 2: Trees & Graphs** | Binary Tree, BST, Graph (BFS/DFS) | Institutional hierarchy tree, Course BST, Conflict Graph | BST reduces course search from $O(N)$ to $O(\log N)$; Adjacency List graph models pairwise resource clashes; BFS isolates independent schedule components. |
| **Phase 3: Search & Sort** | Merge Sort, Quick Sort, Binary Search | Best-fit classroom allocation, priority sorter, benchmarking | Merge Sort is **stable** (preserves chronological order); Quick Sort is in-place for classroom rankings; Best-fit binary search prevents seat waste. |
| **Phase 4: Algorithms** | Greedy, Dynamic Programming, Backtracking | Activity selection, Knapsack faculty workload, CSP graph-coloring solver | Greedy optimizes single-room utilization in $O(N \log N)$; DP resolves discrete credit limits optimally; Backtracking systematically prunes clashes to yield 100% valid schedules. |

---

## 🌐 Web Timetable Portal

### Default Accounts & Credentials

The database is pre-seeded with an Administrator and 6 faculty accounts (one for each department subject):

| Role | Name | Email | Password | Assigned Subject |
|---|---|---|---|---|
| **Admin** | Administrator | `admin@college.edu` | `admin123` | *Full Administrative Access* |
| **Faculty** | Dr. Ananya Sharma | `ananya@college.edu` | `faculty123` | MCA-201: Data Structures & Algorithms |
| **Faculty** | Prof. Ravi Kumar | `ravi.k@college.edu` | `faculty123` | MCA-202: Operating Systems |
| **Faculty** | Ms. Priya Nair | `priya.nair@college.edu` | `faculty123` | MCA-203: Database Management Systems |
| **Faculty** | Mr. Arjun Mehta | `arjun.m@college.edu` | `faculty123` | MCA-204: Computer Networks |
| **Faculty** | Dr. Sunita Rao | `sunita.rao@college.edu` | `faculty123` | MCA-205: Machine Learning & AI |
| **Faculty** | Prof. Vikram Joshi | `vikram.j@college.edu` | `faculty123` | MCA-206: Web Technologies & Cloud |

---

## 🚀 Quick Start Guide

### 1. Installation
Clone the repository and install the dependencies:
```bash
git clone https://github.com/AM1904/ds_project.git
cd ds_project
pip install -r requirements.txt
```

### 2. Launch the Web Timetable Portal
Start the web server:
```bash
python run_web.py
```
Or directly:
```bash
python web_server.py
```
Open **[http://localhost:5050](http://localhost:5050)** in your browser.

### 3. Run the Algorithmic CLI Demos
To run the interactive CLI control panel:
```bash
python run_project.py
```
To run all 4 phases sequentially in automated verification mode:
```bash
python run_project.py --all
```

---

## 🗄️ MySQL Workbench Integration (Optional)

If you wish to view the relational schema and EER diagram in MySQL Workbench:
1. Ensure MySQL server is running on `localhost:3306`.
2. Run the one-click initialization script:
   ```bash
   python database/setup_db.py
   ```
3. In MySQL Workbench, open `database/schema.sql`, `database/seed_data.sql`, and `database/queries.sql`.
4. Go to **Database $\rightarrow$ Reverse Engineer...** to view the interactive EER Diagram.

---

## 👥 Authors & Acknowledgments

- **Author**: AM1904
- **Repository**: [https://github.com/AM1904/ds_project.git](https://github.com/AM1904/ds_project.git)
- Built for Academic Review & Data Structures & Algorithms coursework.
