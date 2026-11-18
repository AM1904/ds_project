import { useEffect, useState } from 'react';
import { MapPin, User } from 'lucide-react';
import { api, ApiError } from '../../lib/api';
import { formatLong } from '../../lib/dates';
import type { ScheduleEntry } from '../../lib/types';

interface Props { section: string; date: string; timeslots: string[]; version: number; onUse: (ts: string) => void }

/** Read-only view of one section's day, with a shortcut to fill the timeslot field. */
export function DayPreview({ section, date, timeslots, version, onUse }: Props) {
  const [rows, setRows] = useState<ScheduleEntry[] | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!section || !date) { setRows(null); return; }
    let alive = true;
    setError('');
    api.schedule({ section, date })
      .then(r => alive && setRows(r))
      .catch(e => alive && setError(e instanceof ApiError ? e.message : 'Could not load the day.'));
    return () => { alive = false; };
  }, [section, date, version]);

  return (
    <section className="card adm-preview" aria-labelledby="adm-prev-h">
      <h2 id="adm-prev-h">Day's timetable</h2>
      <p className="muted">{section && date ? `${section} · ${formatLong(date)}` : 'Choose a section and date.'}</p>
      {error && <p className="alert alert-error" role="alert">{error}</p>}
      {rows && (
        <ul className="adm-slots">
          {timeslots.map(ts => {
            const here = rows.filter(r => r.timeslot === ts);
            return (
              <li key={ts} className="adm-slot">
                <span className="adm-slot-time">{ts.replace(' - ', ' – ')}</span>
                {here.length === 0 ? (
                  <span className="adm-slot-free">
                    <span className="pill pill-ok">Free</span>
                    <button type="button" className="btn btn-sm" aria-label={`Use slot ${ts}`} onClick={() => onUse(ts)}>Use this slot</button>
                  </span>
                ) : (
                  <span className="adm-slot-body">
                    {here.map(c => (
                      <span key={c.id} className="adm-slot-class">
                        <strong>{c.subject_code} · {c.subject_name}</strong>
                        <span className="cc-meta"><User className="ico" aria-hidden="true" />{c.teacher_name}</span>
                        <span className="cc-meta"><MapPin className="ico" aria-hidden="true" />{c.room_name}</span>
                        {c.has_clash === 1 && <span className="pill pill-clash">Clash</span>}
                      </span>
                    ))}
                  </span>
                )}
              </li>
            );
          })}
        </ul>
      )}
      {!rows && !error && section && date && <p className="muted" aria-busy="true">Loading…</p>}
    </section>
  );
}
