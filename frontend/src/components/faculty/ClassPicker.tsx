import { useEffect, useState } from 'react';
import { useToast } from '../../context/Toast';
import { api, ApiError } from '../../lib/api';
import { isWeekend, toWeekday } from '../../lib/dates';
import type { ScheduleEntry } from '../../lib/types';
import { ClassCard } from '../ClassCard';

interface Props {
  email: string;
  date: string;
  onDate: (d: string) => void;
  selected: ScheduleEntry | null;
  onSelect: (c: ScheduleEntry) => void;
}

export function ClassPicker({ email, date, onDate, selected, onSelect }: Props) {
  const toast = useToast();
  const [classes, setClasses] = useState<ScheduleEntry[] | null>(null);

  useEffect(() => {
    let alive = true;
    setClasses(null);
    api.facultyDay(email, date)
      .then(c => alive && setClasses(c))
      .catch(e => { if (alive) { setClasses([]); toast(e instanceof ApiError ? e.message : 'Could not load classes', 'error'); } });
    return () => { alive = false; };
  }, [email, date, toast]);

  const change = (v: string) => {
    if (!v) return;
    if (isWeekend(v)) { toast('Classes run Monday to Friday. Moved to Monday.', 'info'); v = toWeekday(v); }
    onDate(v);
  };

  return (
    <section className="card stack" aria-labelledby="fac-pick">
      <h2 id="fac-pick">Pick a class</h2>
      <div className="field">
        <label htmlFor="fac-view-date">Viewing date</label>
        <input id="fac-view-date" type="date" className="input" value={date} onChange={e => change(e.target.value)} />
      </div>
      {classes === null ? <p className="muted" aria-busy="true">Loading classes…</p>
        : classes.length === 0 ? <p className="empty">No classes on this day.</p>
        : (
          <ul className="fac-list">
            {classes.map(c => (
              <li key={c.id}>
                <ClassCard entry={c} showSection showTime onSelect={onSelect} selected={selected?.id === c.id} selectLabel="Request a change for" />
              </li>
            ))}
          </ul>
        )}
    </section>
  );
}
