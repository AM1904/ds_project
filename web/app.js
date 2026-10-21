/**
 * Campus Timetable Portal — Frontend Controller
 * Complete implementation supporting Student, Faculty, and Admin roles.
 */

// Global State
let currentUser = null;
let allSubjects = [];
let allClassrooms = [];
let allTimeslots = [];
let allFaculty = [];          // registered Faculty users from /api/users/faculty
let selectedSubjectId = null;
let selectedFacultyEmail = null;
let selectedFacultyName = null;
let adminCurrentDate = '';
let adminCurrentSection = 'MCA A';
let facultyCurrentDate = '';
let selectedClassForChange = null;

// ---------------------------------------------------------------------------
// INITIALIZATION
// ---------------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', () => {
  setupAuthEvents();
  setupQuickLogins();
  setupRoleToggle();
  checkSession();
});

// ---------------------------------------------------------------------------
// AUTH & SESSION MANAGEMENT
// ---------------------------------------------------------------------------
async function checkSession() {
  try {
    const res = await fetch('/api/auth/me');
    const data = await res.json();
    if (data.authenticated && data.user) {
      currentUser = data.user;
      enterPortal();
    } else {
      showAuthScreen();
    }
  } catch {
    showAuthScreen();
  }
}

function showAuthScreen() {
  document.getElementById('authScreen').style.display = 'flex';
  document.getElementById('appScreen').style.display = 'none';
}

function setupAuthEvents() {
  // Tabs
  document.getElementById('tabLoginBtn').addEventListener('click', () => switchAuthTab('login'));
  document.getElementById('tabRegisterBtn').addEventListener('click', () => switchAuthTab('register'));

  // Sign In Form
  document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value.trim();
    await doLogin(email, password);
  });

  // Register Form
  document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('regName').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const password = document.getElementById('regPassword').value.trim();
    const role = document.getElementById('regRole').value;
    const section = document.getElementById('regSection').value;
    const deptEl = document.getElementById('regDept');
    const department = deptEl ? deptEl.value.trim() : '';
    const phone = document.getElementById('regPhone').value.trim();

    const submitBtn = e.target.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Creating account...';

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, role, section, department, phone })
      });
      const data = await res.json();
      if (data.success) {
        currentUser = data.user;
        enterPortal();
      } else {
        showFormAlert('registerAlert', data.message || 'Registration failed', 'error');
      }
    } catch {
      showFormAlert('registerAlert', 'Connection error. Please try again.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Register & Sign In';
    }
  });

  // Logout
  document.getElementById('logoutBtn').addEventListener('click', doLogout);
}

function switchAuthTab(tab) {
  const loginForm = document.getElementById('loginForm');
  const registerForm = document.getElementById('registerForm');
  const tabLogin = document.getElementById('tabLoginBtn');
  const tabRegister = document.getElementById('tabRegisterBtn');

  if (tab === 'login') {
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
    tabLogin.classList.add('active');
    tabRegister.classList.remove('active');
  } else {
    loginForm.style.display = 'none';
    registerForm.style.display = 'block';
    tabLogin.classList.remove('active');
    tabRegister.classList.add('active');
  }
}

function setupRoleToggle() {
  document.getElementById('regRole').addEventListener('change', (e) => {
    const role = e.target.value;
    document.getElementById('regSectionGroup').style.display = (role === 'Student') ? 'block' : 'none';
    document.getElementById('regDeptGroup').style.display = (role === 'Faculty' || role === 'Admin') ? 'block' : 'none';
  });
}

function setupQuickLogins() {
  // Admin always exists (seeded). Students/Faculty must register first.
  const btn_A     = document.getElementById('quickStudentA');
  const btn_B     = document.getElementById('quickStudentB');
  const btn_admin = document.getElementById('quickAdmin');

  if (btn_A) btn_A.addEventListener('click', () => {
    showToast('Register a Student account with section MCA A, then use Sign In.', 'info');
    switchAuthTab('register');
  });

  if (btn_B) btn_B.addEventListener('click', () => {
    showToast('Register a Student account with section MCA B, then use Sign In.', 'info');
    switchAuthTab('register');
  });

  if (btn_admin) btn_admin.addEventListener('click', () => {
    document.getElementById('loginEmail').value    = 'admin@college.edu';
    document.getElementById('loginPassword').value = 'admin123';
    switchAuthTab('login');
    doLogin('admin@college.edu', 'admin123');
  });
}

async function doLogin(email, password) {
  const submitBtn = document.querySelector('#loginForm button[type="submit"]');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Signing in...';
  hideFormAlert('loginAlert');

  try {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();
    if (data.success) {
      currentUser = data.user;
      enterPortal();
    } else {
      showFormAlert('loginAlert', data.message || 'Invalid credentials.', 'error');
    }
  } catch {
    showFormAlert('loginAlert', 'Cannot reach server. Please ensure Flask is running.', 'error');
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Sign In';
  }
}

async function doLogout() {
  await fetch('/api/auth/logout', { method: 'POST' });
  currentUser = null;
  showAuthScreen();
  showToast('Signed out successfully', 'info');
}

