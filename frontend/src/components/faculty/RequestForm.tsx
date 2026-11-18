import { useEffect, useMemo, useState, type FormEvent } from 'react';
import { useAuth } from '../../context/Auth';
import { useBadges } from '../../context/Badges';
import { useToast } from '../../context/Toast';
import { api, ApiError } from '../../lib/api';
import { formatDay, isWeekend, todayISO, toWeekday } from '../../lib/dates';
import type { Availability, Classroom, RequestType, ScheduleEntry } from '../../lib/types';

interface Props {
  type: RequestType;
  onType: (t: RequestType) => void;
  canExtra: boolean;
  selected: ScheduleEntry | null;
  onSent: () => void;
}

type Errors = Partial<Record<'date' | 'slot' | 'reason', string>>;
const ORDER = ['date', 'slot', 'reason'] as const;
const IDS = { date: 'fac-date', slot: 'fac-slot', reason: 'fac-reason' };

export function RequestForm({ type, onType, canExtra, selected, onSent }: Props) {
  const { user } = useAuth();
  const toast = useToast();
  const { refresh } = useBadges();
  const email = user?.email ?? '';
  const extra = type === 'extra_hour';

  const [slots, setSlots] = useState<string[]>([]);
  const [rooms, setRooms] = useState<Classroom[]>([]);
  const [sections, setSections] = useState<string[]>([]);
  const [date, setDate] = useState('');
  const [slot, setSlot] = useState('');
  const [room, setRoom] = useState('');
  const [section, setSection] = useState('');
  const [reason, setReason] = useState('');
  const [avail, setAvail] = useState<Availability | null>(null);
  const [errors, setErrors] = useState<Errors>({});
  const [serverError, setServerError] = useState('');
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let alive = true;
    Promise.all([api.timeslots(), api.classrooms(), api.sections()])
      .then(([t, c, s]) => { if (alive) { setSlots(t); setRooms(c); setSections(s); setSection(p => p || user?.section || s[0] || ''); } })
      .catch(e => alive && toast(e instanceof ApiError ? e.message : 'Could not load form options', 'error'));
    return () => { alive = false; };
  }, [toast, user?.section]);

  // Availability only matters for the extra hour form.
  useEffect(() => {
    if (!extra || !date || !section) { setAvail(null); return; }
    let alive = true;
    api.availability({ date, section, teacher_email: email })
      .then(a => {
        if (!alive) return;
        setAvail(a);
        setSlot(s => (s && isBusy(a, s, rooms) ? '' : s));
      })
      .catch(() => alive && setAvail(null));
    return () => { alive = false; };
  }, [extra, date, section, email, rooms]);

  const busySlot = useMemo(() => (s: string) => !!avail && isBusy(avail, s, rooms), [avail, rooms]);

  const pickDate = (v: string) => {
    if (v && isWeekend(v)) { toast('Classes run Monday to Friday. Moved to Monday.', 'info'); v = toWeekday(v); }
    setDate(v);
  };

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    const err: Errors = {};
    if (extra) {
      if (!date) err.date = 'Choose a date.';
      if (!slot) err.slot = 'Choose a timeslot.';
    } else if (!date && !slot && !room) err.date = 'Choose a new date, timeslot or classroom.';
    if (!reason.trim()) err.reason = 'Give a reason.';
    setErrors(err);
    setServerError('');
    const first = ORDER.find(k => err[k]);
    if (first) { document.getElementById(IDS[first])?.focus(); return; }
    setBusy(true);
    try {
      await api.submitRequest(extra
        ? { request_type: 'extra_hour', reason: reason.trim(), requested_date: date, requested_timeslot: slot, preferred_section: section }
        : {
          request_type: 'change_request', reason: reason.trim(), schedule_id: selected?.id ?? null,
          requested_date: date, requested_timeslot: slot, requested_classroom: room,
        });
      toast('Request sent to the admin', 'success');
      setDate(''); setSlot(''); setRoom(''); setReason('');
      refresh();
      onSent();
    } catch (x) {
      setServerError(x instanceof ApiError ? x.message : 'Could not send the request.');
    } finally { setBusy(false); }
  };

  const fe = (k: keyof Errors) => ({
    'aria-invalid': errors[k] ? true : undefined,
    'aria-describedby': errors[k] ? `${IDS[k]}-err` : undefined,
  });
  const Err = ({ k }: { k: keyof Errors }) => errors[k] ? <p className="field-error" id={`${IDS[k]}-err`}>{errors[k]}</p> : null;

  return (
    <form className="card stack" onSubmit={submit} noValidate aria-labelledby="fac-form-h">
      <h2 id="fac-form-h">Send a request</h2>
      <div className="segmented" role="group" aria-label="Request type">
        <button type="button" aria-pressed={!extra} onClick={() => onType('change_request')}>Change a class</button>
        <button type="button" aria-pressed={extra} disabled={!canExtra} onClick={() => onType('extra_hour')}>Extra hour</button>
      </div>
      {!canExtra && <p className="alert alert-info">No subject is assigned to you yet. Ask the admin to assign one.</p>}

      {!extra && (selected ? (
        <div className="fac-summary">
          <strong>{selected.subject_name} ({selected.section})</strong>
          <span>{formatDay(selected.date)}, {selected.timeslot}, {selected.room_name}</span>
        </div>
      ) : <p className="help muted">Choose a class on the left.</p>)}

      <div className="fac-two">
        <div className="field">
          <label htmlFor={IDS.date}>{extra ? 'Date' : 'New date (optional)'}</label>
          <input id={IDS.date} type="date" className="input" min={todayISO()} value={date} onChange={e => pickDate(e.target.value)} {...fe('date')} />
          <Err k="date" />
        </div>
        <div className="field">
          <label htmlFor={IDS.slot}>{extra ? 'Timeslot' : 'New timeslot (optional)'}</label>
          <select id={IDS.slot} className="select" value={slot} onChange={e => setSlot(e.target.value)} {...fe('slot')}>
            <option value="">{extra ? 'Select a timeslot' : 'Keep current'}</option>
            {slots.map(s => <option key={s} value={s} disabled={busySlot(s)}>{s}{busySlot(s) ? ' (busy)' : ''}</option>)}
          </select>
          <Err k="slot" />
        </div>
      </div>

      {extra ? (
        <div className="field">
          <label htmlFor="fac-section">Section</label>
          <select id="fac-section" className="select" value={section} onChange={e => setSection(e.target.value)}>
            {sections.map(s => <option key={s} value={s}>{s}</option>)}
          </select>
        </div>
      ) : (
        <div className="field">
          <label htmlFor="fac-room">New classroom (optional)</label>
          <select id="fac-room" className="select" value={room} onChange={e => setRoom(e.target.value)}>
            <option value="">Keep current</option>
            {rooms.map(r => <option key={r.id} value={r.name}>{r.name}</option>)}
          </select>
        </div>
      )}

      <div className="field">
        <label htmlFor={IDS.reason}>Reason</label>
        <textarea id={IDS.reason} className="textarea" rows={3} value={reason} onChange={e => setReason(e.target.value)} {...fe('reason')} />
        <Err k="reason" />
      </div>

      {serverError && <p className="alert alert-error" role="alert">{serverError}</p>}
      <button type="submit" className="btn btn-primary" disabled={busy}>{busy ? 'Sending…' : 'Send request'}</button>
    </form>
  );
}

function isBusy(a: Availability, slot: string, rooms: Classroom[]) {
  const s = a.slots[slot];
  if (!s) return false;
  return s.section_busy || s.teacher_busy || (rooms.length > 0 && rooms.every(r => s.busy_rooms.includes(r.id)));
}
