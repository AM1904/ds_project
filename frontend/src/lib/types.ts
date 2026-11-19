export type Role = 'Admin' | 'Faculty' | 'Student';

export interface User {
  id: number; name: string; email: string; role: Role;
  section: string; department: string; phone: string; created_at: string;
}
export interface Subject {
  id: number; code: string; name: string; department: string; faculty_email: string | null;
}
export interface Classroom { id: number; name: string; capacity: number; room_type: string }
export interface FacultyUser {
  id: number; name: string; email: string; department: string; phone: string; created_at: string;
}

export interface ScheduleEntry {
  id: number; section: string; date: string; timeslot: string;
  has_clash: number; clash_reason: string | null;
  teacher_name: string; teacher_email: string;
  subject_id: number; subject_code: string; subject_name: string; subject_department: string;
  classroom_id: number; room_name: string; room_capacity: number; room_type: string;
  changed_at: string | null; changed_note: string | null;
}

export interface WeekDay {
  date: string; day_name: string; short_day: string; formatted: string;
  full_formatted: string; is_today: boolean; classes: ScheduleEntry[];
}
export interface WeekMeta {
  start_date: string; end_date: string; label: string;
  prev_week: string; next_week: string; current_week: string; selected_date: string;
}
export interface WeekData {
  week_meta: WeekMeta; days: WeekDay[]; timeslots: string[]; classes: ScheduleEntry[];
}

export type RequestType = 'change_request' | 'extra_hour';
export type RequestStatus = 'pending' | 'approved' | 'rejected' | 'cancelled';
export interface FacultyRequest {
  id: number; faculty_name: string; faculty_email: string;
  request_type: RequestType; schedule_id: number | null;
  requested_date: string; requested_timeslot: string; requested_classroom: string;
  preferred_section: string; reason: string; status: RequestStatus;
  admin_note: string | null; created_at: string; resolved_at: string | null;
  class_section: string | null; class_date: string | null; class_timeslot: string | null;
  class_subject: string | null; class_room: string | null;
  can_revert: number;
}

export interface EntryPayload {
  section: string; date: string; timeslot: string;
  subject_id: number; classroom_id: number;
  teacher_name: string; teacher_email: string;
  allow_clash?: boolean;
}
export interface EntryResult {
  success: boolean; entry: ScheduleEntry; has_clash: boolean; clash_type: string | null; message: string;
}
export interface SlotAvailability { section_busy: boolean; teacher_busy: boolean; busy_rooms: number[] }
export interface Availability { slots: Record<string, SlotAvailability> }

export const SECTION_STRENGTHS: Record<string, number> = {
  'MCA A': 42,
  'MCA B': 36,
  'MCA C': 40,
  'MCA D': 35,
};

export interface RoomSuggestionResult {
  success: boolean;
  section: string;
  strength: number;
  suggested_classroom: Classroom | null;
  unused_seats: number | null;
  available_classrooms: Array<Classroom & { is_best_fit: boolean; unused_seats: number; fits: boolean }>;
  algorithm: {
    name: string;
    sorting: string;
    searching: string;
    objective: string;
  };
}