// ---------------------------------------------------------------------------
// PORTAL SETUP (POST LOGIN)
// ---------------------------------------------------------------------------
async function enterPortal() {
  document.getElementById('authScreen').style.display = 'none';
  document.getElementById('appScreen').style.display = 'block';

  updateHeaderUI();
  setupNavigation();
  setupProfileModal();

  // Load shared metadata
  await Promise.all([loadSubjects(), loadClassrooms(), loadTimeslots(), loadFacultyList()]);

  // Route to the appropriate role screen
  const role = currentUser.role;
  if (role === 'Student') {
    showView('student');
    initStudentView();
  } else if (role === 'Faculty') {
    showView('faculty');
    initFacultyView();
  } else if (role === 'Admin') {
    showView('adminTimetable');
    initAdminTimetableView();
    loadPendingRequestsCount();
  }
}

function updateHeaderUI() {
  const name = currentUser.name || 'User';
  const role = currentUser.role || 'Student';
  const section = currentUser.section;
  const initials = name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);

  document.getElementById('userAvatar').textContent = initials;
  document.getElementById('navUserName').textContent = name;
  document.getElementById('navUserSub').textContent = role === 'Student' ? (section || 'Student') : role;
  document.getElementById('userRoleBadge').textContent =
    role === 'Admin' ? 'Admin Portal' : role === 'Faculty' ? 'Faculty Portal' : 'Student Portal';

  // Role-based Nav items
  document.getElementById('navStudentBtn').style.display = (role === 'Student' || role === 'Admin') ? 'flex' : 'none';
  document.getElementById('navFacultyBtn').style.display = (role === 'Faculty' || role === 'Admin') ? 'flex' : 'none';
  document.getElementById('navAdminTimetableBtn').style.display = (role === 'Admin') ? 'flex' : 'none';
  document.getElementById('navAdminRequestsBtn').style.display = (role === 'Admin') ? 'flex' : 'none';
}

function setupNavigation() {
  const navButtons = [
    { id: 'navStudentBtn', view: 'student', init: initStudentView },
    { id: 'navFacultyBtn', view: 'faculty', init: initFacultyView },
    { id: 'navAdminTimetableBtn', view: 'adminTimetable', init: initAdminTimetableView },
    { id: 'navAdminRequestsBtn', view: 'adminRequests', init: initAdminRequestsView },
  ];

  navButtons.forEach(({ id, view, init }) => {
    const btn = document.getElementById(id);
    if (btn) {
      btn.addEventListener('click', () => {
        showView(view);
        init();
      });
    }
  });
}

function showView(viewName) {
  // Update nav buttons active state
  const viewToNav = {
    'student': 'navStudentBtn',
    'faculty': 'navFacultyBtn',
    'adminTimetable': 'navAdminTimetableBtn',
    'adminRequests': 'navAdminRequestsBtn',
  };

  document.querySelectorAll('.portal-nav-links .nav-link').forEach(btn => btn.classList.remove('active'));
  const activeBtn = document.getElementById(viewToNav[viewName]);
  if (activeBtn) activeBtn.classList.add('active');

  // Hide all panels, show requested one
  document.querySelectorAll('.view-panel').forEach(panel => {
    panel.style.display = 'none';
    panel.classList.remove('active');
  });

  const targetPanel = document.getElementById(`view-${viewName}`);
  if (targetPanel) {
    targetPanel.style.display = 'block';
    targetPanel.classList.add('active');
  }
}

// ---------------------------------------------------------------------------
// REFERENCE DATA LOADERS
// ---------------------------------------------------------------------------
async function loadSubjects() {
  try {
    const res = await fetch('/api/subjects');
    allSubjects = await res.json();
  } catch {
    allSubjects = [];
  }
}

async function loadFacultyList() {
  try {
    const res = await fetch('/api/users/faculty');
    allFaculty = await res.json();
  } catch {
    allFaculty = [];
  }
}

async function loadClassrooms() {
  try {
    const res = await fetch('/api/classrooms');
    allClassrooms = await res.json();
    populateClassroomSelects();
  } catch {
    allClassrooms = [];
  }
}

async function loadTimeslots() {
  try {
    const res = await fetch('/api/timeslots');
    allTimeslots = await res.json();
    populateTimeslotSelects();
  } catch {
    allTimeslots = [];
  }
}

function populateClassroomSelects() {
  const selects = ['adminClassroom', 'reqNewClassroom'];
  selects.forEach(selectId => {
    const sel = document.getElementById(selectId);
    if (!sel) return;
    const isOptional = selectId.startsWith('req');
    sel.innerHTML = isOptional ? '<option value="">— No preference —</option>' : '';
    allClassrooms.forEach(cr => {
      const opt = document.createElement('option');
      opt.value = cr.id;
      opt.textContent = `${cr.name} (${cr.capacity} seats · ${cr.room_type})`;
      sel.appendChild(opt);
    });
  });
}

function populateTimeslotSelects() {
  const selects = [
    { id: 'adminTimeslot', hasEmpty: false },
    { id: 'reqNewTimeslot', hasEmpty: true, emptyText: '— No preference —' },
    { id: 'reqExtraTimeslot', hasEmpty: true, emptyText: '— Select timeslot —' },
  ];

  selects.forEach(({ id, hasEmpty, emptyText }) => {
    const sel = document.getElementById(id);
    if (!sel) return;
    sel.innerHTML = hasEmpty ? `<option value="">${emptyText}</option>` : '';
    allTimeslots.forEach(ts => {
      const opt = document.createElement('option');
      opt.value = ts;
      opt.textContent = ts;
      sel.appendChild(opt);
    });
  });
}

