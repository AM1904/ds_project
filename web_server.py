# -*- coding: utf-8 -*-
"""
Campus Timetable Portal — Backend
Roles:
  - Admin:   Creates timetable, manages schedule, approves/rejects faculty requests
  - Faculty: Views own day schedule, submits change requests and extra-hour requests
  - Student: Views the weekly timetable for their class section

Teacher data comes from REGISTERED FACULTY ACCOUNTS in the users table.
No hardcoded teachers in subjects — subjects are just courses; teachers are assigned per schedule slot.
"""
import os
import sqlite3
from datetime import datetime, date, timedelta
from flask import Flask, request, jsonify, send_from_directory, session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE  = os.path.join(BASE_DIR, "portal_data.db")

DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")
app = Flask(__name__, static_folder=None)
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
    # guarded migrations for existing databases
    for table, cols in (("faculty_requests", ("prev_date TEXT", "prev_timeslot TEXT", "prev_classroom_id INTEGER", "created_schedule_id INTEGER")),
                        ("schedule", ("changed_at TEXT", "changed_note TEXT"))):
        have = {r["name"] for r in conn.execute(f"PRAGMA table_info({table})")}
        for col in cols:
            if col.split()[0] not in have:
                c.execute(f"ALTER TABLE {table} ADD COLUMN {col}")
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
@app.route("/<path:path>")
def index(path=""):
    """Serve the built React app; unknown non-API paths fall back to index.html (client-side routing)."""
    if path.startswith("api/"):
        return jsonify({"success": False, "message": "Not found"}), 404
    full = os.path.join(DIST_DIR, path)
    if path and os.path.isfile(full):
        return send_from_directory(DIST_DIR, path)
    if not os.path.isfile(os.path.join(DIST_DIR, "index.html")):
        return ("Frontend not built. Run: cd frontend && npm install && npm run build", 503)
    return send_from_directory(DIST_DIR, "index.html")

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
    if role not in ("Student", "Faculty"):
        role = "Student"
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
    if role != "Student":
        section = ""
    elif not section:
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
    cur = session.get("user")
    if not cur:
        return jsonify({"success": False, "message": "Please sign in again."}), 401
    d = request.get_json(silent=True) or {}
    name  = (d.get("name") or "").strip()
    phone = (d.get("phone") or "").strip()
    dept  = (d.get("department") or "").strip() or cur.get("department", "")
    sect  = cur.get("section", "")  # students cannot change section
    if not name:
        return jsonify({"success": False, "message": "Name is required"}), 400
    conn = get_db(); c = conn.cursor()
    c.execute("UPDATE users SET name=?,phone=?,section=?,department=? WHERE id=?", (name, phone, sect, dept, cur["id"]))
    if name != cur["name"]:  # keep denormalised names in sync
        c.execute("UPDATE schedule SET teacher_name=? WHERE LOWER(teacher_email)=?", (name, cur["email"].lower()))
        c.execute("UPDATE faculty_requests SET faculty_name=? WHERE LOWER(faculty_email)=?", (name, cur["email"].lower()))
    conn.commit()
    c.execute("SELECT * FROM users WHERE id=?", (cur["id"],))
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
SLOT_ORDER_SQL = "CASE s.timeslot " + " ".join(
    f"WHEN '{t}' THEN {i}" for i, t in enumerate(TIMESLOTS)) + " ELSE 99 END"

