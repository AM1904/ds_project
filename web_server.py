# -*- coding: utf-8 -*-
"""
Campus Timetable Portal — Backend
Roles:
  - Admin:   Creates timetable, manages schedule, approves/rejects faculty requests
  - Faculty: Views own day schedule, submits change requests and extra-hour requests
  - Student: Views 3-day timetable for their class section

Teacher data comes from REGISTERED FACULTY ACCOUNTS in the users table.
No hardcoded teachers in subjects — subjects are just courses; teachers are assigned per schedule slot.
"""
import os
import sqlite3
from datetime import datetime, date, timedelta
from flask import Flask, request, jsonify, send_from_directory, session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE  = os.path.join(BASE_DIR, "portal_data.db")

app = Flask(__name__, static_folder="web", static_url_path="")
app.secret_key = "campus_portal_secret_2026"

# -----------------------------------------------------------------------
# DB helpers
# -----------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db(); c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            section TEXT,
            department TEXT,
            phone TEXT,
            created_at TEXT NOT NULL
        )""")

    # Subjects — each has a default assigned faculty (by email)
    c.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT NOT NULL,
            name TEXT NOT NULL,
            credits INTEGER NOT NULL,
            department TEXT NOT NULL,
            faculty_email TEXT NOT NULL DEFAULT ''
        )""")

    c.execute("""
        CREATE TABLE IF NOT EXISTS classrooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            room_type TEXT NOT NULL
        )""")

    # schedule now stores teacher_name + teacher_email chosen at creation time
    c.execute("""
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            section TEXT NOT NULL,
            date TEXT NOT NULL,
            timeslot TEXT NOT NULL,
            subject_id INTEGER NOT NULL,
            classroom_id INTEGER NOT NULL,
            teacher_name TEXT NOT NULL DEFAULT '',
            teacher_email TEXT NOT NULL DEFAULT '',
            created_by TEXT,
            has_clash INTEGER DEFAULT 0,
            clash_reason TEXT,
            FOREIGN KEY (subject_id)   REFERENCES subjects(id),
            FOREIGN KEY (classroom_id) REFERENCES classrooms(id)
        )""")

    c.execute("""
        CREATE TABLE IF NOT EXISTS faculty_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            faculty_name TEXT NOT NULL,
            faculty_email TEXT NOT NULL,
            request_type TEXT NOT NULL,
            schedule_id INTEGER,
            requested_date TEXT NOT NULL,
            requested_timeslot TEXT,
            requested_classroom TEXT,
            preferred_section TEXT,
            reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            admin_note TEXT,
            created_at TEXT NOT NULL,
            resolved_at TEXT
        )""")

    conn.commit()

    # --- Seed subjects (each linked to a default faculty by email) ---
    c.execute("SELECT COUNT(*) FROM subjects")
    if c.fetchone()[0] == 0:
        subjects = [
            ("MCA-201", "Data Structures & Algorithms", 4, "Computer Science",    "ananya@college.edu"),
            ("MCA-202", "Operating Systems",             3, "Systems Engineering", "ravi.k@college.edu"),
            ("MCA-203", "Database Management Systems",   3, "Database Technologies","priya.nair@college.edu"),
            ("MCA-204", "Computer Networks",             3, "Network Systems",     "arjun.m@college.edu"),
            ("MCA-205", "Machine Learning & AI",         3, "Artificial Intelligence","sunita.rao@college.edu"),
            ("MCA-206", "Web Technologies & Cloud",      3, "Software Engineering","vikram.j@college.edu"),
        ]
        c.executemany(
            "INSERT INTO subjects (code,name,credits,department,faculty_email) VALUES (?,?,?,?,?)",
            subjects
        )

    # --- Seed classrooms ---
    c.execute("SELECT COUNT(*) FROM classrooms")
    if c.fetchone()[0] == 0:
        rooms = [
            ("Room A-101",  60, "Lecture Hall"),
            ("Room B-202",  45, "Classroom"),
            ("Room C-303",  30, "Seminar Hall"),
            ("Systems Lab-1", 25, "Computer Lab"),
        ]
        c.executemany("INSERT INTO classrooms (name,capacity,room_type) VALUES (?,?,?)", rooms)

    # --- Seed admin + all 6 faculty accounts ---
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] == 0:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        users = [
            # Admin
            ("Administrator",    "admin@college.edu",      "admin123",   "Admin",   "",       "Dean of Academics",       "+91 9800000000", now),
            # Faculty — one per subject
            ("Dr. Ananya Sharma","ananya@college.edu",     "faculty123", "Faculty", "",       "Computer Science",         "+91 9800000001", now),
            ("Prof. Ravi Kumar", "ravi.k@college.edu",     "faculty123", "Faculty", "",       "Systems Engineering",      "+91 9800000002", now),
            ("Ms. Priya Nair",   "priya.nair@college.edu", "faculty123", "Faculty", "",       "Database Technologies",    "+91 9800000003", now),
            ("Mr. Arjun Mehta",  "arjun.m@college.edu",    "faculty123", "Faculty", "",       "Network Systems",          "+91 9800000004", now),
            ("Dr. Sunita Rao",   "sunita.rao@college.edu", "faculty123", "Faculty", "",       "Artificial Intelligence",  "+91 9800000005", now),
            ("Prof. Vikram Joshi","vikram.j@college.edu",  "faculty123", "Faculty", "",       "Software Engineering",     "+91 9800000006", now),
        ]
        c.executemany(
            "INSERT INTO users (name,email,password,role,section,department,phone,created_at) VALUES (?,?,?,?,?,?,?,?)",
            users
        )

    # --- Seed sample schedule with real teacher emails ---
    c.execute("SELECT COUNT(*) FROM schedule")
    if c.fetchone()[0] == 0:
        today = date.today().isoformat()
        tom   = (date.today() + timedelta(days=1)).isoformat()
        sched = [
            # MCA A — today
            ("MCA A", today, "09:00 AM - 10:00 AM", 1, 1, "Dr. Ananya Sharma",   "ananya@college.edu",     "admin@college.edu", 0, None),
            ("MCA A", today, "10:00 AM - 11:00 AM", 2, 2, "Prof. Ravi Kumar",    "ravi.k@college.edu",     "admin@college.edu", 0, None),
            ("MCA A", today, "01:00 PM - 02:00 PM", 3, 4, "Ms. Priya Nair",      "priya.nair@college.edu", "admin@college.edu", 0, None),
            # MCA B — today
            ("MCA B", today, "09:00 AM - 10:00 AM", 4, 3, "Mr. Arjun Mehta",    "arjun.m@college.edu",    "admin@college.edu", 0, None),
            ("MCA B", today, "11:15 AM - 12:15 PM", 5, 1, "Dr. Sunita Rao",     "sunita.rao@college.edu", "admin@college.edu", 0, None),
            ("MCA B", today, "02:00 PM - 03:00 PM", 6, 4, "Prof. Vikram Joshi", "vikram.j@college.edu",   "admin@college.edu", 0, None),
            # MCA A — tomorrow
            ("MCA A", tom,   "10:00 AM - 11:00 AM", 4, 3, "Mr. Arjun Mehta",    "arjun.m@college.edu",    "admin@college.edu", 0, None),
            ("MCA A", tom,   "11:15 AM - 12:15 PM", 5, 1, "Dr. Sunita Rao",     "sunita.rao@college.edu", "admin@college.edu", 0, None),
            # MCA B — tomorrow
            ("MCA B", tom,   "09:00 AM - 10:00 AM", 1, 2, "Dr. Ananya Sharma",  "ananya@college.edu",     "admin@college.edu", 0, None),
            ("MCA B", tom,   "02:00 PM - 03:00 PM", 6, 4, "Prof. Vikram Joshi", "vikram.j@college.edu",   "admin@college.edu", 0, None),
        ]
        c.executemany(
            "INSERT INTO schedule (section,date,timeslot,subject_id,classroom_id,teacher_name,teacher_email,created_by,has_clash,clash_reason) VALUES (?,?,?,?,?,?,?,?,?,?)",
            sched
        )

    conn.commit(); conn.close()