// ---------------------------------------------------------------------------
// 1. STUDENT VIEW — 3-DAY TIMETABLE
// ---------------------------------------------------------------------------
function initStudentView() {
  const sectionSelect = document.getElementById('studentSectionSelect');
  if (currentUser && currentUser.role === 'Student' && currentUser.section) {
    sectionSelect.value = currentUser.section;
  }

  // Remove existing listeners by cloning or just re-assigning handler
  sectionSelect.onchange = (e) => loadStudentSchedule(e.target.value);
  loadStudentSchedule(sectionSelect.value);
}

async function loadStudentSchedule(section) {
  const label = document.getElementById('studentSectionLabel');
  if (label) label.textContent = section;

  const grid = document.getElementById('studentDayGrid');
  grid.innerHTML = '<div style="padding:40px;text-align:center;color:#64748b;">Loading 3-day schedule...</div>';

  try {
    const res = await fetch(`/api/student-schedule?section=${encodeURIComponent(section)}`);
    const data = await res.json();
    renderStudentDays(data.days);
  } catch {
    grid.innerHTML = '<div style="padding:40px;text-align:center;color:#dc2626;">Could not load student schedule.</div>';
  }
}

function renderStudentDays(days) {
  const grid = document.getElementById('studentDayGrid');
  grid.innerHTML = '';

  days.forEach((dayData, idx) => {
    const card = document.createElement('div');
    card.className = 'day-schedule-card';

    const isToday = idx === 0;
    const headerClass = isToday ? 'day-card-header today-hdr' : 'day-card-header';

    card.innerHTML = `
      <div class="${headerClass}">
        <div class="day-label">${dayData.meta.label}</div>
        <div class="day-name">${dayData.meta.day_name}</div>
        <div class="day-date">${dayData.meta.formatted}</div>
      </div>
      <div class="day-card-body"></div>
    `;

    const body = card.querySelector('.day-card-body');

    if (!dayData.has_classes) {
      body.innerHTML = `
        <div class="no-timetable-state">
          <span class="no-tt-icon">📭</span>
          <div class="no-tt-text">No classes scheduled</div>
          <div class="no-tt-sub">No timetable for this day yet.</div>
        </div>
      `;
    } else {
      dayData.classes.forEach(cls => {
        const isClash = cls.has_clash === 1;
        const item = document.createElement('div');
        item.className = `class-item ${isClash ? 'has-clash' : ''}`;

        item.innerHTML = `
          <div class="class-time">
            <span class="time-range">${cls.timeslot.replace(' - ', '<br>')}</span>
          </div>
          <div class="class-info">
            <div class="class-subject">
              <span class="class-subject-code">${cls.subject_code}</span>${cls.subject_name}
            </div>
            <div class="class-teacher">👤 ${cls.teacher_name} <span style="color:#94a3b8;font-size:12px;">(${cls.teacher_designation})</span></div>
            <div class="class-room">
              <span>📍 ${cls.room_name}</span>
            </div>
            ${isClash ? `
              <span class="clash-pill">⚠ Conflict</span>
              <span class="clash-reason-text">${cls.clash_reason}</span>
            ` : ''}
          </div>
        `;
        body.appendChild(item);
      });
    }

    grid.appendChild(card);
  });
}

// ---------------------------------------------------------------------------
// 2. FACULTY VIEW — SCHEDULE & REQUESTS
// ---------------------------------------------------------------------------
function initFacultyView() {
  const datePicker = document.getElementById('facultyDatePicker');
  if (!datePicker.value) {
    const today = new Date().toISOString().split('T')[0];
    datePicker.value = today;
  }
  facultyCurrentDate = datePicker.value;

  datePicker.onchange = (e) => {
    facultyCurrentDate = e.target.value;
    loadFacultySchedule();
  };

  setupFacultyRequestForm();
  loadFacultySchedule();
  loadMyRequestsList();
}

async function loadFacultySchedule() {
  const dateStr = facultyCurrentDate;
  const teacherEmail = currentUser ? currentUser.email : '';

  const label = document.getElementById('facultyDateLabel');
  if (label) {
    const dateObj = new Date(dateStr + 'T00:00:00');
    label.textContent = `Teaching schedule for ${dateObj.toLocaleDateString('en-IN', { weekday: 'long', day: 'numeric', month: 'short', year: 'numeric' })}`;
  }

  const container = document.getElementById('facultyClassList');
  const countBadge = document.getElementById('facultyClassCount');
  container.innerHTML = '<div style="padding:30px;text-align:center;color:#64748b;">Loading your classes...</div>';

  try {
    const res = await fetch(`/api/faculty-schedule?teacher_email=${encodeURIComponent(teacherEmail)}&date=${dateStr}`);
    const classes = await res.json();

    countBadge.textContent = `${classes.length} ${classes.length === 1 ? 'class' : 'classes'}`;
    container.innerHTML = '';

    if (classes.length === 0) {
      container.innerHTML = `
        <div class="empty-faculty-day">
          <span class="empty-faculty-icon">☕</span>
          <strong>No classes scheduled today</strong>
          <p style="font-size:13px;margin-top:4px;color:#94a3b8;">Enjoy your free time or request an extra session on the right.</p>
        </div>
      `;
      return;
    }

    classes.forEach(cls => {
      const isClash = cls.has_clash === 1;
      const card = document.createElement('div');
      card.className = `faculty-class-card ${isClash ? 'has-clash' : ''}`;
      card.dataset.id = cls.id;

      card.innerHTML = `
        <div class="fcc-top">
          <span class="fcc-timeslot">${cls.timeslot}</span>
          <span class="fcc-code">${cls.subject_code}</span>
        </div>
        <div class="fcc-subject">${cls.subject_name}</div>
        <div class="fcc-meta">
          <span>👥 Section: <strong>${cls.section}</strong></span>
          <span>📍 <strong>${cls.room_name}</strong></span>
        </div>
        ${isClash ? `<div class="clash-reason-text">⚠ ${cls.clash_reason}</div>` : ''}
        <div class="select-hint">👆 Click to select for schedule change request</div>
      `;

      card.addEventListener('click', () => {
        document.querySelectorAll('.faculty-class-card').forEach(c => c.classList.remove('selected-for-request'));
        card.classList.add('selected-for-request');
        selectClassForChange(cls);
      });

      container.appendChild(card);
    });
  } catch {
    container.innerHTML = '<div style="padding:30px;text-align:center;color:#dc2626;">Error loading classes.</div>';
  }
}