def parse_day(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None

def is_past(date_str):
    """Days before today are read-only history."""
    return bool(date_str) and date_str < date.today().isoformat()

def validate_slot(date_str, timeslot, section=None):
    dt = parse_day(date_str)
    if not dt:
        return "Pick a valid date."
    if dt.weekday() > 4:
        return "Classes run Monday to Friday only."
    if is_past(date_str):
        return "Past dates can't be scheduled."
    if timeslot not in TIMESLOTS:
        return "Pick one of the listed timeslots."
    if section is not None and section not in SECTIONS:
        return "Unknown section."
    return None

def _slot_rows(conn, date_str, timeslot):
    cur = conn.execute("""
        SELECT s.id, s.section, s.teacher_name, s.teacher_email, s.classroom_id,
               sub.name AS subject_name, cr.name AS room_name
        FROM schedule s
        JOIN subjects sub ON s.subject_id=sub.id
        JOIN classrooms cr ON s.classroom_id=cr.id
        WHERE s.date=? AND s.timeslot=?""", (date_str, timeslot))
    return [dict(r) for r in cur.fetchall()]

def _find_conflict(me, others):
    me_teacher = (me["teacher_email"] or me["teacher_name"] or "").lower()
    for o in others:
        if o["classroom_id"] == me["classroom_id"]:
            return "room", f"Classroom clash: {me['room_name']} is also booked for {o['section']} ({o['subject_name']})."
        if me_teacher and me_teacher == (o["teacher_email"] or o["teacher_name"] or "").lower():
            return "teacher", f"Teacher clash: {o['teacher_name']} is also teaching {o['subject_name']} for {o['section']} at this time."
        if o["section"] == me["section"]:
            return "section", f"Section clash: {me['section']} also has {o['subject_name']} in this timeslot."
    return None, None

def check_clash(conn, section, date_str, timeslot, teacher_email, classroom_id, ignore_id=None, teacher_name=""):
    rm = conn.execute("SELECT name FROM classrooms WHERE id=?", (classroom_id,)).fetchone()
    me = {"section": section, "teacher_email": teacher_email, "teacher_name": teacher_name,
          "classroom_id": classroom_id, "room_name": rm["name"] if rm else ""}
    others = [o for o in _slot_rows(conn, date_str, timeslot) if o["id"] != ignore_id]
    ctype, msg = _find_conflict(me, others)
    return ctype is not None, ctype, (msg or "No clash")

def refresh_clashes(conn, *slots):
    """Recompute has_clash for every row in the given (date, timeslot) slots, so flags never go stale."""
    for date_str, timeslot in set(slots):
        rows = _slot_rows(conn, date_str, timeslot)
        for r in rows:
            ctype, msg = _find_conflict(r, [o for o in rows if o["id"] != r["id"]])
            conn.execute("UPDATE schedule SET has_clash=?, clash_reason=? WHERE id=?",
                         (1 if ctype else 0, msg, r["id"]))

def _clash_type(reason):
    if not reason: return None
    return {"Classroom": "room", "Teacher": "teacher", "Section": "section"}.get(reason.split(" ")[0])

def _read_entry(d):
    try:
        subject_id = int(d.get("subject_id") or 0)
        classroom_id = int(d.get("classroom_id") or 0)
    except (TypeError, ValueError):
        return None, "Invalid subject or classroom."
    e = {"section": (d.get("section") or "").strip(), "date": (d.get("date") or "").strip(),
         "timeslot": (d.get("timeslot") or "").strip(), "subject_id": subject_id, "classroom_id": classroom_id,
         "teacher_name": (d.get("teacher_name") or "").strip(),
         "teacher_email": (d.get("teacher_email") or "").strip().lower()}
    if not all([e["section"], e["date"], e["timeslot"], subject_id, classroom_id, e["teacher_name"]]):
        return None, "All fields including teacher are required"
    err = validate_slot(e["date"], e["timeslot"], e["section"])
    return (None, err) if err else (e, None)

def _refs_exist(conn, e):
    return (conn.execute("SELECT 1 FROM subjects WHERE id=?", (e["subject_id"],)).fetchone()
            and conn.execute("SELECT 1 FROM classrooms WHERE id=?", (e["classroom_id"],)).fetchone())

def _refresh_all_clashes():
    conn = get_db()
    slots = conn.execute("SELECT DISTINCT date, timeslot FROM schedule").fetchall()
    refresh_clashes(conn, *[(r["date"], r["timeslot"]) for r in slots])
    conn.commit(); conn.close()

def _moved_note(date_str, timeslot, room_name):
    return f"Moved from {parse_day(date_str).strftime('%a %d %b')} {timeslot}, {room_name}"

def _needs_confirm(conn, e, d, ignore_id=None):
    """409 response when the entry clashes and the caller has not sent allow_clash; else None."""
    if d.get("allow_clash"):
        return None
    has_clash, ctype, msg = check_clash(conn, e["section"], e["date"], e["timeslot"], e["teacher_email"],
                                        e["classroom_id"], ignore_id=ignore_id, teacher_name=e["teacher_name"])
    if not has_clash:
        return None
    return jsonify({"success": False, "needs_confirm": True, "has_clash": True,
                    "clash_type": ctype, "message": msg}), 409

@app.route("/api/availability")
def api_availability():
    date_str = request.args.get("date", "")
    section = request.args.get("section", "")
    email = request.args.get("teacher_email", "").strip().lower()
    dt = parse_day(date_str)
    if not dt or dt.weekday() > 4:
        return jsonify({"success": False, "message": "Pick a valid weekday date."}), 400
    conn = get_db()
    rows = conn.execute("SELECT section, timeslot, teacher_email, classroom_id FROM schedule WHERE date=?", (date_str,)).fetchall()
    conn.close()
    slots = {}
    for t in TIMESLOTS:
        at = [r for r in rows if r["timeslot"] == t]
        slots[t] = {"section_busy": any(r["section"] == section for r in at),
                    "teacher_busy": bool(email) and any((r["teacher_email"] or "").lower() == email for r in at),
                    "busy_rooms": [r["classroom_id"] for r in at]}
    return jsonify({"slots": slots})

_refresh_all_clashes()

# -----------------------------------------------------------------------
# Schedule CRUD
# -----------------------------------------------------------------------
def _full_schedule_query(where="", params=None):
    return (f"""
        SELECT s.id, s.section, s.date, s.timeslot, s.has_clash, s.clash_reason, s.changed_at, s.changed_note,
               s.teacher_name, s.teacher_email,
               sub.id AS subject_id, sub.code AS subject_code, sub.name AS subject_name,
               sub.department AS subject_department,
               cr.id AS classroom_id, cr.name AS room_name, cr.capacity AS room_capacity, cr.room_type
        FROM schedule s
        JOIN subjects sub ON s.subject_id=sub.id
        JOIN classrooms cr ON s.classroom_id=cr.id
        {where}
        ORDER BY s.date ASC, {SLOT_ORDER_SQL}""", params or [])

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

def _entry(conn, eid):
    q, params = _full_schedule_query("WHERE s.id=?", [eid])
    return dict(conn.execute(q, params).fetchone())

@app.route("/api/schedule/create", methods=["POST"])
def api_create_schedule():
    d = request.get_json(silent=True) or {}
    e, err = _read_entry(d)
    if err:
        return jsonify({"success": False, "message": err}), 400
    conn = get_db()
    if not _refs_exist(conn, e):
        conn.close()
        return jsonify({"success": False, "message": "Unknown subject or classroom."}), 400
    dup = conn.execute("""SELECT 1 FROM schedule WHERE section=? AND date=? AND timeslot=? AND subject_id=?
                          AND classroom_id=? AND LOWER(teacher_name)=LOWER(?)""",
                       (e["section"], e["date"], e["timeslot"], e["subject_id"], e["classroom_id"], e["teacher_name"])).fetchone()
    if dup:
        conn.close()
        return jsonify({"success": False, "message": "This exact class is already scheduled."}), 409
    needs = _needs_confirm(conn, e, d)
    if needs:
        conn.close()
        return needs
    created_by = (session.get("user") or {}).get("email", "admin")
    cur = conn.execute("""
        INSERT INTO schedule (section, date, timeslot, subject_id, classroom_id,
                              teacher_name, teacher_email, created_by, has_clash, clash_reason)
        VALUES (?,?,?,?,?,?,?,?,0,NULL)""",
        (e["section"], e["date"], e["timeslot"], e["subject_id"], e["classroom_id"],
         e["teacher_name"], e["teacher_email"], created_by))
    eid = cur.lastrowid
    refresh_clashes(conn, (e["date"], e["timeslot"]))
    conn.commit()
    entry = _entry(conn, eid); conn.close()
    return jsonify({
        "success": True, "entry": entry,
        "has_clash": bool(entry["has_clash"]),
        "clash_type": _clash_type(entry["clash_reason"]),
        "message": entry["clash_reason"] or "Class scheduled successfully!"
    })

@app.route("/api/schedule/<int:eid>", methods=["DELETE"])
def api_delete_schedule(eid):
    conn = get_db()
    old = conn.execute("SELECT date, timeslot FROM schedule WHERE id=?", (eid,)).fetchone()
    if not old:
        conn.close()
        return jsonify({"success": False, "message": "That class no longer exists. Refresh the page."}), 404
    if is_past(old["date"]):
        conn.close()
        return jsonify({"success": False, "message": "Past classes can't be removed."}), 400
    conn.execute("DELETE FROM schedule WHERE id=?", (eid,))
    refresh_clashes(conn, (old["date"], old["timeslot"]))
    conn.commit(); conn.close()
    return jsonify({"success": True})

@app.route("/api/schedule/<int:eid>", methods=["GET"])
def api_get_schedule_entry(eid):
    conn = get_db()
    q, params = _full_schedule_query("WHERE s.id=?", [eid])
    row = conn.execute(q, params).fetchone()
    conn.close()
    if not row:
        return jsonify({"success": False, "message": "Entry not found"}), 404
    entry = dict(row)
    return jsonify({"success": True, "entry": entry, **entry})

@app.route("/api/schedule/<int:eid>", methods=["PUT"])
def api_update_schedule(eid):
    d = request.get_json(silent=True) or {}
    conn = get_db()
    old = conn.execute("SELECT date, timeslot, classroom_id, teacher_email FROM schedule WHERE id=?", (eid,)).fetchone()
    if not old:
        conn.close()
        return jsonify({"success": False, "message": "That class no longer exists. Refresh the page."}), 404
    if is_past(old["date"]):
        conn.close()
        return jsonify({"success": False, "message": "Past classes can't be changed."}), 400
    e, err = _read_entry(d)
    if err:
        conn.close()
        return jsonify({"success": False, "message": err}), 400
    if not _refs_exist(conn, e):
        conn.close()
        return jsonify({"success": False, "message": "Unknown subject or classroom."}), 400
    needs = _needs_confirm(conn, e, d, ignore_id=eid)
    if needs:
        conn.close()
        return needs
    changed = (old["date"], old["timeslot"], old["classroom_id"], (old["teacher_email"] or "").lower()) != \
              (e["date"], e["timeslot"], e["classroom_id"], e["teacher_email"])
    note_sql, note_args = "", []
    if changed:
        old_room = conn.execute("SELECT name FROM classrooms WHERE id=?", (old["classroom_id"],)).fetchone()
        note_sql = ", changed_at=?, changed_note=?"
        note_args = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     _moved_note(old["date"], old["timeslot"], old_room["name"] if old_room else "")]
    conn.execute(f"""
        UPDATE schedule
        SET section=?, date=?, timeslot=?, subject_id=?, classroom_id=?, teacher_name=?, teacher_email=?{note_sql}
        WHERE id=?""",
        [e["section"], e["date"], e["timeslot"], e["subject_id"], e["classroom_id"],
         e["teacher_name"], e["teacher_email"], *note_args, eid])
    refresh_clashes(conn, (old["date"], old["timeslot"]), (e["date"], e["timeslot"]))
    conn.commit()
    entry = _entry(conn, eid); conn.close()
    return jsonify({
        "success": True, "entry": entry,
        "has_clash": bool(entry["has_clash"]),
        "clash_type": _clash_type(entry["clash_reason"]),
        "message": entry["clash_reason"] or "Schedule entry updated successfully!"
    })

