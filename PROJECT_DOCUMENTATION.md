# Clash-Free Timetable Generator & Academic Scheduling System
## Complete Phase-by-Phase Technical Breakdown & MySQL Workbench Guide

---

## 1. Project Overview & Architecture

The **Clash-Free Timetable Generator** is an end-to-end Data Structures & Algorithms project designed to automate academic schedule creation without room, faculty, or cohort conflicts.

The project is structured into **four progressive phases** backed by a **MySQL relational database backend**:

```
DS_Project/
├── phase1/                  # Phase 1: Linear Data Structures
│   ├── node.py              # Generic linked node
│   ├── data_models.py       # Domain entities: Teacher, Course, Classroom, TimeSlot
│   ├── linked_list.py       # Custom Singly Linked List (insert, delete, search, traverse)
│   ├── stack.py             # LIFO Stack (slot undo history)
│   ├── queue_ds.py          # FIFO Queue (course scheduling queue)
│   ├── expression_handler.py# Stack-based bracket/constraint validator
│   └── main.py              # Phase 1 Interactive Demo
├── phase2/                  # Phase 2: Hierarchical and Graph Structures
│   ├── binary_tree.py       # Hierarchical curriculum/department tree (In/Pre/Post-order)
│   ├── bst.py               # Binary Search Tree for O(log n) Course ID indexing & search
│   ├── graph.py             # Conflict Graph (Adjacency List & Adjacency Matrix)
│   ├── traversals.py        # BFS & DFS Traversals, Connected Components
│   └── main.py              # Phase 2 Interactive Demo
├── phase3/                  # Phase 3: Searching and Sorting Operations
│   ├── searching.py         # Linear Search, Binary Search, Best-Fit Room Search
│   ├── sorting.py           # Insertion Sort, Merge Sort, Quick Sort
│   ├── analysis.py          # Big-O Conceptual Matrix & Empirical Benchmarking
│   ├── workflow.py          # Priority course sorting & optimal room fit workflow
│   └── main.py              # Phase 3 Interactive Demo
├── phase4/                  # Phase 4: Basic Algorithmic Problem Solving
│   ├── greedy_scheduler.py  # Greedy Activity Selection & Interval Partitioning
│   ├── dp_workload.py       # 0/1 Knapsack DP Faculty Workload Optimizer
│   ├── backtracking_timetable.py # Graph Coloring CSP Backtracking Solver
│   ├── pipeline.py          # Integrated Algorithmic Pipeline Orchestrator
│   └── main.py              # Phase 4 Interactive Demo
├── database/                # MySQL Relational Backend
│   ├── schema.sql           # DDL Table Definitions, Foreign Keys & Views
│   ├── seed_data.sql        # Realistic Academic Seed Data
│   ├── queries.sql          # Workbench Clash-Detection & Analytical Queries
│   ├── db_manager.py        # Python Database Access Layer & DS Bridges
│   └── setup_db.py          # One-Click Database Initialization Script
└── run_project.py           # Master System Control Panel
```

---

## 2. Phase-by-Phase Breakdown & "Why" Rationale

### Phase 1: Linear Data Structures Implementation
#### What was done:
1. **Domain Data Models**: Defined `Teacher`, `Course`, `Classroom`, and `TimeSlot` entities with clean string formatting and equality semantics.
2. **Custom Singly Linked List**: Built `LinkedList` supporting:
   - `insert_at_head`, `insert_at_tail`, `insert_at_position(pos)`
   - `delete_by_id`, `delete_at_position(pos)`
   - `search(id)` and full formatted `traverse()`
3. **Custom Stack (`stack.py`)**: Built a LIFO stack backed by linked nodes implementing `push`, `pop`, `peek`, and `is_empty`. Applied for an **undo assignment history** mechanism.
4. **Custom Queue (`queue_ds.py`)**: Built a FIFO queue implementing `enqueue`, `dequeue`, `front`, and `is_empty`. Applied for **pending course arrival scheduling**.
5. **Expression Handler (`expression_handler.py`)**: Applied the stack to validate bracket balancing in timetable constraint formulas (e.g. `(TeacherA AND (RoomB OR RoomC))`).

#### Why this plan was chosen:
- **Why Linked Lists instead of dynamic arrays/lists?** Linked lists provide $O(1)$ insertions at the head and flexible node-by-node dynamic allocation without reallocation overhead when records are added dynamically during scheduling.
- **Why Stack for Undo History?** The Last-In, First-Out (LIFO) property is mathematically identical to schedule rollback: if an assigned slot causes a conflict, the scheduler must revert the *most recent* decision first.
- **Why Queue for Pending Courses?** Fairness in course processing: courses arrive sequentially and should be serviced in First-In, First-Out (FIFO) arrival order.
- **Why Stack-based Expression Validator?** Bracket validation requires matching closing delimiters with their immediate counterpart on top of the stack, which runs in guaranteed $O(n)$ time.

---

### Phase 2: Hierarchical and Graph Structures
#### What was done:
1. **Binary Tree for Structured Hierarchy (`binary_tree.py`)**: Models the academic hierarchy:
   $$\text{Dean} \rightarrow \text{Departments} \rightarrow \text{Academic Tracks} \rightarrow \text{Modules}$$