function selectClassForChange(cls) {
  selectedClassForChange = cls;
  document.getElementById('reqScheduleId').value = cls.id;

  const preview = document.getElementById('selectedClassPreview');
  preview.innerHTML = `
    <div class="preview-filled">
      <strong>Selected Class:</strong> ${cls.subject_name} (${cls.section})<br>
      <span style="color:#64748b;">📅 ${cls.date} · ⏰ ${cls.timeslot} · 📍 ${cls.room_name}</span>
    </div>
  `;

  // Switch request tab to change_request if not already
  switchRequestType('change_request');
}

function setupFacultyRequestForm() {
  const btnChange = document.getElementById('reqTypeChangeBtn');
  const btnExtra = document.getElementById('reqTypeExtraBtn');

  btnChange.onclick = () => switchRequestType('change_request');
  btnExtra.onclick = () => switchRequestType('extra_hour');

  // Today default for extra hour date
  const extraDate = document.getElementById('reqExtraDate');
  if (extraDate && !extraDate.value) {
    extraDate.value = new Date().toISOString().split('T')[0];
  }

  // Handle submit
  const form = document.getElementById('facultyRequestForm');
  form.onsubmit = async (e) => {
    e.preventDefault();
    const requestType = document.getElementById('reqType').value;
    const scheduleId = document.getElementById('reqScheduleId').value || null;
    const reason = document.getElementById('reqReason').value.trim();

    if (!reason) {
      showFormAlert('requestFormAlert', 'Please provide a reason for your request.', 'error');
      return;
    }

    if (requestType === 'change_request' && !scheduleId) {
      showFormAlert('requestFormAlert', 'Please select a class from the left first.', 'error');
      return;
    }

    const payload = {
      request_type: requestType,
      faculty_name: currentUser.name,
      faculty_email: currentUser.email,
      reason: reason
    };

    if (requestType === 'change_request') {
      payload.schedule_id = parseInt(scheduleId);
      const newDateVal = document.getElementById('reqNewDate') ? document.getElementById('reqNewDate').value : '';
      payload.requested_date = newDateVal || (selectedClassForChange ? selectedClassForChange.date : facultyCurrentDate);
      payload.requested_timeslot = document.getElementById('reqNewTimeslot').value;
      const roomSelect = document.getElementById('reqNewClassroom');
      const selectedRoom = allClassrooms.find(r => r.id == roomSelect.value);
      payload.requested_classroom = selectedRoom ? selectedRoom.name : (roomSelect.value ? roomSelect.options[roomSelect.selectedIndex].text : '');
    } else {
      payload.requested_date = document.getElementById('reqExtraDate').value;
      payload.requested_timeslot = document.getElementById('reqExtraTimeslot').value;
      payload.preferred_section = document.getElementById('reqExtraSection').value;
    }

    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Submitting...';

    try {
      const res = await fetch('/api/requests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success) {
        showToast('Request submitted to Admin!', 'success');
        form.reset();
        selectedClassForChange = null;
        document.getElementById('reqScheduleId').value = '';
        document.getElementById('selectedClassPreview').innerHTML =
          '<span class="preview-hint">👆 Click a class on the left to select it for a change request</span>';
        hideFormAlert('requestFormAlert');
        loadMyRequestsList();
      } else {
        showFormAlert('requestFormAlert', data.message || 'Failed to submit request.', 'error');
      }
    } catch {
      showFormAlert('requestFormAlert', 'Network error. Please try again.', 'error');
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Submit Request';
    }
  };
}

function switchRequestType(type) {
  document.getElementById('reqType').value = type;
  const isChange = (type === 'change_request');

  document.getElementById('reqTypeChangeBtn').classList.toggle('active', isChange);
  document.getElementById('reqTypeExtraBtn').classList.toggle('active', !isChange);

  document.getElementById('changeRequestFields').style.display = isChange ? 'block' : 'none';
  document.getElementById('extraHourFields').style.display = !isChange ? 'block' : 'none';
}

