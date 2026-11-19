import { useEffect, useMemo, useState, type FormEvent } from 'react';
import { api, ApiError } from '../../lib/api';
import { useConfirm } from '../../context/Confirm';
import { useToast } from '../../context/Toast';
import { formatDay, isWeekend, toWeekday, todayISO } from '../../lib/dates';
import { SECTION_STRENGTHS, type Availability, type Classroom, type EntryPayload, type EntryResult, type ScheduleEntry } from '../../lib/types';
import type { AdminRefs } from './useAdminRefs';

/**
 * Quick Sort implementation for Classrooms sorted ascending by capacity.
 * Time Complexity: O(n log n) average.
 */
function quickSortClassrooms(rooms: Classroom[]): Classroom[] {
  if (rooms.length <= 1) return [...rooms];
  const pivot = rooms[Math.floor(rooms.length / 2)];
  const left: Classroom[] = [];
  const mid: Classroom[] = [];
  const right: Classroom[] = [];
  for (const r of rooms) {
    if (r.capacity < pivot.capacity) left.push(r);
    else if (r.capacity === pivot.capacity) mid.push(r);
    else right.push(r);
  }
  return [...quickSortClassrooms(left), ...mid, ...quickSortClassrooms(right)];
}

/**
 * Binary Search Best-Fit implementation.
 * Finds the smallest classroom capable of accommodating requiredCapacity.
 * Time Complexity: O(log n).
 * Minimizes unused seating capacity.
 */
function binarySearchBestFit(sortedRooms: Classroom[], requiredCapacity: number): Classroom | null {
  let low = 0;
  let high = sortedRooms.length - 1;
  let best: Classroom | null = null;
  while (low <= high) {
    const mid = Math.floor((low + high) / 2);
    if (sortedRooms[mid].capacity >= requiredCapacity) {
      best = sortedRooms[mid];
      high = mid - 1; // Look for a smaller fitting room to minimize waste
    } else {
      low = mid + 1; // Room too small, search larger rooms
    }
  }
  return best;
}

export interface FormValues {
  section: string; date: string; subjectId: string; teacherEmail: string; timeslot: string; classroomId: string;
}

interface Props {
  refs: AdminRefs;
  value: FormValues;
  onChange: (patch: Partial<FormValues>) => void;
  /** Set when editing: its own slot/room stay selectable. */
  entry?: ScheduleEntry;
  /** Bump to refetch availability after the parent changed the schedule. */
  version?: number;
  submitLabel: string;
  onSaved: (r: EntryResult, p: EntryPayload) => void;
  onCancel?: () => void;
  /** Left-aligned action next to Cancel / Save (e.g. Remove class in the editor). */
  leading?: React.ReactNode;
}

const same = (a: string, b: string) => a.toLowerCase() === b.toLowerCase();
const REQUIRED: [keyof FormValues, string, string][] = [
  ['section', 'ef-section', 'Choose a section.'],
  ['date', 'ef-date', 'Choose a date.'],
  ['subjectId', 'ef-subject', 'Choose a subject.'],
  ['teacherEmail', 'ef-teacher', 'Choose a teacher.'],
  ['timeslot', 'ef-timeslot', 'Choose a timeslot.'],
  ['classroomId', 'ef-room', 'Choose a classroom.'],
];

