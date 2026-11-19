import type {
  Availability, Classroom, EntryPayload, EntryResult, FacultyRequest, FacultyUser,
  ScheduleEntry, Subject, User, WeekData, RequestType, RoomSuggestionResult,
} from './types';

export class ApiError extends Error {
  status: number;
  data: any;
  constructor(message: string, status: number, data: any) {
    super(message);
    this.status = status;
    this.data = data;
  }
  /** Server asked the caller to confirm saving a clashing class (HTTP 409). */
  get needsConfirm() { return !!this.data?.needs_confirm; }
}

async function call<T>(method: string, url: string, body?: unknown): Promise<T> {
  let res: Response;
  try {
    res = await fetch(url, {
      method,
      headers: body === undefined ? undefined : { 'Content-Type': 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
      credentials: 'same-origin',
    });
  } catch {
    throw new ApiError('Cannot reach the server. Is it running?', 0, null);
  }
  let data: any = null;
  try { data = await res.json(); } catch { /* non-JSON error page */ }
  if (!res.ok || data?.success === false) {
    throw new ApiError(data?.message ?? `Something went wrong (${res.status}).`, res.status, data);
  }
  return data as T;
}
const get = <T>(url: string) => call<T>('GET', url);
const qs = (o: Record<string, string | undefined>) => {
  const q = new URLSearchParams();
  Object.entries(o).forEach(([k, v]) => { if (v) q.set(k, v); });
  const s = q.toString();
  return s ? `?${s}` : '';
};

export const api = {
  // auth
  me: () => get<{ authenticated: boolean; user: User | null }>('/api/auth/me'),
  login: (email: string, password: string) => call<{ user: User }>('POST', '/api/auth/login', { email, password }),
  register: (b: { name: string; email: string; password: string; role: string; section?: string; department?: string; phone?: string }) =>
    call<{ user: User }>('POST', '/api/auth/register', b),
  logout: () => call<{ success: boolean }>('POST', '/api/auth/logout'),
  updateProfile: (b: { name: string; phone: string; department: string; section: string }) =>
    call<{ user: User }>('PUT', '/api/auth/profile', b),

  // reference data
  subjects: () => get<Subject[]>('/api/subjects'),
  classrooms: () => get<Classroom[]>('/api/classrooms'),
  timeslots: () => get<string[]>('/api/timeslots'),
  sections: () => get<string[]>('/api/sections'),
  facultyUsers: () => get<FacultyUser[]>('/api/users/faculty'),

  // schedule
  weekly: (p: { date?: string; section?: string; teacher_email?: string }) =>
    get<WeekData>(`/api/weekly-schedule${qs(p)}`),
  schedule: (p: { section?: string; date?: string } = {}) =>
    get<ScheduleEntry[]>(`/api/schedule${qs(p)}`),
  facultyDay: (teacher_email: string, date: string) =>
    get<ScheduleEntry[]>(`/api/faculty-schedule${qs({ teacher_email, date })}`),
  entry: (id: number) => get<{ entry: ScheduleEntry }>(`/api/schedule/${id}`),
  createEntry: (b: EntryPayload) => call<EntryResult>('POST', '/api/schedule/create', b),
  updateEntry: (id: number, b: EntryPayload) => call<EntryResult>('PUT', `/api/schedule/${id}`, b),
  deleteEntry: (id: number) => call<{ success: boolean }>('DELETE', `/api/schedule/${id}`),
  availability: (p: { date: string; section: string; teacher_email?: string }) =>
    get<Availability>(`/api/availability${qs(p)}`),
  suggestClassroom: (p: { section?: string; date?: string; timeslot?: string; ignore_id?: number }) =>
    get<RoomSuggestionResult>(`/api/classrooms/suggest${qs({
      section: p.section,
      date: p.date,
      timeslot: p.timeslot,
      ignore_id: p.ignore_id ? String(p.ignore_id) : undefined,
    })}`),

  // requests
  requests: (p: { status?: string; faculty_email?: string } = {}) =>
    get<FacultyRequest[]>(`/api/requests${qs(p)}`),
  submitRequest: (b: {
    request_type: RequestType; reason: string; schedule_id?: number | null;
    requested_date?: string; requested_timeslot?: string; requested_classroom?: string; preferred_section?: string;
  }) => call<{ message: string }>('POST', '/api/requests', b),
  resolveRequest: (id: number, action: 'approve' | 'reject', admin_note: string) =>
    call<{ status: string; message: string }>('PUT', `/api/requests/${id}/resolve`, { action, admin_note }),
  cancelRequest: (id: number) => call<{ status: string }>('PUT', `/api/requests/${id}/cancel`),
  revertRequest: (id: number) => call<{ message?: string }>('PUT', `/api/requests/${id}/revert`),
};