# -----------------------------------------------------------------------
# Faculty: own day schedule (matched by teacher_email in schedule table)
# -----------------------------------------------------------------------
@app.route("/api/faculty-schedule")
def api_faculty_schedule():
    teacher_email = request.args.get("teacher_email", "").strip().lower()
    date_str      = request.args.get("date", date.today().isoformat())
    if not teacher_email:
        return jsonify([])
    conn = get_db()
    q, params = _full_schedule_query("WHERE s.date=? AND LOWER(s.teacher_email)=?", [date_str, teacher_email])
    rows = [dict(r) for r in conn.execute(q, params).fetchall()]; conn.close()
    return jsonify(rows)

# -----------------------------------------------------------------------
# Weekly Timetable Grid API (for Faculty, Students & Admin)
# -----------------------------------------------------------------------
@app.route("/api/weekly-schedule")
def api_weekly_schedule():
    date_param    = request.args.get("date", "").strip()
    section       = request.args.get("section", "").strip()
    teacher_email = request.args.get("teacher_email", "").strip().lower()

    if not date_param:
        ref_date = date.today()
    else:
        try:
            ref_date = datetime.strptime(date_param, "%Y-%m-%d").date()
        except Exception:
            ref_date = date.today()

    monday = ref_date - timedelta(days=ref_date.weekday())
    friday = monday + timedelta(days=4)

    conn = get_db()
    where_clauses = ["s.date >= ?", "s.date <= ?"]
    params = [monday.isoformat(), friday.isoformat()]

    if section and section != "ALL":
        where_clauses.append("s.section = ?")
        params.append(section)

    if teacher_email:
        where_clauses.append("LOWER(s.teacher_email) = ?")
        params.append(teacher_email)

    q, q_params = _full_schedule_query("WHERE " + " AND ".join(where_clauses), params)
    classes = [dict(r) for r in conn.execute(q, q_params).fetchall()]
    conn.close()

    days = []
    for i in range(5):
        d = monday + timedelta(days=i)
        days.append({
            "date": d.isoformat(),
            "day_name": d.strftime("%A"),
            "short_day": d.strftime("%a"),
            "formatted": d.strftime("%d %b"),
            "full_formatted": d.strftime("%A, %d %b %Y"),
            "is_today": (d == date.today()),
            "classes": [c for c in classes if c["date"] == d.isoformat()],
        })

    return jsonify({
        "week_meta": {
            "start_date": monday.isoformat(),
            "end_date": friday.isoformat(),
            "label": f"Week of {monday.strftime('%d %b')} – {friday.strftime('%d %b %Y')}",
            "prev_week": (monday - timedelta(days=7)).isoformat(),
            "next_week": (monday + timedelta(days=7)).isoformat(),
            "current_week": (date.today() - timedelta(days=date.today().weekday())).isoformat(),
            "selected_date": ref_date.isoformat(),
        },
        "days": days,
        "timeslots": TIMESLOTS,
        "classes": classes
    })