/** One form for "schedule a class" and "edit a class": fields, availability, validation, clash confirm. */
export function EntryForm({ refs, value: v, onChange, entry, version = 0, submitLabel, onSaved, onCancel, leading }: Props) {
  const toast = useToast();
  const confirm = useConfirm();
  const [errors, setErrors] = useState<Partial<Record<keyof FormValues, string>>>({});
  const [formError, setFormError] = useState('');
  const [busy, setBusy] = useState(false);
  const [avail, setAvail] = useState<{ key: string; data: Availability } | null>(null);

  const key = `${v.date}|${v.section}|${v.teacherEmail}|${version}`;
  useEffect(() => {
    if (!v.date || !v.section) return;
    let alive = true;
    api.availability({ date: v.date, section: v.section, teacher_email: v.teacherEmail || undefined })
      .then(data => alive && setAvail({ key, data }))
      .catch(e => alive && toast(e instanceof ApiError ? e.message : 'Could not check availability', 'error'));
    return () => { alive = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key, toast]);
  const slots = avail?.key === key ? avail.data.slots : null;

  const ownDay = !!entry && v.date === entry.date;
  const slotBusy = (ts: string) => {
    const s = slots?.[ts];
    if (!s) return false;
    const own = ownDay && v.section === entry!.section && ts === entry!.timeslot;
    return (s.section_busy && !own) || (s.teacher_busy && !(own && same(v.teacherEmail, entry!.teacher_email)));
  };
  const roomBusy = (id: number) =>
    !!slots?.[v.timeslot]?.busy_rooms.includes(id) && !(ownDay && v.timeslot === entry!.timeslot && id === entry!.classroom_id);

  // Never leave a disabled option selected.
  useEffect(() => {
    if (v.timeslot && slotBusy(v.timeslot)) onChange({ timeslot: '', classroomId: '' });
    else if (v.classroomId && roomBusy(Number(v.classroomId))) onChange({ classroomId: '' });
  });

  const setDate = (d: string) => {
    if (d && isWeekend(d)) {
      const mon = toWeekday(d);
      toast(`Classes run Monday to Friday. Date moved to ${formatDay(mon)}.`, 'info');
      d = mon;
    }
    onChange({ date: d });
  };
  const setSubject = (id: string) => {
    const s = refs.subjects.find(x => String(x.id) === id);
    const sug = refs.faculty.find(f => s?.faculty_email && same(f.email, s.faculty_email));
    onChange({ subjectId: id, ...(sug ? { teacherEmail: sug.email } : {}) });
  };

  const subject = refs.subjects.find(s => String(s.id) === v.subjectId);
  const suggested = !!subject?.faculty_email && !!v.teacherEmail && same(subject.faculty_email, v.teacherEmail);
  const teacherKnown = refs.faculty.some(f => same(f.email, v.teacherEmail));

  // Best-Fit Classroom Allocation via Quick Sort + Binary Search
  const strength = SECTION_STRENGTHS[v.section] ?? (v.section ? 40 : 0);
  const sortedClassrooms = useMemo(() => quickSortClassrooms(refs.classrooms), [refs.classrooms]);
  const availableRooms = useMemo(
    () => sortedClassrooms.filter(c => !roomBusy(c.id)),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [sortedClassrooms, slots, v.timeslot, v.date, entry]
  );
  const suggestedRoom = useMemo(() => {
    if (!v.section || !v.timeslot || availableRooms.length === 0) return null;
    return binarySearchBestFit(availableRooms, strength);
  }, [v.section, v.timeslot, availableRooms, strength]);

  // Auto-suggest best fit classroom when section + timeslot are chosen and no classroom is selected yet
  useEffect(() => {
    if (v.section && v.timeslot && !v.classroomId && suggestedRoom) {
      onChange({ classroomId: String(suggestedRoom.id) });
    }
  }, [v.section, v.timeslot, suggestedRoom, v.classroomId, onChange]);

  const a11y = (k: keyof FormValues, id: string) => ({
    id, 'aria-invalid': errors[k] ? true : undefined, 'aria-describedby': errors[k] ? `${id}-err` : undefined,
  });
  const err = (k: keyof FormValues, id: string) => errors[k] && <p id={`${id}-err`} className="field-error">{errors[k]}</p>;

  async function submit(e: FormEvent) {
    e.preventDefault();
    const next: typeof errors = {};
    let first = '';
    for (const [k, id, msg] of REQUIRED) if (!v[k]) { next[k] = msg; first ||= id; }
    setErrors(next);
    if (first) { document.getElementById(first)?.focus(); return; }

    const teacher = refs.faculty.find(f => same(f.email, v.teacherEmail));
    const payload: EntryPayload = {
      section: v.section, date: v.date, timeslot: v.timeslot,
      subject_id: Number(v.subjectId), classroom_id: Number(v.classroomId),
      teacher_name: teacher?.name ?? entry?.teacher_name ?? v.teacherEmail, teacher_email: v.teacherEmail,
    };
    const send = (p: EntryPayload) => (entry ? api.updateEntry(entry.id, p) : api.createEntry(p));
    setBusy(true);
    setFormError('');
    try {
      let r: EntryResult;
      try {
        r = await send(payload);
      } catch (ex) {
        if (!(ex instanceof ApiError && ex.needsConfirm)) throw ex;
        const ok = await confirm(ex.message, { title: 'Class clash', confirmText: 'Save with clash', danger: true });
        if (!ok) return;
        r = await send({ ...payload, allow_clash: true });
      }
      onSaved(r, payload);
    } catch (ex) {
      setFormError(ex instanceof ApiError ? ex.message : 'Could not save the class.');
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="adm-form" onSubmit={submit} noValidate>
      <div className="adm-grid">
        <div className="field">
          <label htmlFor="ef-section">Section</label>
          <select className="select" {...a11y('section', 'ef-section')} value={v.section} onChange={e => onChange({ section: e.target.value })}>
            <option value="">Select section</option>
            {refs.sections.map(s => {
              const cap = SECTION_STRENGTHS[s];
              return <option key={s} value={s}>{s}{cap ? ` (${cap} students)` : ''}</option>;
            })}
          </select>
          {err('section', 'ef-section')}
        </div>
        <div className="field">
          <label htmlFor="ef-date">Date</label>
          <input type="date" className="input" min={todayISO()} {...a11y('date', 'ef-date')} value={v.date} onChange={e => setDate(e.target.value)} />
          {err('date', 'ef-date')}
        </div>
        <div className="field adm-span">
          <label htmlFor="ef-subject">Subject</label>
          <select className="select" {...a11y('subjectId', 'ef-subject')} value={v.subjectId} onChange={e => setSubject(e.target.value)}>
            <option value="">Select subject</option>
            {refs.subjects.map(s => <option key={s.id} value={s.id}>{s.code} · {s.name}</option>)}
          </select>
          {err('subjectId', 'ef-subject')}
        </div>
        <div className="field adm-span">
          <label htmlFor="ef-teacher">Teacher {suggested && <span className="pill pill-ok">Suggested</span>}</label>
          <select className="select" {...a11y('teacherEmail', 'ef-teacher')} value={v.teacherEmail} onChange={e => onChange({ teacherEmail: e.target.value })}>
            <option value="">Select teacher</option>
            {!teacherKnown && v.teacherEmail && <option value={v.teacherEmail}>{entry?.teacher_name ?? v.teacherEmail}</option>}
            {refs.faculty.map(f => <option key={f.id} value={f.email}>{f.name}</option>)}
          </select>
          {err('teacherEmail', 'ef-teacher')}
        </div>
        <div className="field">
          <label htmlFor="ef-timeslot">Timeslot</label>
          <select className="select" {...a11y('timeslot', 'ef-timeslot')} value={v.timeslot} onChange={e => onChange({ timeslot: e.target.value })}>
            <option value="">Select timeslot</option>
            {refs.timeslots.map(ts => {
              const busyNow = slotBusy(ts);
              return <option key={ts} value={ts} disabled={busyNow}>{ts}{busyNow ? ' (busy)' : ''}</option>;
            })}
          </select>
          {err('timeslot', 'ef-timeslot')}
        </div>
        <div className="field">
          <label htmlFor="ef-room">Classroom</label>
          <select className="select" {...a11y('classroomId', 'ef-room')} value={v.classroomId} onChange={e => onChange({ classroomId: e.target.value })}>
            <option value="">Select classroom</option>
            {sortedClassrooms.map(c => {
              const booked = roomBusy(c.id);
              const isBest = suggestedRoom?.id === c.id;
              const unused = c.capacity - strength;
              let annot = '';
              if (booked) {
                annot = ' (booked)';
              } else if (v.section) {
                if (isBest) {
                  annot = ` — ★ Best Fit (${unused} unused seats)`;
                } else if (c.capacity < strength) {
                  annot = ` — ⚠️ Under-capacity (${c.capacity}/${strength})`;
                } else {
                  annot = ` — (${unused} unused seats)`;
                }
              }
              return (
                <option key={c.id} value={c.id} disabled={booked}>
                  {c.name} ({c.capacity} seats){annot}
                </option>
              );
            })}
          </select>
          {err('classroomId', 'ef-room')}
        </div>
      </div>

      {formError && <p className="alert alert-error" role="alert">{formError}</p>}
      <div className="dialog-actions form-actions">
        {leading}
        <div className="row">
          {onCancel && <button type="button" className="btn" onClick={onCancel}>Cancel</button>}
          <button type="submit" className="btn btn-primary" disabled={busy}>{busy ? 'Saving…' : submitLabel}</button>
        </div>
      </div>
    </form>
  );
}