init_db()

TIMESLOTS = [
    "09:00 AM - 10:00 AM",
    "10:00 AM - 11:00 AM",
    "11:15 AM - 12:15 PM",
    "01:00 PM - 02:00 PM",
    "02:00 PM - 03:00 PM",
    "03:15 PM - 04:15 PM",
]
SECTIONS = ["MCA A", "MCA B", "MCA C", "MCA D"]

# -----------------------------------------------------------------------
# Static
# -----------------------------------------------------------------------
@app.route("/")
def index(): return send_from_directory("web", "index.html")

# -----------------------------------------------------------------------
# AUTH
# -----------------------------------------------------------------------
@app.route("/api/auth/login", methods=["POST"])
def api_login():
    d = request.get_json() or {}
    email, password = d.get("email","").strip().lower(), d.get("password","").strip()
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM users WHERE LOWER(email)=? AND password=?", (email, password))
    user = c.fetchone(); conn.close()
    if not user:
        return jsonify({"success": False, "message": "Invalid email or password"}), 401
    u = dict(user); del u["password"]
    session["user"] = u
    return jsonify({"success": True, "user": u})

@app.route("/api/auth/register", methods=["POST"])
def api_register():
    d = request.get_json() or {}
    name     = d.get("name","").strip()
    email    = d.get("email","").strip().lower()
    password = d.get("password","").strip()
    role     = d.get("role","Student").strip()
    section  = d.get("section","").strip()
    dept     = d.get("department","").strip()
    phone    = d.get("phone","").strip()

    if not name or not email or not password:
        return jsonify({"success": False, "message": "Name, email and password are required"}), 400

    conn = get_db(); c = conn.cursor()
    c.execute("SELECT id FROM users WHERE LOWER(email)=?", (email,))
    if c.fetchone():
        conn.close()
        return jsonify({"success": False, "message": "An account with this email already exists"}), 400

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if role == "Student" and not section:
        section = "MCA A"
    if not dept:
        dept = "MCA Department" if role == "Student" else "General"

    c.execute(
        "INSERT INTO users (name,email,password,role,section,department,phone,created_at) VALUES (?,?,?,?,?,?,?,?)",
        (name, email, password, role, section, dept, phone, now)
    )
    uid = c.lastrowid; conn.commit()
    c.execute("SELECT * FROM users WHERE id=?", (uid,))
    user = dict(c.fetchone()); conn.close()
    del user["password"]
    session["user"] = user
    return jsonify({"success": True, "user": user})