async function loadMyRequestsList() {
  const container = document.getElementById('myRequestsList');
  if (!container) return;

  try {
    const res = await fetch('/api/requests');
    const all = await res.json();
    const myRequests = all.filter(r => r.faculty_email === currentUser.email);

    if (myRequests.length === 0) {
      container.innerHTML = '<div class="no-requests-msg">You have not submitted any requests yet.</div>';
      return;
    }

    container.innerHTML = '';
    myRequests.forEach(req => {
      const item = document.createElement('div');
      item.className = 'request-history-item';

      const typeLabel = req.request_type === 'change_request' ? 'Schedule Change' : 'Extra Hour Request';

      item.innerHTML = `
        <div class="rhi-header">
          <span class="rhi-type">${typeLabel}</span>
          <span class="rhi-status ${req.status}">${req.status.toUpperCase()}</span>
        </div>
        <div class="rhi-reason">"${req.reason}"</div>
        <div class="rhi-date">📅 Requested for: <strong>${req.requested_date}</strong> ${req.requested_timeslot ? `(${req.requested_timeslot})` : ''} · Submitted on: ${req.created_at}</div>
        ${req.admin_note ? `<div class="rhi-note"><strong>Admin Response:</strong> ${req.admin_note}</div>` : ''}
      `;
      container.appendChild(item);
    });
  } catch {
    container.innerHTML = '<div class="no-requests-msg">Could not load requests history.</div>';
  }
}

// ---------------------------------------------------------------------------
// 3. ADMIN VIEW A — MANAGE TIMETABLE
// ---------------------------------------------------------------------------
function initAdminTimetableView() {
  const dateInput = document.getElementById('adminDate');
  if (!dateInput.value) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
  }
  adminCurrentDate = dateInput.value;
  adminCurrentSection = document.getElementById('adminSection').value;

  // Chip buttons
  document.querySelectorAll('.quick-date-buttons .btn-chip').forEach(chip => {
    chip.onclick = () => {
      const offset = parseInt(chip.dataset.offset || 0);
      const d = new Date();
      d.setDate(d.getDate() + offset);
      const dateStr = d.toISOString().split('T')[0];
      dateInput.value = dateStr;
      adminCurrentDate = dateStr;

      document.querySelectorAll('.quick-date-buttons .btn-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      refreshAdminDayPreview();
    };
  });

  dateInput.onchange = (e) => {
    adminCurrentDate = e.target.value;
    refreshAdminDayPreview();
  };

  document.getElementById('adminSection').onchange = (e) => {
    adminCurrentSection = e.target.value;
    refreshAdminDayPreview();
  };

  document.getElementById('btnAdminAddClass').onclick = adminAddClass;

  document.getElementById('adminOverviewFilter').onchange = (e) => {
    loadAdminOverviewSchedule(e.target.value);
  };

  renderSubjectPicker();
  refreshAdminDayPreview();
  loadAdminOverviewSchedule('ALL');
}