2. **Tree Traversals**:
   - **Preorder** ($\text{Root} \rightarrow \text{Left} \rightarrow \text{Right}$): Top-down administrative overview.
   - **Inorder** ($\text{Left} \rightarrow \text{Root} \rightarrow \text{Right}$): Symmetric curriculum audit.
   - **Postorder** ($\text{Left} \rightarrow \text{Right} \rightarrow \text{Root}$): Bottom-up dependency and prerequisite resolution.
3. **Binary Search Tree (BST) (`bst.py`)**:
   - Keys = `course_id`.
   - Supports `insert`, `search`, `delete` (handling 0, 1, and 2 children via in-order successor), `find_min`, `find_max`.
   - In-order traversal yields an automatically sorted list of courses in $O(n)$ time.
4. **Timetable Conflict Graph (`graph.py`)**:
   - Vertices = Courses.
   - Edges = Conflicts (shared faculty, cohorts, or physical equipment).
   - Dual representation: **Adjacency List** and **2D Adjacency Matrix**.
5. **Graph Traversals (`traversals.py`)**:
   - **BFS (Breadth-First Search)**: Explores conflict clusters level-by-level, computes distance from conflicts, and isolates **connected components** (independent timetable subgraphs that can be solved in parallel!).
   - **DFS (Depth-First Search)**: Detects deep dependency chains and circular prerequisites.

#### Why this plan was chosen:
- **Why Binary Search Tree for Course Lookup?** Looking up a course in an unsorted list takes $O(n)$ comparisons. A BST provides $O(\log n)$ average search time and keeps items ordered without needing re-sorting passes.
- **Why Graph for Conflict Representation?** Timetabling is inherently a graph theory problem. Two courses cannot occupy the same timeslot if and only if there is an edge between them.
- **Why Both Adjacency List and Matrix?**
  - Adjacency List is space-efficient ($O(V + E)$) when conflict graphs are sparse.
  - Adjacency Matrix allows instant $O(1)$ edge-check queries (`matrix[u][v] == 1`) during the backtracking phase.
- **Why Connected Components via BFS?** If the graph splits into multiple components, the scheduler can divide the problem and solve each sub-schedule independently, reducing exponential search spaces.

---

### Phase 3: Searching and Sorting Operations
#### What was done:
1. **Searching Algorithms (`searching.py`)**:
   - `linear_search`: $O(n)$ sequential search with comparison counter.
   - `binary_search`: $O(\log n)$ divide-and-conquer search on sorted arrays.
   - `binary_search_best_fit`: Binary search extension that finds the *smallest classroom whose capacity $\ge$ required students*.
2. **Sorting Algorithms (`sorting.py`)**:
   - `insertion_sort`: $O(n^2)$ adaptive, stable, in-place sort.
   - `merge_sort`: $O(n \log n)$ divide-and-conquer, stable sort.
   - `quick_sort`: $O(n \log n)$ average in-place partition sort.
3. **Conceptual & Empirical Analysis (`analysis.py`)**:
   - Theoretical Big-O comparison table across best, average, and worst-case time, space complexity, and stability.
   - Benchmarking suite running comparisons and execution time ($\mu s$) on datasets from $N=10$ to $N=250$.
4. **Project Workflow Application (`workflow.py`)**:
   - Workflow A: Prioritize heavy courses first using descending Merge Sort ($O(n \log n)$).
   - Workflow B: Sort classrooms by capacity via Quick Sort, then allocate rooms using Binary Search Best-Fit to prevent seat waste.

#### Why this plan was chosen:
- **Why Merge Sort for Course Priority?** Merge sort is **stable**; when sorting courses by hours per week, it preserves the original relative order (e.g. course ID or teacher name).
- **Why Quick Sort for Classrooms?** Classroom lists are static during allocation. Quick Sort is in-place ($O(1)$ auxiliary space) and boasts smaller constant factors than Merge Sort.
- **Why Best-Fit Binary Search for Rooms?** Assigning a 100-capacity auditorium to a 20-student class wastes 80 seats. Best-fit finds the tightest fit in $O(\log n)$ comparisons rather than checking all rooms sequentially.

---

### Phase 4: Basic Algorithmic Problem Solving
#### What was done:
1. **Greedy Technique (`greedy_scheduler.py`)**:
   - **Interval Scheduling / Activity Selection**: Selects the maximal number of non-overlapping course sessions in a single room using the **Earliest Finish Time (EFT)** greedy heuristic.
   - **Interval Partitioning**: Computes the minimal number of classrooms required to hold all requested sessions without time clashes.
2. **Dynamic Programming Technique (`dp_workload.py`)**:
   - **0/1 Knapsack Workload Optimizer**: Given a faculty member with maximum weekly hours $W$ and course modules with hours (weight) and curriculum priority (value), computes the maximum possible instructional value without exceeding $W$.
   - Generates the full 2D DP matrix and reconstructs the optimal module set.