@app.route("/api/auth/me")
def api_me():
    u = session.get("user")
    return jsonify({"authenticated": bool(u), "user": u})

@app.route("/api/auth/logout", methods=["POST"])
def api_logout():
    session.pop("user", None)
    return jsonify({"success": True})

@app.route("/api/auth/profile", methods=["PUT"])
def api_profile():
    d = request.get_json() or {}
    uid  = d.get("id")
    name = d.get("name","").strip()
    phone= d.get("phone","").strip()
    sect = d.get("section","").strip()
    dept = d.get("department","").strip()
    conn = get_db(); c = conn.cursor()
    c.execute("UPDATE users SET name=?,phone=?,section=?,department=? WHERE id=?", (name, phone, sect, dept, uid))
    conn.commit()
    c.execute("SELECT * FROM users WHERE id=?", (uid,))
    user = dict(c.fetchone()); conn.close()
    del user["password"]; session["user"] = user
    return jsonify({"success": True, "user": user})

# -----------------------------------------------------------------------
# Reference data
# -----------------------------------------------------------------------
@app.route("/api/subjects")
def api_subjects():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM subjects ORDER BY id")
    rows = [dict(r) for r in c.fetchall()]; conn.close()
    return jsonify(rows)

@app.route("/api/classrooms")
def api_classrooms():
    conn = get_db(); c = conn.cursor()
    c.execute("SELECT * FROM classrooms ORDER BY capacity DESC")
    rows = [dict(r) for r in c.fetchall()]; conn.close()
    return jsonify(rows)

@app.route("/api/timeslots")
def api_timeslots(): return jsonify(TIMESLOTS)

@app.route("/api/sections")
def api_sections(): return jsonify(SECTIONS)

# NEW: returns all registered Faculty users for the admin teacher picker
@app.route("/api/users/faculty")
def api_faculty_users():
    conn = get_db(); c = conn.cursor()
    c.execute("""
        SELECT id, name, email, department, phone, created_at
        FROM users
        WHERE LOWER(role)='faculty'
        ORDER BY name ASC
    """)
    rows = [dict(r) for r in c.fetchall()]; conn.close()
    return jsonify(rows)