function renderSubjectPicker() {
  const grid = document.getElementById('adminSubjectPicker');
  grid.innerHTML = '';
  selectedSubjectId = null;
  selectedFacultyEmail = null;
  selectedFacultyName = null;
  document.getElementById('adminSelectedSubject').value = '';

  allSubjects.forEach(sub => {
    const card = document.createElement('div');
    card.className = 'subject-pick-card';
    card.dataset.id = sub.id;

    // Look up the assigned faculty name from allFaculty list
    const assignedFac = allFaculty.find(f => f.email === sub.faculty_email);
    const teacherLine = assignedFac
      ? `<div class="subj-assigned-teacher">👤 ${assignedFac.name}</div>`
      : '';

    card.innerHTML = `
      <div class="subj-code">${sub.code}</div>
      <div class="subj-name">${sub.name}</div>
      <div class="subj-credits">${sub.credits} credits · ${sub.department}</div>
      ${teacherLine}
    `;

    card.addEventListener('click', () => {
      document.querySelectorAll('#adminSubjectPicker .subject-pick-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      selectedSubjectId = sub.id;
      document.getElementById('adminSelectedSubject').value = sub.id;
      document.getElementById('adminClashBanner').style.display = 'none';
      // Auto-suggest the subject's assigned teacher in Step 3
      renderFacultyPicker(sub.faculty_email || '');
    });

    grid.appendChild(card);
  });
}

function renderFacultyPicker(suggestedEmail = '') {
  const grid = document.getElementById('adminFacultyPicker');
  if (!grid) return;
  grid.innerHTML = '';

  // Only reset selection state if no suggestion (fresh call without a subject)
  if (!suggestedEmail) {
    selectedFacultyEmail = null;
    selectedFacultyName = null;
  }

  if (allFaculty.length === 0) {
    grid.innerHTML = `
      <div style="padding:16px;text-align:center;color:#dc2626;font-size:13px;grid-column:1/-1;">
        <strong>No faculty registered yet.</strong><br>
        <span style="color:#94a3b8;">Ask faculty members to register an account first, then assign them here.</span>
      </div>`;
    return;
  }

  allFaculty.forEach(fac => {
    const card = document.createElement('div');
    card.className = 'subject-pick-card';
    card.dataset.email = fac.email;

    const initials = fac.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
    const isAssigned = suggestedEmail && fac.email.toLowerCase() === suggestedEmail.toLowerCase();

    card.innerHTML = `
      <div class="subj-teacher-card" style="margin:0;">
        <div class="teacher-avatar-sm" style="${isAssigned ? 'background:linear-gradient(135deg,#2563eb,#7c3aed);' : ''}">${initials}</div>
        <div class="teacher-info-mini">
          <span class="teacher-name-mini">${fac.name}${isAssigned ? ' <span class="assigned-badge">Assigned</span>' : ''}</span>
          <span class="teacher-desig-mini">${fac.department}</span>
        </div>
      </div>
      <div class="subj-credits" style="margin-top:6px;">${fac.email}</div>
    `;

    // Auto-select the suggested teacher
    if (isAssigned) {
      card.classList.add('selected');
      selectedFacultyEmail = fac.email;
      selectedFacultyName = fac.name;
    }

    card.addEventListener('click', () => {
      document.querySelectorAll('#adminFacultyPicker .subject-pick-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      selectedFacultyEmail = fac.email;
      selectedFacultyName = fac.name;
      document.getElementById('adminClashBanner').style.display = 'none';
    });

    grid.appendChild(card);
  });
}

async function refreshAdminDayPreview() {
  const section = adminCurrentSection;
  const dateStr = adminCurrentDate;
  const subtitle = document.getElementById('adminPreviewSubtitle');
  const badge = document.getElementById('adminPreviewBadge');
  const timeline = document.getElementById('adminDayTimeline');

  if (!dateStr) {
    timeline.innerHTML = '<div class="empty-preview-state">Select a date</div>';
    return;
  }

  const dateObj = new Date(dateStr + 'T00:00:00');
  subtitle.textContent = `${section} — ${dateObj.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short' })}`;

  try {
    const res = await fetch(`/api/schedule?section=${encodeURIComponent(section)}&date=${dateStr}`);
    const rows = await res.json();

    const clashCount = rows.filter(r => r.has_clash === 1).length;
    badge.textContent = `${rows.length} ${rows.length === 1 ? 'Class' : 'Classes'}${clashCount > 0 ? ` · ${clashCount} ⚠` : ''}`;
    badge.className = clashCount > 0 ? 'badge danger-badge' : 'badge';

    timeline.innerHTML = '';
    if (rows.length === 0) {
      timeline.innerHTML = `
        <div class="empty-preview-state">
          <span class="empty-preview-icon">📅</span>
          No classes scheduled for this day & section.<br>
          <small style="color:#94a3b8">Use the form to add one.</small>
        </div>
      `;
      return;
    }

    rows.forEach(r => {
      const isClash = r.has_clash === 1;
      const block = document.createElement('div');
      block.className = `preview-class-block ${isClash ? 'clash-block' : ''}`;

      block.innerHTML = `
        <div class="preview-timeslot">${r.timeslot}</div>
        <div class="preview-subj">${r.subject_name}</div>
        <div class="preview-teacher">👤 ${r.teacher_name}</div>
        <div class="preview-room">📍 ${r.room_name}</div>
        ${isClash ? `<div class="preview-clash-note">⚠ ${r.clash_reason}</div>` : ''}
        <button class="preview-delete-btn" title="Delete class" data-id="${r.id}">✕</button>
      `;

      block.querySelector('.preview-delete-btn').addEventListener('click', async (e) => {
        e.stopPropagation();
        await deleteScheduleEntry(r.id);
      });

      timeline.appendChild(block);
    });
  } catch {
    timeline.innerHTML = '<div class="empty-preview-state" style="color:#dc2626">Error loading day preview</div>';
  }
}

async function adminAddClass() {
  const section = document.getElementById('adminSection').value;
  const dateStr = document.getElementById('adminDate').value;
  const timeslot = document.getElementById('adminTimeslot').value;
  const classroomId = document.getElementById('adminClassroom').value;
  const subjectId = document.getElementById('adminSelectedSubject').value;

  if (!dateStr) { showToast('Please select a date first (Step 1)', 'error'); return; }
  if (!subjectId) { showToast('Please select a subject (Step 2)', 'error'); return; }
  if (!selectedFacultyEmail) { showToast('Please select a faculty member (Step 3)', 'error'); return; }
  if (!timeslot) { showToast('Please select a timeslot (Step 4)', 'error'); return; }
  if (!classroomId) { showToast('Please select a classroom (Step 4)', 'error'); return; }

  const btn = document.getElementById('btnAdminAddClass');
  btn.disabled = true;
  btn.textContent = 'Adding to Timetable...';

  try {
    const res = await fetch('/api/schedule/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        section,
        date: dateStr,
        timeslot,
        subject_id: parseInt(subjectId),
        classroom_id: parseInt(classroomId),
        teacher_name: selectedFacultyName,
        teacher_email: selectedFacultyEmail
      })
    });
    const data = await res.json();

    if (data.success) {
      if (data.has_clash) {
        document.getElementById('adminClashMsg').textContent = data.message;
        document.getElementById('adminClashBanner').style.display = 'flex';
        showToast('Class added, but a clash was detected (highlighted in red)!', 'error');
      } else {
        document.getElementById('adminClashBanner').style.display = 'none';
        showToast('Class successfully scheduled!', 'success');
      }
      refreshAdminDayPreview();
      loadAdminOverviewSchedule(document.getElementById('adminOverviewFilter').value);
    } else {
      showToast(data.message || 'Could not schedule class', 'error');
    }
  } catch {
    showToast('Network error while scheduling class', 'error');
  } finally {
    btn.disabled = false;
    btn.innerHTML = '➕ Add to Timetable';
  }
}

