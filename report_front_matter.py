# -*- coding: utf-8 -*-
"""
Module 1: Front Matter, Table of Contents, Title, Introduction, Proposed Solutions,
Objectives, and Scope for Ananya Ann Mathew (26MCAC07).
"""
import os
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def build_front_matter(doc, helpers):
    add_heading_1 = helpers['add_heading_1']
    add_heading_2 = helpers['add_heading_2']
    add_heading_3 = helpers['add_heading_3']
    add_paragraph = helpers['add_paragraph']
    add_bullet = helpers['add_bullet']
    add_styled_table = helpers['add_styled_table']
    LOGO_FILE = helpers['LOGO_FILE']

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    print(">> Generating Cover Page...")
    if os.path.exists(LOGO_FILE):
        logo_p = doc.add_paragraph()
        logo_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        logo_p.paragraph_format.space_before = Pt(0)
        logo_p.paragraph_format.space_after = Pt(8)
        logo_p.add_run().add_picture(LOGO_FILE, width=Inches(5.0))

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(4)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("KRISTU JAYANTI INSTITUTE OF TECHNOLOGY\n")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(13)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(12, 35, 64)

    r_sub_inst = p_inst.add_run("KRISTU JAYANTI (DEEMED TO BE UNIVERSITY), BENGALURU\n")
    r_sub_inst.font.name = "Times New Roman"
    r_sub_inst.font.size = Pt(11)
    r_sub_inst.font.bold = True
    r_sub_inst.font.color.rgb = RGBColor(70, 70, 70)

    p_proj = doc.add_paragraph()
    p_proj.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_proj.paragraph_format.space_before = Pt(14)
    p_proj.paragraph_format.space_after = Pt(6)
    r_rep = p_proj.add_run("PROJECT-BASED PRACTICAL REPORT ON\n")
    r_rep.font.name = "Times New Roman"
    r_rep.font.size = Pt(13)
    r_rep.font.bold = True

    r_title = p_proj.add_run("“CAMPUSGRID: INTELLIGENT CLASH-FREE TIMETABLE GENERATOR & ACADEMIC SCHEDULING SYSTEM”\n")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(15.5)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(12, 35, 64)

    p_req = doc.add_paragraph()
    p_req.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_req.paragraph_format.space_before = Pt(10)
    p_req.paragraph_format.space_after = Pt(10)
    r_req = p_req.add_run(
        "Submitted in partial fulfilment of the requirements for\n"
        "Data Structures Practical Course – First Semester\n"
        "MASTER OF COMPUTER APPLICATIONS (MCA)\n"
    )
    r_req.font.name = "Times New Roman"
    r_req.font.size = Pt(12)
    r_req.font.color.rgb = RGBColor(40, 40, 40)

    p_subm = doc.add_paragraph()
    p_subm.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subm.paragraph_format.space_before = Pt(18)
    p_subm.paragraph_format.space_after = Pt(4)
    r_subm = p_subm.add_run("Submitted by\n")
    r_subm.font.name = "Times New Roman"
    r_subm.font.size = Pt(12)
    r_subm.font.bold = True

    # Candidate info table
    cand_tbl = doc.add_table(rows=1, cols=2)
    cand_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cand_tbl.rows[0].cells[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    cand_tbl.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r_c1 = cand_tbl.rows[0].cells[0].paragraphs[0].add_run("Ananya Ann Mathew")
    r_c1.font.name = "Times New Roman"
    r_c1.font.size = Pt(13)
    r_c1.font.bold = True
    
    r_c2 = cand_tbl.rows[0].cells[1].paragraphs[0].add_run("Register Number: 26MCAC07")
    r_c2.font.name = "Times New Roman"
    r_c2.font.size = Pt(13)
    r_c2.font.bold = True

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(22)
    p_guide.paragraph_format.space_after = Pt(2)
    r_gu = p_guide.add_run("Under the guidance of\n")
    r_gu.font.name = "Times New Roman"
    r_gu.font.size = Pt(12)
    r_gu.font.italic = True

    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sign.paragraph_format.space_before = Pt(2)
    p_sign.paragraph_format.space_after = Pt(2)
    r_sign = p_sign.add_run("__________________________________\n")
    r_sign.font.name = "Times New Roman"
    r_sign.font.size = Pt(12)

    r_fg = p_sign.add_run("Faculty Guide\n")
    r_fg.font.name = "Times New Roman"
    r_fg.font.size = Pt(12)
    r_fg.font.bold = True

    r_gname = p_sign.add_run("Dr. M. Subramaniakumar\n")
    r_gname.font.name = "Times New Roman"
    r_gname.font.size = Pt(13)
    r_gname.font.bold = True
    r_gname.font.color.rgb = RGBColor(12, 35, 64)

    r_dept = p_sign.add_run("Department of Computer Applications\nKristu Jayanti (Deemed to be University), Bengaluru")
    r_dept.font.name = "Times New Roman"
    r_dept.font.size = Pt(11.5)

    doc.add_page_break()

    # =========================================================================
    # CERTIFICATE OF ORIGINALITY & APPROVAL
    # =========================================================================
    print(">> Generating Certificate Page...")
    add_heading_1(doc, "CERTIFICATE OF ORIGINALITY & APPROVAL", page_break=False)
    add_paragraph(doc, 
        "This is to certify that the project-based practical report entitled “CAMPUSGRID: INTELLIGENT "
        "CLASH-FREE TIMETABLE GENERATOR & ACADEMIC SCHEDULING SYSTEM” is a bonafide record of practical work "
        "carried out by Ananya Ann Mathew (Register Number: 26MCAC07), a student of First Semester Master of "
        "Computer Applications (MCA), in partial fulfillment of the requirements for the Data Structures Practical "
        "Course during the academic year 2026 at Kristu Jayanti (Deemed to be University), Bengaluru."
    )
    add_paragraph(doc,
        "The practical assignments, custom linear and non-linear data structures, searching and sorting workflows, "
        "greedy interval optimizations, dynamic programming workload allocations, constraint satisfaction backtracking "
        "solvers, and web-based application interfaces documented in this report have been executed and tested under my "
        "supervision. To the best of my knowledge, this report represents original work and adheres to academic standards."
    )

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(40)
    p_sp.paragraph_format.space_after = Pt(10)

    sig_tbl = doc.add_table(rows=1, cols=2)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_g = sig_tbl.rows[0].cells[0]
    cell_h = sig_tbl.rows[0].cells[1]

    pg = cell_g.paragraphs[0]
    pg.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pg.add_run("_____________________________\n").font.name = "Times New Roman"
    r_fg_title = pg.add_run("Dr. M. Subramaniakumar\n")
    r_fg_title.font.name = "Times New Roman"; r_fg_title.font.bold = True
    pg.add_run("Faculty Guide & Internal Examiner\nDepartment of Computer Applications\nKristu Jayanti University").font.name = "Times New Roman"

    ph = cell_h.paragraphs[0]
    ph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    ph.add_run("_____________________________\n").font.name = "Times New Roman"
    r_hod_title = ph.add_run("Head of Department\n")
    r_hod_title.font.name = "Times New Roman"; r_hod_title.font.bold = True
    ph.add_run("Department of Computer Applications\nKristu Jayanti (Deemed to be University)\nBengaluru, India").font.name = "Times New Roman"

    doc.add_page_break()

    # =========================================================================
    # DECLARATION
    # =========================================================================
    print(">> Generating Declaration Page...")
    add_heading_1(doc, "DECLARATION", page_break=False)
    add_paragraph(doc,
        "I, Ananya Ann Mathew, hereby declare that the project-based practical report entitled "
        "“CAMPUSGRID: INTELLIGENT CLASH-FREE TIMETABLE GENERATOR & ACADEMIC SCHEDULING SYSTEM” submitted to "
        "Kristu Jayanti (Deemed to be University), Bengaluru, in partial fulfillment of the requirements for "
        "the award of the degree of Master of Computer Applications (MCA) for the First Semester Data Structures "
        "Practical Course, is an authentic record of original work performed by me."
    )
    add_paragraph(doc,
        "I confirm that the algorithms, custom pointer-based data structures, database schemas, and web application "
        "controllers described herein were developed and verified by me. The theoretical formulations, asymptotic proofs, "
        "and empirical benchmark results presented in this report have not previously formed the basis for the award of "
        "any other Degree, Diploma, Associateship, Fellowship, or academic distinction at this or any other university."
    )

    p_d_sp = doc.add_paragraph()
    p_d_sp.paragraph_format.space_before = Pt(35)
    p_d_sp.paragraph_format.space_after = Pt(10)

    dec_tbl = doc.add_table(rows=1, cols=2)
    dec_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = dec_tbl.rows[0].cells[0]
    c_right = dec_tbl.rows[0].cells[1]

    p_dl = c_left.paragraphs[0]
    p_dl.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_dl.add_run("Place: Bengaluru\nDate: 05 November 2026").font.name = "Times New Roman"

    p_dr = c_right.paragraphs[0]
    p_dr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_ananya = p_dr.add_run("Ananya Ann Mathew\n")
    r_ananya.font.name = "Times New Roman"; r_ananya.font.bold = True
    p_dr.add_run("Register Number: 26MCAC07\n1st Semester MCA").font.name = "Times New Roman"

    doc.add_page_break()

    # =========================================================================
    # ACKNOWLEDGMENTS
    # =========================================================================
    print(">> Generating Acknowledgments Page...")
    add_heading_1(doc, "ACKNOWLEDGMENTS", page_break=False)
    add_paragraph(doc,
        "I bow in humble gratitude before God Almighty for His abundant grace, wisdom, health, and perseverance "
        "granted to me throughout the execution of this academic practical project."
    )
    add_paragraph(doc,
        "I express my profound gratitude to the Management and Leadership of Kristu Jayanti (Deemed to be University), "
        "Bengaluru, for providing state-of-the-art computational laboratories, an inspiring academic environment, and "
        "the infrastructural support that enabled me to develop and benchmark this system."
    )
    add_paragraph(doc,
        "I am deeply indebted to my faculty guide, Dr. M. Subramaniakumar, Department of Computer Applications, for his "
        "scholarly guidance, constant encouragement, critical insights, and patience throughout every phase of this project. "
        "His guidance on formulating timetabling as a graph-coloring constraint satisfaction problem and linking custom "
        "data structures to real-world software workflows was invaluable."
    )
    add_paragraph(doc,
        "I extend my sincere thanks to the Head of the Department and all faculty members of the Department of "
        "Computer Applications for imparting the foundational principles of Data Structures, Algorithms, Relational "
        "Databases, and Software Engineering. I also thank my parents, family members, and classmates for their unceasing "
        "moral support, constructive feedback, and encouragement during my practical coursework."
    )

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    print(">> Generating Table of Contents...")
    add_heading_1(doc, "TABLE OF CONTENTS", page_break=False)
    add_paragraph(doc, "The practical coursework is organized into cohesive academic phases aligning with syllabus specifications:")

    toc_headers = ["S. No.", "Topics", "Page No."]
    toc_data = [
        ["1", "Introduction", "1"],
        ["1.1", "Objectives", "3"],
        ["1.2", "Project Description", "7"],
        ["2", "Phase I – Core Data Handling using Linear Structures", "15"],
        ["2.1", "Dataset Input and Representation", "15"],
        ["2.2", "Linked List Implementation and Operations", "17"],
        ["2.3", "Stack and Queue Implementation", "19"],
        ["2.4", "Basic Infix to Postfix Conversion & Constraint Parsing", "22"],
        ["2.5", "Iterative and Recursive Approaches", "24"],
        ["3", "Phase II – Structured Data Representation", "26"],
        ["3.1", "Binary Tree Representation", "26"],
        ["3.2", "Tree Traversals (Preorder, Inorder, Postorder)", "27"],
        ["3.3", "Binary Search Tree Implementation & Deletion", "29"],
        ["3.4", "Graph Representation using Adjacency List & Matrix", "32"],
        ["3.5", "Graph Traversal using BFS or DFS", "34"],
        ["4", "Phase III – Data Processing using Searching and Sorting", "37"],
        ["4.1", "Linear Search and Binary Search", "37"],
        ["4.2", "Sorting Techniques (Insertion, Merge, Quick Sort)", "39"],
        ["4.3", "Integration of Searching and Sorting", "42"],
        ["4.4", "Basic Heap or Priority-Based Processing", "43"],
        ["5", "Phase IV – Basic Algorithmic Problem Solving for Data Optimization", "45"],
        ["5.1", "Selection of an Algorithmic Problem", "45"],
        ["5.2", "Greedy / Dynamic Programming / Backtracking Approach", "46"],
        ["5.3", "Implementation and Result Analysis", "49"],
        ["5.4", "Integration with Dataset Analysis", "51"],
        ["5.5", "Final Testing and Demonstration", "53"],
        ["6", "Screenshots and User Interface Walkthrough", "55"],
        ["7", "Source Code (Functional Code Structure)", "60"],
        ["8", "Features of the Project", "65"],
        ["9", "Future Enhancements", "68"],
        ["10", "Conclusion", "70"],
        ["11", "References", "72"],
    ]
    add_styled_table(doc, toc_headers, toc_data, col_widths=[0.8, 4.8, 1.0])

    doc.add_page_break()

    # =========================================================================
    # TITLE OF THE PROJECT
    # =========================================================================
    print(">> Generating Project Title Section...")
    add_heading_1(doc, "TITLE OF THE PROJECT", page_break=False)
    add_heading_2(doc, "CAMPUSGRID: INTELLIGENT CLASH-FREE TIMETABLE GENERATOR & ACADEMIC SCHEDULING SYSTEM")
    add_paragraph(doc,
        "The project is titled CampusGrid: Intelligent Clash-Free Timetable Generator & Academic Scheduling System. "
        "It combines a practical, responsive university timetable management web application with a complete set of "
        "explicit, from-scratch data structure implementations and algorithmic problem-solving paradigms. A timetable "
        "entry is treated as an atomic, multi-dimensional relational tuple—combining class section, date, temporal window, "
        "academic course, assigned professor, and physical classroom—rather than a passive text entry in an arbitrary spreadsheet."
    )
    add_paragraph(doc,
        "The moniker 'CampusGrid' reflects two interrelated engineering objectives. 'Campus' emphasizes the institutional "
        "academic reality: managing students across distinct cohorts (e.g., MCA Section A, Section B), coordinating faculty "
        "workloads across specialized computer science disciplines, and optimizing shared physical infrastructure such as "
        "multimedia lecture halls, seminar rooms, and computer labs. 'Grid' denotes both the visual 5-day weekly matrix that "
        "students and faculty rely upon, and the underlying mathematical conflict graph and discrete-time constraint lattice "
        "governing all scheduled events."
    )
    add_paragraph(doc,
        "The repository is structured into four progressive laboratory phases, a robust relational persistence backend "
        "(supporting both SQLite for immediate local execution and MySQL Workbench for enterprise EER modeling), and a "
        "modern full-stack web dashboard (Flask micro-framework backend coupled with responsive HTML5, modern CSS, and "
        "asynchronous JavaScript). This decoupled architectural arrangement ensures that core data structure algorithms "
        "can be inspected, verified, and benchmarked independently in a terminal, while simultaneously powering an "
        "intuitive, real-time web portal for campus stakeholders."
    )

    # =========================================================================
    # 1. INTRODUCTION
    # =========================================================================
    print(">> Generating Chapter 1: Introduction...")
    add_heading_1(doc, "1. INTRODUCTION", page_break=True)
    add_paragraph(doc,
        "Every semester at Kristu Jayanti (Deemed to be University), academic coordinators face the daunting challenge "
        "of creating an error-free timetable. A university timetable is not merely a calendar; it is the central operational "
        "blueprint of the entire institution. It synchronizes hundreds of enrolled students, dozens of specialized professors, "
        "and physical classrooms and laboratories across multiple campus buildings."
    )
    add_paragraph(doc,
        "When timetables are prepared manually—using physical whiteboards, paper sheets, or spreadsheets—human cognitive "
        "fatigue inevitably leads to scheduling collisions. A professor is accidentally double-booked for two separate lectures "
        "at 10:00 AM on Monday; two different student sections arrive at Room A-101 at the same hour; or a small elective "
        "batch of 20 students is allocated a 120-seat auditorium while a mandatory lecture of 60 students is forced into a "
        "cramped lab. These conflicts disrupt classes, waste physical infrastructure, and cause unnecessary administrative friction."
    )
    add_paragraph(doc,
        "The University Course Timetabling Problem (UCTP) is formally recognized in computational complexity theory as an "
        "NP-Complete combinatorial constraint satisfaction problem. It cannot be resolved effectively through brute-force "
        "permutations because the search space explodes exponentially with every additional course, classroom, and faculty member. "
        "For a department with just 30 course modules and 6 timeslots, the number of possible assignment permutations exceeds "
        "6^30 (approximately 2.21 × 10^23), rendering unguided exploration completely impossible."
    )
    add_paragraph(doc,
        "CampusGrid solves this fundamental challenge by uniting foundational Data Structures and Algorithms (DSA) with "
        "modern software engineering. By modeling courses as graph vertices, conflicts as undirected edges, and timeslots as "
        "colors, the scheduling puzzle is transformed into a Graph Vertex Coloring Problem. We then apply recursive backtracking "
        "with Most Constrained Variable (MCV) degree heuristics, 0/1 Knapsack Dynamic Programming for faculty workload balancing, "
        "Greedy Activity Selection for shared venue optimization, and Best-Fit Binary Search to eliminate classroom seat wastage."
    )

    # =========================================================================
    # 2. PROPOSED SOLUTIONS
    # =========================================================================
    print(">> Generating Chapter 2: Proposed Solutions...")
    add_heading_1(doc, "2. PROPOSED SOLUTIONS", page_break=True)
    add_paragraph(doc,
        "In computer science education, data structures and algorithmic concepts are frequently taught as isolated abstractions. "
        "A student memorizes that a stack is Last-In, First-Out (LIFO) or that a binary search tree offers O(log n) lookups, but "
        "rarely sees how these mechanisms solve concrete operational bottlenecks in a cohesive production system. The core "
        "philosophy behind CampusGrid is to connect every foundational data structure directly to a visible user-facing workflow:"
    )

    add_bullet(doc, 
        "Rather than relying on contiguous dynamic arrays that incur hidden reallocation and element-shifting costs, a custom "
        "singly linked list manages active course and classroom records dynamically using memory pointers. When viewing recent "
        "schedule changes, a move-to-front linked list ensures that recently touched items appear first in O(1) time.",
        bold_prefix="1. Custom Singly Linked List for Dynamic Records:"
    )
    add_bullet(doc,
        "When an administrator edits or schedules a class that inadvertently causes downstream issues, a stack provides "
        "instantaneous undo capability. Because a stack operates under LIFO discipline, the most recent scheduling action is "
        "always the first candidate restored, ensuring the timeline is reverted in exact inverse order.",
        bold_prefix="2. LIFO Stack for Schedule Mutation Rollback:"
    )
    add_bullet(doc,
        "Course requests submitted by various academic departments arrive asynchronously. A FIFO queue ensures strict chronological "
        "fairness: the first department offering placed in the scheduling buffer is the first one allocated a classroom, preventing "
        "introductory modules from being starved of prime morning slots.",
        bold_prefix="3. FIFO Queue for Departmental Course Ingestion:"
    )
    add_bullet(doc,
        "Looking up a course by identifier in an unsorted list takes O(n) linear time. By structuring course records into a Binary "
        "Search Tree (BST) keyed on course ID, search time drops to O(log n) average complexity, while an in-order traversal yields "
        "an automatically sorted curriculum roster.",
        bold_prefix="4. Binary Search Tree (BST) for Logarithmic Indexing:"
    )
    add_bullet(doc,
        "Academic conflicts are inherently relational. CampusGrid constructs a dual-representation Conflict Graph (Adjacency List "
        "for memory efficiency and 2D Adjacency Matrix for instant O(1) edge checks). Breadth-First Search (BFS) is then utilized to "
        "discover independent connected components, allowing non-conflicting departments to be scheduled in parallel.",
        bold_prefix="5. Conflict Graph and Component Decomposition (BFS):"
    )
    add_bullet(doc,
        "To prevent faculty burnout and satisfy University Grants Commission (UGC) workload ceilings (maximum 14–16 lecture hours "
        "per week), course allocations are modeled as a 0/1 Knapsack problem and solved via Dynamic Programming. This guarantees "
        "that total instructional credit value is maximized without exceeding statutory workload caps.",
        bold_prefix="6. Dynamic Programming for Faculty Workload Compliance:"
    )
    add_bullet(doc,
        "Classrooms are sorted in ascending order of seating capacity using Quick Sort. When a course requires a venue, a Best-Fit "
        "Binary Search identifies the smallest available classroom capable of seating the enrolled students, eliminating seat wastage.",
        bold_prefix="7. Divide-and-Conquer Sorting and Best-Fit Allocation:"
    )
    add_bullet(doc,
        "A full-stack web dashboard built with Flask and Vanilla HTML5/CSS/JavaScript exposes role-based views for Administrators, "
        "Faculty, and Students, complemented by an atomic 3-point clash verification engine evaluating room, teacher, and section "
        "availability in real time.",
        bold_prefix="8. Full-Stack Web Portal with Tri-Factor Real-Time Clash Prevention:"
    )

    # =========================================================================
    # 3. OBJECTIVE OF THE PROJECT
    # =========================================================================
    print(">> Generating Chapter 3: Objectives...")
    add_heading_1(doc, "3. OBJECTIVE OF THE PROJECT", page_break=True)
    add_heading_2(doc, "1.1 Objectives")
    add_paragraph(doc,
        "The comprehensive objective of CampusGrid is to design, implement, analyze, and demonstrate an automated, "
        "clash-free academic timetabling web system backed by custom data structures and classic algorithmic optimization "
        "techniques. The specific objectives are categorized into functional, algorithmic, and software engineering domains:"
    )

    add_heading_3(doc, "Functional & Operational Objectives:")
    add_bullet(doc, "To provide an interactive timetable studio allowing academic administrators to create, update, and delete schedule slots with instantaneous feedback.", bold_prefix="• Schedule Lifecycle Management:")
    add_bullet(doc, "To enforce a mathematical zero-clash guarantee across three critical institutional dimensions: Classroom double-booking, Faculty concurrent lecturing, and Student cohort lecture overlap.", bold_prefix="• Tri-Factor Conflict Prevention:")
    add_bullet(doc, "To provide faculty members with personalized daily and weekly lecture views, alongside a digital desk to submit rescheduling and extra-hour coaching requests.", bold_prefix="• Faculty Self-Service Desk:")
    add_bullet(doc, "To provide students with section-specific (MCA A, MCA B) 3-day rolling agendas and 5-day weekly scheduling grids accessible on mobile and desktop viewports.", bold_prefix="• Student Cohort Visualizer:")
    add_bullet(doc, "To streamline administrative approval of faculty requests such that approved changes mutate the live database and propagate immediately across all student calendars.", bold_prefix="• Dynamic Mutation Workflow:")

    add_heading_3(doc, "Algorithmic & Data Structure Objectives:")
    add_bullet(doc, "To construct all linear data structures (generic Node, Singly Linked List, LIFO Stack, FIFO Queue) from foundational memory pointers without utilizing third-party abstraction packages.", bold_prefix="• Scratch Linear Structures:")
    add_bullet(doc, "To implement an expression handler using stack mechanics to parse, validate, and convert propositional timetabling constraint expressions from infix to postfix notation.", bold_prefix="• Constraint Expression Parser:")
    add_bullet(doc, "To construct an academic institutional hierarchy using a Binary Tree and explore Preorder, Inorder, and Postorder traversals for administrative and prerequisite audits.", bold_prefix="• Hierarchical Tree Modeling:")
    add_bullet(doc, "To implement a Binary Search Tree (BST) supporting O(log n) search, insertion, in-order sorted traversal, and three-case node deletion (leaf, single child, two children via in-order successor).", bold_prefix="• Logarithmic Indexing:")
    add_bullet(doc, "To construct a Conflict Graph in both Adjacency List and 2D Adjacency Matrix formats, applying BFS to isolate connected components and DFS to detect circular prerequisite deadlocks.", bold_prefix="• Graph Theory & Traversals:")
    add_bullet(doc, "To benchmark searching (Linear vs Binary) and sorting (Insertion, Merge, Quick Sort) empirically across expanding datasets from N = 10 to N = 250 records.", bold_prefix="• Empirical Benchmarking:")
    add_bullet(doc, "To implement Greedy Activity Selection (Earliest Finish Time heuristic) for single-hall utilization and Interval Partitioning for minimum venue count calculation.", bold_prefix="• Greedy Optimization:")
    add_bullet(doc, "To formulate and solve faculty teaching load limits as a 0/1 Knapsack problem using Dynamic Programming, constructing full 2D tables and backtracking optimal course subsets.", bold_prefix="• Dynamic Programming Optimizer:")
    add_bullet(doc, "To model timetable slot assignment as a Graph Vertex Coloring Constraint Satisfaction Problem (CSP) and solve it via recursive backtracking guided by the Most Constrained Variable (MCV) degree heuristic.", bold_prefix="• CSP Backtracking Solver:")

    # =========================================================================
    # 4. SCOPE OF THE PROJECT
    # =========================================================================
    print(">> Generating Chapter 4: Scope...")
    add_heading_1(doc, "4. SCOPE OF THE PROJECT", page_break=True)
    add_heading_2(doc, "1.2 Project Description & Scope Boundaries")
    add_paragraph(doc,
        "The scope of CampusGrid encompasses the core operational scheduling workflow of a university department. "
        "The project is designed to be accessible as a standalone computational laboratory submission while simultaneously "
        "serving as a functional web application prototype suitable for department-level deployment."
    )
    add_paragraph(doc,
        "Within the current implementation boundary, the system models:"
    )
    add_bullet(doc, "Multiple distinct student cohorts progressing through homogeneous academic tracks (specifically demonstrated for MCA Section A, Section B, Section C, and Section D).", bold_prefix="• Student Cohort Scope:")
    add_bullet(doc, "A roster of accredited professorial faculty members, each associated with specific subject domain expertise, contact emails, and statutory maximum teaching hours.", bold_prefix="• Faculty Resource Scope:")
    add_bullet(doc, "A collection of physical classrooms, lecture halls, seminar venues, and computer laboratories with designated seating capacities and facility types (e.g., Room A-101, Room B-202, Room C-303, Systems Lab-1).", bold_prefix="• Physical Infrastructure Scope:")
    add_bullet(doc, "A discrete weekly calendar structured across six 60-minute instructional windows per day (09:00–10:00 AM, 10:00–11:00 AM, 11:15–12:15 PM, 01:00–02:00 PM, 02:00–03:00 PM, 03:15–04:15 PM), Monday through Friday.", bold_prefix="• Temporal Scheduling Grid:")
    add_bullet(doc, "Role-Based Access Control (RBAC) supporting three discrete personas: Administrators (Dean/HOD), Faculty Members (Professors), and Student Scholars.", bold_prefix="• Security & Authorization Scope:")
    add_bullet(doc, "Dual-persistence database architecture: SQLite3 (portal_data.db) for out-of-the-box zero-configuration web execution, and MySQL 8.0 (timetable_db) for enterprise DDL, foreign key cascading integrity, and MySQL Workbench EER visualization.", bold_prefix="• Database Persistence Scope:")

    add_paragraph(doc,
        "Non-functional boundaries and assumptions are explicitly documented to preserve academic integrity:"
    )
    add_bullet(doc, "The current scheduler models single-campus operations. Multi-campus transit distance matrices and traveling faculty travel windows are identified as future enhancements.", bold_prefix="• Geographic Boundaries:")
    add_bullet(doc, "The system operates on deterministic hard constraints. Stochastic variables (such as sudden weather emergencies or unplanned power cuts) are handled via real-time rescheduling rather than predictive probability.", bold_prefix="• Determinism Assumption:")
    add_bullet(doc, "The web portal is engineered as an educational prototype. While passwords in SQLite are hashed and session cookies are utilized, enterprise single-sign-on (SSO) and biometric attendance integration are scope extensions for future versions.", bold_prefix="• Deployment Security Scope:")

    print(">> Front matter and initial chapters built successfully.")