# -----------------------------------------------------------------------
# Faculty Requests
# -----------------------------------------------------------------------
def _find_room(conn, text):
    row = conn.execute("SELECT id FROM classrooms WHERE LOWER(name)=LOWER(?)", (text,)).fetchone()
    if not row:
        row = conn.execute("SELECT id FROM classrooms WHERE ? LIKE ('%' || name || '%')", (text,)).fetchone()
    return row["id"] if row else None

def _subject_for(conn, email):
    return conn.execute("SELECT id FROM subjects WHERE LOWER(faculty_email)=?", ((email or "").lower(),)).fetchone()

@app.route("/api/requests", methods=["POST"])
def api_submit_request():
    d = request.get_json(silent=True) or {}
    user = session.get("user") or {}
    faculty_name    = user.get("name") or d.get("faculty_name", "")
    faculty_email   = (user.get("email") or d.get("faculty_email") or "").strip().lower()
    request_type    = d.get("request_type", "change_request")
    schedule_id     = d.get("schedule_id")
    requested_date  = (d.get("requested_date") or "").strip()
    requested_slot  = (d.get("requested_timeslot") or "").strip()
    requested_room  = (d.get("requested_classroom") or "").strip()
    pref_section    = (d.get("preferred_section") or "").strip()
    reason          = (d.get("reason") or "").strip()

    def bad(msg, code=400):
        return jsonify({"success": False, "message": msg}), code

    if not faculty_email:
        return bad("Please sign in again.", 401)
    if not reason:
        return bad("Please provide a reason")
    if request_type not in ("change_request", "extra_hour"):
        return bad("Unknown request type")
    today = date.today().isoformat()
    if requested_date and requested_date < today:
        return bad("Choose a date that is not in the past.")

    conn = get_db(); c = conn.cursor()
    try:
        if request_type == "change_request":
            orig = c.execute("SELECT teacher_email, date FROM schedule WHERE id=?", (schedule_id,)).fetchone() if schedule_id else None
            if not orig:
                return bad("Please select a class from the left first.")
            if (orig["teacher_email"] or "").lower() != faculty_email:
                return bad("You can only request changes to your own classes.")
            if is_past(orig["date"]):
                return bad("That class is in the past and can't be changed.")
            if not (requested_date or requested_slot or requested_room):
                return bad("Choose a new date, timeslot or classroom.")
            if requested_date or requested_slot:
                if requested_date and (not parse_day(requested_date) or parse_day(requested_date).weekday() > 4):
                    return bad("Pick a valid weekday date (Monday to Friday).")
                if requested_slot and requested_slot not in TIMESLOTS:
                    return bad("Pick one of the listed timeslots.")
            if requested_room and _find_room(c, requested_room) is None:
                return bad("Unknown classroom.")
        else:
            err = validate_slot(requested_date, requested_slot, pref_section)
            if err:
                return bad(err)
            if not _subject_for(c, faculty_email):
                return bad("No subject is assigned to you yet. Ask the admin to assign one.")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("""
            INSERT INTO faculty_requests
              (faculty_name, faculty_email, request_type, schedule_id, requested_date,
               requested_timeslot, requested_classroom, preferred_section, reason, status, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (faculty_name, faculty_email, request_type, schedule_id, requested_date,
             requested_slot, requested_room, pref_section, reason, "pending", now))
        conn.commit()
    finally:
        conn.close()
    return jsonify({"success": True, "message": "Your request has been submitted to the admin."})

@app.route("/api/requests", methods=["GET"])
def api_get_requests():
    where, params = [], []
    if request.args.get("status"):
        where.append("fr.status=?"); params.append(request.args["status"])
    if request.args.get("faculty_email"):
        where.append("LOWER(fr.faculty_email)=?"); params.append(request.args["faculty_email"].strip().lower())
    conn = get_db()
    rows = conn.execute(f"""
        SELECT fr.*, s.section AS class_section, s.date AS class_date, s.timeslot AS class_timeslot,
               sub.name AS class_subject, cr.name AS class_room,
               CASE WHEN fr.status='approved' AND (fr.prev_date IS NOT NULL OR fr.created_schedule_id IS NOT NULL)
                    THEN 1 ELSE 0 END AS can_revert
        FROM faculty_requests fr
        LEFT JOIN schedule s ON s.id=fr.schedule_id
        LEFT JOIN subjects sub ON sub.id=s.subject_id
        LEFT JOIN classrooms cr ON cr.id=s.classroom_id
        {"WHERE " + " AND ".join(where) if where else ""}
        ORDER BY fr.created_at DESC""", params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/requests/<int:rid>/cancel", methods=["PUT"])
def api_cancel_request(rid):
    user = session.get("user") or {}
    conn = get_db()
    row = conn.execute("SELECT faculty_email, status FROM faculty_requests WHERE id=?", (rid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"success": False, "message": "Request not found"}), 404
    if (row["faculty_email"] or "").lower() != (user.get("email") or "").lower():
        conn.close()
        return jsonify({"success": False, "message": "You can only cancel your own requests."}), 403
    if row["status"] != "pending":
        conn.close()
        return jsonify({"success": False, "message": f"This request was already {row['status']}."}), 409
    conn.execute("UPDATE faculty_requests SET status='cancelled', resolved_at=? WHERE id=?",
                 (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), rid))
    conn.commit(); conn.close()
    return jsonify({"success": True, "status": "cancelled"})

@app.route("/api/requests/<int:rid>/revert", methods=["PUT"])
def api_revert_request(rid):
    conn = get_db(); c = conn.cursor()
    req_row = c.execute("SELECT * FROM faculty_requests WHERE id=?", (rid,)).fetchone()
    if not req_row:
        conn.close()
        return jsonify({"success": False, "message": "Request not found"}), 404
    if req_row["status"] != "approved" or (req_row["prev_date"] is None and req_row["created_schedule_id"] is None):
        conn.close()
        return jsonify({"success": False, "message": "This request cannot be reverted."}), 409

    def refuse(msg):
        conn.close()
        return jsonify({"success": False, "message": msg}), 409

    if req_row["request_type"] == "change_request":
        cur = c.execute("SELECT * FROM schedule WHERE id=?", (req_row["schedule_id"],)).fetchone()
        if not cur:
            return refuse("Cannot revert, that class no longer exists.")
        if is_past(cur["date"]) or is_past(req_row["prev_date"]):
            return refuse("Cannot revert, that class is in the past.")
        has_clash, _, msg = check_clash(conn, cur["section"], req_row["prev_date"], req_row["prev_timeslot"], cur["teacher_email"],
                                        req_row["prev_classroom_id"], ignore_id=cur["id"], teacher_name=cur["teacher_name"])
        if has_clash:
            return refuse(f"Cannot revert, the old slot would clash. {msg}")
        c.execute("UPDATE schedule SET date=?, timeslot=?, classroom_id=?, changed_at=NULL, changed_note=NULL WHERE id=?",
                  (req_row["prev_date"], req_row["prev_timeslot"], req_row["prev_classroom_id"], cur["id"]))
        refresh_clashes(conn, (cur["date"], cur["timeslot"]), (req_row["prev_date"], req_row["prev_timeslot"]))
    else:
        cur = c.execute("SELECT date, timeslot FROM schedule WHERE id=?", (req_row["created_schedule_id"],)).fetchone()
        if cur:
            if is_past(cur["date"]):
                return refuse("Cannot revert, that class is in the past.")
            c.execute("DELETE FROM schedule WHERE id=?", (req_row["created_schedule_id"],))
            refresh_clashes(conn, (cur["date"], cur["timeslot"]))
    c.execute("""UPDATE faculty_requests SET status='pending', admin_note=?, resolved_at=NULL, prev_date=NULL,
                 prev_timeslot=NULL, prev_classroom_id=NULL, created_schedule_id=NULL WHERE id=?""",
              ("Reverted by admin. Needs a new decision.", rid))
    conn.commit(); conn.close()
    return jsonify({"success": True, "status": "pending", "message": "Approval reverted. The request is pending again."})

@app.route("/api/requests/<int:rid>/resolve", methods=["PUT"])
def api_resolve_request(rid):
    d          = request.get_json(silent=True) or {}
    action     = d.get("action", "approve")
    admin_note = (d.get("admin_note") or "").strip()
    if action not in ("approve", "reject"):
        return jsonify({"success": False, "message": "Unknown action"}), 400
    if action == "reject" and not admin_note:
        return jsonify({"success": False, "message": "Add a note explaining the rejection."}), 400
    status = "approved" if action == "approve" else "rejected"
    now    = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db(); c = conn.cursor()

    req_row = c.execute("SELECT * FROM faculty_requests WHERE id=?", (rid,)).fetchone()
    if not req_row:
        conn.close()
        return jsonify({"success": False, "message": "Request not found"}), 404
    if req_row["status"] != "pending":
        conn.close()
        return jsonify({"success": False, "message": f"This request was already {req_row['status']}."}), 409

    prev, created_id = (None, None, None), None

    def refuse(msg):
        c.execute("UPDATE faculty_requests SET admin_note=? WHERE id=?", ("Could not apply: " + msg, rid))
        conn.commit(); conn.close()
        return jsonify({"success": False, "message": msg}), 409

    if action == "approve":
        if req_row["request_type"] == "change_request":
            orig = c.execute("SELECT * FROM schedule WHERE id=?", (req_row["schedule_id"],)).fetchone()
            if not orig:
                return refuse("That class no longer exists. Reject this request instead.")
            if is_past(orig["date"]):
                return refuse("That class is in the past and can't be changed. Reject this request instead.")
            new_date = req_row["requested_date"] or orig["date"]
            new_slot = req_row["requested_timeslot"] or orig["timeslot"]
            new_room_id = orig["classroom_id"]
            if (req_row["requested_classroom"] or "").strip():
                new_room_id = _find_room(c, req_row["requested_classroom"].strip())
                if new_room_id is None:
                    return refuse("The requested classroom was not found. Reject this request instead.")
            err = validate_slot(new_date, new_slot)
            if err:
                return refuse(err)
            has_clash, _, msg = check_clash(conn, orig["section"], new_date, new_slot, orig["teacher_email"],
                                            new_room_id, ignore_id=orig["id"], teacher_name=orig["teacher_name"])
            if has_clash:
                return refuse(f"Cannot approve, this move would clash. {msg}")
            old_room = c.execute("SELECT name FROM classrooms WHERE id=?", (orig["classroom_id"],)).fetchone()
            c.execute("UPDATE schedule SET date=?, timeslot=?, classroom_id=?, changed_at=?, changed_note=? WHERE id=?",
                      (new_date, new_slot, new_room_id, now, _moved_note(orig["date"], orig["timeslot"], old_room["name"] if old_room else ""), orig["id"]))
            prev = (orig["date"], orig["timeslot"], orig["classroom_id"])
            refresh_clashes(conn, (orig["date"], orig["timeslot"]), (new_date, new_slot))
        else:  # extra_hour
            email = req_row["faculty_email"].lower()
            sub_row = _subject_for(c, email)
            if not sub_row:
                return refuse("No subject is assigned to this teacher. Reject this request instead.")
            section, req_date, req_slot = req_row["preferred_section"], req_row["requested_date"], req_row["requested_timeslot"]
            err = validate_slot(req_date, req_slot, section)
            if err:
                return refuse(err)
            # room 0 matches no classroom, so this finds only teacher/section clashes
            has_clash, _, msg = check_clash(conn, section, req_date, req_slot, email, 0, teacher_name=req_row["faculty_name"])
            if has_clash:
                return refuse(f"Cannot approve, it would clash. {msg}")
            chosen_room = None
            for r in c.execute("SELECT id FROM classrooms ORDER BY capacity DESC").fetchall():
                if not check_clash(conn, section, req_date, req_slot, email, r["id"], teacher_name=req_row["faculty_name"])[0]:
                    chosen_room = r["id"]; break
            if chosen_room is None:
                return refuse("Cannot approve: no classroom is free at that time.")
            created_id = c.execute("""
                INSERT INTO schedule (section, date, timeslot, subject_id, classroom_id,
                                      teacher_name, teacher_email, created_by, has_clash, clash_reason)
                VALUES (?,?,?,?,?,?,?,?,0,NULL)""",
                (section, req_date, req_slot, sub_row["id"], chosen_room,
                 req_row["faculty_name"], email, "faculty_request_approved")).lastrowid

    c.execute("UPDATE faculty_requests SET status=?, admin_note=?, resolved_at=?, prev_date=?, prev_timeslot=?, prev_classroom_id=?, created_schedule_id=? WHERE id=?",
              (status, admin_note, now, prev[0], prev[1], prev[2], created_id, rid))
    conn.commit(); conn.close()
    return jsonify({
        "success": True,
        "status": status,
        "clash_warning": None,
        "message": "Request approved and the timetable is updated." if status == "approved" else "Request rejected."
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"\n{'='*55}\n CAMPUS TIMETABLE PORTAL  — http://localhost:{port}\n{'='*55}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