async function deleteScheduleEntry(entryId) {
  try {
    const res = await fetch(`/api/schedule/${entryId}`, { method: 'DELETE' });
    const data = await res.json();
    if (data.success) {
      showToast('Class removed from schedule', 'info');
      refreshAdminDayPreview();
      loadAdminOverviewSchedule(document.getElementById('adminOverviewFilter').value);
    }
  } catch {
    showToast('Failed to delete class', 'error');
  }
}

async function loadAdminOverviewSchedule(filterSection = 'ALL') {
  const tbody = document.getElementById('adminOverviewBody');
  tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:24px;color:#64748b;">Loading full schedule...</td></tr>';

  try {
    const url = filterSection === 'ALL' ? '/api/schedule' : `/api/schedule?section=${encodeURIComponent(filterSection)}`;
    const res = await fetch(url);
    const rows = await res.json();

    if (rows.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:30px;color:#94a3b8;">No classes found.</td></tr>';
      return;
    }

    tbody.innerHTML = '';
    rows.forEach(row => {
      const isClash = row.has_clash === 1;
      const tr = document.createElement('tr');
      if (isClash) tr.style.background = '#fef2f2';

      const dateObj = new Date(row.date + 'T00:00:00');
      const dateFormatted = dateObj.toLocaleDateString('en-IN', { weekday: 'short', day: 'numeric', month: 'short' });

      tr.innerHTML = `
        <td><strong>${dateFormatted}</strong><br><span style="font-size:11px;color:#94a3b8;">${row.date}</span></td>
        <td><span style="font-weight:700;color:#2563eb;">${row.section}</span></td>
        <td><span style="font-size:13px;font-weight:600;">${row.timeslot}</span></td>
        <td><strong>${row.subject_name}</strong><br><span style="font-size:11px;color:#94a3b8;">${row.subject_code}</span></td>
        <td>${row.teacher_name}<br><span style="font-size:11px;color:#94a3b8;">${row.teacher_designation}</span></td>
        <td>${row.room_name}</td>
        <td>
          ${isClash
            ? `<span class="status-clash">⚠ Clash<br><span style="font-size:11px;font-weight:400">${row.clash_reason}</span></span>`
            : '<span class="status-ok">✓ Clear</span>'
          }
        </td>
        <td>
          <button class="btn btn-danger-sm" data-id="${row.id}">Remove</button>
        </td>
      `;

      tr.querySelector('button').addEventListener('click', () => deleteScheduleEntry(row.id));
      tbody.appendChild(tr);
    });
  } catch {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;padding:24px;color:#dc2626;">Error loading schedule table.</td></tr>';
  }
}

// ---------------------------------------------------------------------------
// 4. ADMIN VIEW B — FACULTY REQUESTS
// ---------------------------------------------------------------------------
function initAdminRequestsView() {
  const filterSelect = document.getElementById('requestStatusFilter');
  filterSelect.onchange = (e) => loadAdminRequests(e.target.value);
  loadAdminRequests(filterSelect.value);
  loadPendingRequestsCount();
}

async function loadPendingRequestsCount() {
  const badge = document.getElementById('pendingReqCount');
  if (!badge) return;
  try {
    const res = await fetch('/api/requests?status=pending');
    const rows = await res.json();
    if (rows.length > 0) {
      badge.textContent = rows.length;
      badge.style.display = 'inline-flex';
    } else {
      badge.style.display = 'none';
    }
  } catch {
    badge.style.display = 'none';
  }
}