3. **Backtracking Technique (`backtracking_timetable.py`)**:
   - **Graph Coloring Constraint Satisfaction Problem (CSP)**:
     - Vertices = Courses.
     - Edges = Conflicts.
     - Colors = TimeSlots ($1..K$).
   - Solves slot assignment recursively with state rollback on dead-ends, guided by the *Most Constrained Variable* heuristic (highest conflict degree first).
4. **Integrated Application Flow (`pipeline.py`)**:
   - Step 1: DP selects feasible course commitments for faculty.
   - Step 2: Conflict Graph is constructed.
   - Step 3: Backtracking assigns clash-free TimeSlots.
   - Step 4: Greedy Best-Fit assigns classrooms per timeslot.
   - Generates the Master Clash-Free Timetable.

#### Why this plan was chosen:
- **Why Greedy for Interval Scheduling?** Activity Selection satisfies the *Greedy Choice Property* and *Optimal Substructure*; sorting by earliest finish time guarantees mathematical optimality in $O(n \log n)$ without needing brute force search.
- **Why Dynamic Programming for Faculty Workload?** Greedy heuristic (e.g. pick highest credit-per-hour ratio) fails for 0/1 knapsack problems due to indivisibility. Dynamic programming explores all overlapping subproblems in pseudo-polynomial $O(N \cdot W)$ time and guarantees the global optimum.
- **Why Backtracking for Timetabling?** Timetabling is NP-Complete (reducible from Graph Vertex Coloring). Backtracking systematically explores the search space and immediately prunes invalid branches, guaranteeing that any returned solution is 100% clash-free.

---

## 3. MySQL Database Backend & MySQL Workbench Guide

### Database Architecture
- **Database Name**: `timetable_db`
- **Tables**:
  1. `teachers`: ID, name, subject, max_hours
  2. `classrooms`: ID, room_number, capacity
  3. `timeslots`: ID, day, start_time, end_time
  4. `courses`: ID, name, teacher_id (FK), hours_per_week
  5. `course_conflicts`: conflict_id, course_id_1 (FK), course_id_2 (FK), reason
  6. `timetable_assignments`: assignment_id, course_id (FK), teacher_id (FK), room_id (FK), slot_id (FK), is_clash_free
- **Analytical Views**:
  - `v_clash_free_timetable`: Joined master schedule view
  - `v_teacher_workload`: Faculty hour allocations vs caps

---

### Step-by-Step MySQL Workbench Guide

#### Step 1: Open MySQL Workbench & Connect
1. Launch **MySQL Workbench** on your machine.
2. Under **MySQL Connections**, click on your local connection (e.g., `Local instance MySQL` / `localhost:3306`).
3. Enter your password (`root123`) and click **OK**.

#### Step 2: Open and Run `schema.sql`
1. In MySQL Workbench top menu, click **File $\rightarrow$ Open SQL Script...**
2. Browse to:
   `c:\Users\anany\OneDrive\Desktop\DS_Project\database\schema.sql`
3. Click the **Execute (Lightning Bolt)** icon in the SQL editor toolbar.
4. In the **SCHEMAS** panel on the left, right-click and click **Refresh All**. You will now see `timetable_db` with all tables and views!

#### Step 3: Open and Run `seed_data.sql`
1. Click **File $\rightarrow$ Open SQL Script...**
2. Browse to:
   `c:\Users\anany\OneDrive\Desktop\DS_Project\database\seed_data.sql`
3. Click the **Execute (Lightning Bolt)** icon.
4. All initial data for teachers, courses, rooms, slots, and conflicts are now inserted.

#### Step 4: Generate the EER Diagram (Entity-Relationship Diagram)
In MySQL Workbench, you can visualize the database structure:
1. In the top menu, go to **Database $\rightarrow$ Reverse Engineer...**
2. Keep `Stored Connection` as `Local instance MySQL` and click **Next**.
3. Enter your password (`root123`) and click **Next**.
4. Select `timetable_db` and click **Next $\rightarrow$ Execute $\rightarrow$ Next $\rightarrow$ Finish**.
5. Workbench will open an interactive **EER Diagram** displaying all tables, primary keys, and foreign key relationships visually!

#### Step 5: Run Verification Queries in Workbench
1. Open a new query tab (**File $\rightarrow$ New Query Tab**).
2. Open `c:\Users\anany\OneDrive\Desktop\DS_Project\database\queries.sql`.
3. Highlight and execute query #1:
   ```sql
   USE timetable_db;
   SELECT * FROM v_clash_free_timetable;
   ```
   You will see the complete formatted clash-free timetable!
4. Execute query #2 & #3 (Teacher clash and Room clash checks):
   Both queries will return **0 rows**, proving mathematically and empirically that there are zero clashes!

---

## 4. How to Run the Entire Project

### Method 1: Interactive Control Panel
Open your terminal in `DS_Project` and run:
```powershell
python run_project.py
```
This opens an interactive menu where you can run any individual phase, run the MySQL sync, or view the database records.

### Method 2: One-Click Automated Run (All Phases + MySQL Sync)
To demonstrate all phases sequentially in one automated flow:
```powershell
python run_project.py --all
```

### Method 3: One-Click Database Setup
To re-initialize or verify MySQL database tables at any time:
```powershell
python database/setup_db.py
```