# -----------------------------------------------------------------------
# Clash detection helper
# -----------------------------------------------------------------------
def check_clash(conn, section, date_str, timeslot, teacher_email, classroom_id, ignore_id=None):
    c = conn.cursor()
    c.execute("SELECT * FROM classrooms WHERE id=?", (classroom_id,))
    rm = c.fetchone()
    room_name = rm["name"] if rm else ""

    q = """
        SELECT s.id, s.section, s.teacher_name, s.teacher_email,
               sub.name AS subject_name, cr.name AS room_name
        FROM schedule s
        JOIN subjects sub ON s.subject_id=sub.id
        JOIN classrooms cr ON s.classroom_id=cr.id
        WHERE s.date=? AND s.timeslot=?"""
    params = [date_str, timeslot]
    if ignore_id:
        q += " AND s.id!=?"; params.append(ignore_id)
    c.execute(q, params)

    for row in c.fetchall():
        if row["room_name"] == room_name:
            return True, "room", f"Classroom clash: {room_name} is already booked for {row['section']} ({row['subject_name']})."
        if row["teacher_email"] == teacher_email and teacher_email:
            return True, "teacher", f"Teacher clash: {row['teacher_name']} is already teaching {row['subject_name']} for {row['section']} at this time."
        if row["section"] == section:
            return True, "section", f"Section clash: {section} already has {row['subject_name']} scheduled in this timeslot."
    return False, None, "No clash"

# -----------------------------------------------------------------------
# Schedule CRUD
# -----------------------------------------------------------------------
def _full_schedule_query(where="", params=None):
    return (f"""
        SELECT s.id, s.section, s.date, s.timeslot, s.has_clash, s.clash_reason,
               s.teacher_name, s.teacher_email,
               sub.id AS subject_id, sub.code AS subject_code, sub.name AS subject_name,
               sub.department AS subject_department,
               cr.id AS classroom_id, cr.name AS room_name, cr.capacity AS room_capacity, cr.room_type
        FROM schedule s
        JOIN subjects sub ON s.subject_id=sub.id
        JOIN classrooms cr ON s.classroom_id=cr.id
        {where}
        ORDER BY s.date ASC, s.timeslot ASC""", params or [])

@app.route("/api/schedule")
def api_schedule():
    section  = request.args.get("section")
    date_str = request.args.get("date")
    w, p = [], []
    if section and section != "ALL": w.append("s.section=?");  p.append(section)
    if date_str:                     w.append("s.date=?");     p.append(date_str)
    where = ("WHERE " + " AND ".join(w)) if w else ""
    q, params = _full_schedule_query(where, p)
    conn = get_db(); c = conn.cursor(); c.execute(q, params)
    rows = [dict(r) for r in c.fetchall()]; conn.close()
    return jsonify(rows)