async function loadAdminRequests(statusFilter = '') {
  const container = document.getElementById('adminRequestsList');
  container.innerHTML = '<div style="padding:40px;text-align:center;color:#64748b;">Loading requests...</div>';

  try {
    const url = statusFilter ? `/api/requests?status=${encodeURIComponent(statusFilter)}` : '/api/requests';
    const res = await fetch(url);
    const requests = await res.json();

    if (requests.length === 0) {
      container.innerHTML = `
        <div class="no-requests-state">
          <span class="no-req-icon">📬</span>
          <strong>No requests found</strong>
          <p style="font-size:13px;margin-top:4px;">There are no ${statusFilter ? statusFilter : ''} requests at this time.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = '';
    requests.forEach(req => {
      const card = document.createElement('div');
      card.className = 'admin-request-card';

      const isPending = req.status === 'pending';
      const typeLabel = req.request_type === 'change_request' ? 'Schedule Change' : 'Extra Hour Request';

      card.innerHTML = `
        <div class="arc-header">
          <div class="arc-meta">
            <div class="arc-faculty-name">🧑‍🏫 ${req.faculty_name}</div>
            <span class="arc-type-pill ${req.request_type}">${typeLabel}</span>
            <span class="arc-status-badge ${req.status}">${req.status.toUpperCase()}</span>
          </div>
          <span style="font-size:12px;color:#94a3b8;">Submitted: ${req.created_at}</span>
        </div>

        <div class="arc-body">
          <div class="arc-field">
            <label>Requested Date &amp; Timeslot</label>
            <p>📅 ${req.requested_date} ${req.requested_timeslot ? `· ⏰ ${req.requested_timeslot}` : '(Any timeslot)'}</p>
          </div>
          <div class="arc-field">
            <label>${req.request_type === 'change_request' ? 'Preferred Classroom' : 'Target Section'}</label>
            <p>${req.requested_classroom || req.preferred_section || 'No specific preference'}</p>
          </div>
        </div>

        <div class="arc-reason-box">
          <span class="arc-reason-label">Faculty Reason</span>
          "${req.reason}"
        </div>

        ${req.admin_note ? `
          <div class="arc-admin-note">
            <strong>Admin Note (${req.resolved_at}):</strong> ${req.admin_note}
          </div>
        ` : ''}

        ${isPending ? `
          <div class="arc-actions">
            <input type="text" class="arc-note-input" placeholder="Add an admin note or instructions (optional)...">
            <button class="btn btn-success-sm btn-approve" data-id="${req.id}">✓ Approve</button>
            <button class="btn btn-danger-sm btn-reject" data-id="${req.id}">✕ Reject</button>
          </div>
        ` : ''}
      `;

      if (isPending) {
        const noteInput = card.querySelector('.arc-note-input');
        card.querySelector('.btn-approve').addEventListener('click', () => {
          resolveFacultyRequest(req.id, 'approve', noteInput.value.trim());
        });
        card.querySelector('.btn-reject').addEventListener('click', () => {
          resolveFacultyRequest(req.id, 'reject', noteInput.value.trim());
        });
      }

      container.appendChild(card);
    });
  } catch {
    container.innerHTML = '<div style="padding:40px;text-align:center;color:#dc2626;">Error loading requests.</div>';
  }
}

async function resolveFacultyRequest(requestId, action, adminNote) {
  try {
    const res = await fetch(`/api/requests/${requestId}/resolve`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action, admin_note: adminNote })
    });
    const data = await res.json();
    if (data.success) {
      const msg = data.message || `Request ${action === 'approve' ? 'approved & schedule updated' : 'rejected'}!`;
      showToast(msg, data.clash_warning ? 'info' : 'success');
      loadAdminRequests(document.getElementById('requestStatusFilter').value);
      loadPendingRequestsCount();
      // Instantly refresh timetable views across the app
      if (typeof refreshAdminDayPreview === 'function') refreshAdminDayPreview();
      const overviewFilter = document.getElementById('adminOverviewFilter');
      if (typeof loadAdminOverviewSchedule === 'function' && overviewFilter) {
        loadAdminOverviewSchedule(overviewFilter.value);
      }
      if (typeof loadFacultySchedule === 'function') loadFacultySchedule();
      if (typeof loadStudentSchedule === 'function') loadStudentSchedule();
    } else {
      showToast(data.message || 'Could not resolve request', 'error');
    }
  } catch {
    showToast('Network error resolving request', 'error');
  }
}

// ---------------------------------------------------------------------------
// 5. PROFILE MODAL
// ---------------------------------------------------------------------------
function setupProfileModal() {
  document.getElementById('openProfileBtn').onclick = openProfile;
  document.getElementById('closeProfileBtn').onclick = closeProfile;
  document.getElementById('modalLogoutBtn').onclick = () => {
    closeProfile();
    doLogout();
  };

  document.getElementById('profileModal').addEventListener('click', (e) => {
    if (e.target.id === 'profileModal') closeProfile();
  });

  document.getElementById('profileForm').onsubmit = async (e) => {
    e.preventDefault();
    const name = document.getElementById('modalFullName').value.trim();
    const phone = document.getElementById('modalPhone').value.trim();
    const section = document.getElementById('modalSection').value;
    const department = document.getElementById('modalDept').value.trim();

    try {
      const res = await fetch('/api/auth/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: currentUser.id, name, phone, section, department })
      });
      const data = await res.json();
      if (data.success) {
        currentUser = data.user;
        updateHeaderUI();
        showFormAlert('profileAlert', 'Profile updated successfully!', 'success');
        showToast('Profile saved!', 'success');
      } else {
        showFormAlert('profileAlert', data.message || 'Failed to update profile', 'error');
      }
    } catch {
      showFormAlert('profileAlert', 'Connection error saving profile.', 'error');
    }
  };
}

function openProfile() {
  if (!currentUser) return;
  const u = currentUser;

  const initials = u.name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
  document.getElementById('modalAvatar').textContent = initials;
  document.getElementById('modalName').textContent = u.name;
  document.getElementById('modalRole').textContent = u.role;
  document.getElementById('modalEmail').value = u.email;
  document.getElementById('modalFullName').value = u.name;
  document.getElementById('modalPhone').value = u.phone || '';
  document.getElementById('modalSection').value = u.section || 'MCA A';
  document.getElementById('modalDept').value = u.department || '';
  document.getElementById('modalCreatedAt').textContent = u.created_at || '—';

  const isStudent = (u.role === 'Student');
  document.getElementById('modalSectionGroup').style.display = isStudent ? 'block' : 'none';
  document.getElementById('modalDeptGroup').style.display = !isStudent ? 'block' : 'none';

  hideFormAlert('profileAlert');
  document.getElementById('profileModal').style.display = 'flex';
}

function closeProfile() {
  document.getElementById('profileModal').style.display = 'none';
}

// ---------------------------------------------------------------------------
// NOTIFICATIONS & UI HELPERS
// ---------------------------------------------------------------------------
function showFormAlert(id, message, type) {
  const el = document.getElementById(id);
  if (!el) return;
  el.textContent = message;
  el.className = `form-alert ${type}`;
  el.style.display = 'block';
}

function hideFormAlert(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  const icon = type === 'success' ? '✓' : type === 'error' ? '⚠' : 'ℹ';
  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.25s ease';
    setTimeout(() => toast.remove(), 250);
  }, 3200);
}