@app.route("/api/schedule/create", methods=["POST"])
def api_create_schedule():
    d = request.get_json() or {}
    section       = d.get("section", "MCA A")
    date_str      = d.get("date", "")
    timeslot      = d.get("timeslot", "")
    subject_id    = int(d.get("subject_id", 0))
    classroom_id  = int(d.get("classroom_id", 0))
    teacher_name  = d.get("teacher_name", "").strip()
    teacher_email = d.get("teacher_email", "").strip().lower()
    created_by    = session.get("user", {}).get("email", "admin")

    if not all([date_str, timeslot, subject_id, classroom_id, teacher_name]):
        return jsonify({"success": False, "message": "All fields including teacher are required"}), 400

    conn = get_db()
    has_clash, clash_type, clash_msg = check_clash(
        conn, section, date_str, timeslot, teacher_email, classroom_id
    )

    c = conn.cursor()
    c.execute("""
        INSERT INTO schedule
          (section, date, timeslot, subject_id, classroom_id,
           teacher_name, teacher_email, created_by, has_clash, clash_reason)
        VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (section, date_str, timeslot, subject_id, classroom_id,
         teacher_name, teacher_email, created_by,
         1 if has_clash else 0, clash_msg if has_clash else None))
    eid = c.lastrowid; conn.commit()

    q, params = _full_schedule_query("WHERE s.id=?", [eid])
    c.execute(q, params); entry = dict(c.fetchone()); conn.close()

    return jsonify({
        "success": True,
        "entry": entry,
        "has_clash": has_clash,
        "clash_type": clash_type,
        "message": clash_msg
    })

@app.route("/api/schedule/<int:eid>", methods=["DELETE"])
def api_delete_schedule(eid):
    conn = get_db(); c = conn.cursor()
    c.execute("DELETE FROM schedule WHERE id=?", (eid,)); conn.commit(); conn.close()
    return jsonify({"success": True})

# -----------------------------------------------------------------------
# Faculty: own day schedule (matched by teacher_email in schedule table)
# -----------------------------------------------------------------------
@app.route("/api/faculty-schedule")
def api_faculty_schedule():
    teacher_email = request.args.get("teacher_email", "").strip().lower()
    date_str      = request.args.get("date", date.today().isoformat())

    conn = get_db(); c = conn.cursor()
    c.execute("""
        SELECT s.id, s.section, s.date, s.timeslot, s.has_clash, s.clash_reason,
               s.teacher_name, s.teacher_email,
               sub.id AS subject_id, sub.code AS subject_code, sub.name AS subject_name,
               sub.department AS subject_department,
               cr.id AS classroom_id, cr.name AS room_name, cr.capacity AS room_capacity, cr.room_type
        FROM schedule s
        JOIN subjects sub ON s.subject_id=sub.id
        JOIN classrooms cr ON s.classroom_id=cr.id
        WHERE s.date=? AND LOWER(s.teacher_email)=?
        ORDER BY s.timeslot ASC""", (date_str, teacher_email))
    rows = [dict(r) for r in c.fetchall()]; conn.close()
    return jsonify(rows)

# -----------------------------------------------------------------------
# Student: 3-day schedule
# -----------------------------------------------------------------------
@app.route("/api/student-schedule")
def api_student_schedule():
    section = request.args.get("section", "MCA A")
    today   = date.today()
    days = [
        {"key": "today",     "date": today.isoformat(),
         "label": "Today",              "day_name": today.strftime("%A"),
         "formatted": today.strftime("%d %b %Y")},
        {"key": "tomorrow",  "date": (today+timedelta(days=1)).isoformat(),
         "label": "Tomorrow",           "day_name": (today+timedelta(days=1)).strftime("%A"),
         "formatted": (today+timedelta(days=1)).strftime("%d %b %Y")},
        {"key": "day_after", "date": (today+timedelta(days=2)).isoformat(),
         "label": "Day After Tomorrow", "day_name": (today+timedelta(days=2)).strftime("%A"),
         "formatted": (today+timedelta(days=2)).strftime("%d %b %Y")},
    ]
    conn = get_db(); c = conn.cursor(); result = []
    for d in days:
        c.execute("""
            SELECT s.id, s.section, s.date, s.timeslot, s.has_clash, s.clash_reason,
                   s.teacher_name, s.teacher_email,
                   sub.code AS subject_code, sub.name AS subject_name,
                   sub.department AS subject_department,
                   cr.name AS room_name
            FROM schedule s
            JOIN subjects sub ON s.subject_id=sub.id
            JOIN classrooms cr ON s.classroom_id=cr.id
            WHERE s.section=? AND s.date=?
            ORDER BY s.timeslot ASC""", (section, d["date"]))
        classes = [dict(r) for r in c.fetchall()]
        result.append({"meta": d, "classes": classes, "has_classes": len(classes) > 0})
    conn.close()
    return jsonify({"section": section, "days": result})

# -----------------------------------------------------------------------
# Faculty Requests
# -----------------------------------------------------------------------
@app.route("/api/requests", methods=["POST"])
def api_submit_request():
    d = request.get_json() or {}
    user = session.get("user", {})
    faculty_name    = user.get("name", d.get("faculty_name", ""))
    faculty_email   = user.get("email", d.get("faculty_email", ""))
    request_type    = d.get("request_type", "change_request")
    schedule_id     = d.get("schedule_id")
    requested_date  = d.get("requested_date", date.today().isoformat())
    requested_slot  = d.get("requested_timeslot", "")
    requested_room  = d.get("requested_classroom", "")
    pref_section    = d.get("preferred_section", "")
    reason          = d.get("reason", "").strip()

    if not reason:
        return jsonify({"success": False, "message": "Please provide a reason"}), 400

    conn = get_db(); c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO faculty_requests
          (faculty_name, faculty_email, request_type, schedule_id, requested_date,
           requested_timeslot, requested_classroom, preferred_section, reason, status, created_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (faculty_name, faculty_email, request_type, schedule_id, requested_date,
         requested_slot, requested_room, pref_section, reason, "pending", now))
    conn.commit(); conn.close()
    return jsonify({"success": True, "message": "Your request has been submitted to the admin."})

@app.route("/api/requests", methods=["GET"])
def api_get_requests():
    status_filter = request.args.get("status", "")
    conn = get_db(); c = conn.cursor()
    if status_filter:
        c.execute("SELECT * FROM faculty_requests WHERE status=? ORDER BY created_at DESC", (status_filter,))
    else:
        c.execute("SELECT * FROM faculty_requests ORDER BY created_at DESC")
    rows = [dict(r) for r in c.fetchall()]; conn.close()
    return jsonify(rows)

@app.route("/api/requests/<int:rid>/resolve", methods=["PUT"])
def api_resolve_request(rid):
    d          = request.get_json() or {}
    action     = d.get("action", "approve")
    admin_note = d.get("admin_note", "").strip()
    status     = "approved" if action == "approve" else "rejected"
    now        = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db(); c = conn.cursor()

    c.execute("SELECT * FROM faculty_requests WHERE id=?", (rid,))
    req_row = c.fetchone()
    if not req_row:
        conn.close()
        return jsonify({"success": False, "message": "Request not found"}), 404

    clash_warning = None
    if action == "approve":
        req_type = req_row["request_type"]
        if req_type == "change_request" and req_row["schedule_id"]:
            c.execute("SELECT * FROM schedule WHERE id=?", (req_row["schedule_id"],))
            orig = c.fetchone()
            if orig:
                new_date = req_row["requested_date"] if req_row["requested_date"] else orig["date"]
                new_slot = req_row["requested_timeslot"] if req_row["requested_timeslot"] else orig["timeslot"]

                new_room_id = orig["classroom_id"]
                req_room = (req_row["requested_classroom"] or "").strip()
                if req_room:
                    c.execute("""
                        SELECT id FROM classrooms
                        WHERE LOWER(name)=LOWER(?) OR ? LIKE ('%' || name || '%')
                    """, (req_room, req_room))
                    rm_match = c.fetchone()
                    if rm_match:
                        new_room_id = rm_match["id"]

                # Run clash check
                has_clash, clash_type, clash_msg = check_clash(
                    conn, orig["section"], new_date, new_slot,
                    orig["teacher_email"], new_room_id,
                    ignore_id=orig["id"]
                )
                if has_clash:
                    clash_warning = clash_msg

                c.execute("""
                    UPDATE schedule
                    SET date=?, timeslot=?, classroom_id=?, has_clash=?, clash_reason=?
                    WHERE id=?""",
                    (new_date, new_slot, new_room_id,
                     1 if has_clash else 0, clash_msg if has_clash else None,
                     orig["id"])
                )

        elif req_type == "extra_hour":
            faculty_email = req_row["faculty_email"]
            c.execute("SELECT id FROM subjects WHERE LOWER(faculty_email)=?", (faculty_email.lower(),))
            sub_row = c.fetchone()
            subject_id = sub_row["id"] if sub_row else 1

            target_section = req_row["preferred_section"] or "MCA A"
            req_date = req_row["requested_date"] or date.today().isoformat()
            req_slot = req_row["requested_timeslot"] or TIMESLOTS[0]

            # Choose an available room
            c.execute("SELECT id FROM classrooms ORDER BY capacity DESC")
            all_rooms = [r["id"] for r in c.fetchall()]
            chosen_room = all_rooms[0] if all_rooms else 1
            for rm_id in all_rooms:
                clash, _, _ = check_clash(conn, target_section, req_date, req_slot, faculty_email, rm_id)
                if not clash:
                    chosen_room = rm_id
                    break

            has_clash, clash_type, clash_msg = check_clash(
                conn, target_section, req_date, req_slot, faculty_email, chosen_room
            )
            if has_clash:
                clash_warning = clash_msg

            c.execute("""
                INSERT INTO schedule
                  (section, date, timeslot, subject_id, classroom_id,
                   teacher_name, teacher_email, created_by, has_clash, clash_reason)
                VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (target_section, req_date, req_slot, subject_id, chosen_room,
                 req_row["faculty_name"], faculty_email, "faculty_request_approved",
                 1 if has_clash else 0, clash_msg if has_clash else None)
            )

    c.execute("UPDATE faculty_requests SET status=?, admin_note=?, resolved_at=? WHERE id=?",
              (status, admin_note, now, rid))
    conn.commit(); conn.close()
    return jsonify({
        "success": True,
        "status": status,
        "clash_warning": clash_warning,
        "message": "Schedule updated successfully!" if status == "approved" else "Request rejected."
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"\n{'='*55}\n CAMPUS TIMETABLE PORTAL  — http://localhost:{port}\n{'='*55}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
