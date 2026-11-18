import { MapPin, User } from 'lucide-react';
import type { ScheduleEntry } from '../lib/types';

const WEEK_MS = 7 * 24 * 3600 * 1000;
export const isRecentlyChanged = (c: ScheduleEntry) =>
  !!c.changed_at && Date.now() - new Date(c.changed_at.replace(' ', 'T')).getTime() < WEEK_MS;

interface Props {
  entry: ScheduleEntry;
  showSection?: boolean;
  showTime?: boolean;
  /** Grid cell: name and one meta line, no subject code. */
  compact?: boolean;
  /** Teacher's own timetable: their name on every cell is noise. */
  hideTeacher?: boolean;
  /** Makes the card a button (teacher picks a class, admin opens the editor). */
  onSelect?: (c: ScheduleEntry) => void;
  selected?: boolean;
  selectLabel?: string;
}

export function ClassCard({ entry: c, showSection, showTime, compact, hideTeacher, onSelect, selected, selectLabel }: Props) {
  const flags = (c.has_clash === 1 || isRecentlyChanged(c)) && (
    <span className="cc-flags">
      {c.has_clash === 1 && <span className="pill pill-clash">Clash</span>}
      {isRecentlyChanged(c) && <span className="pill pill-updated" title={c.changed_note ?? 'Updated'}>Updated</span>}
    </span>
  );
  const body = compact ? (
    <>
      <span className="chip-top">
        <span className="chip-name">{c.subject_name}</span>
        {showSection && <span className="chip-sec">{c.section}</span>}
      </span>
      <span className="chip-meta">{hideTeacher ? c.room_name : `${c.room_name} · ${c.teacher_name}`}</span>
      {flags}
      {c.has_clash === 1 && c.clash_reason && <span className="cc-clash">{c.clash_reason}</span>}
    </>
  ) : (
    <>
      <span className="cc-top">
        <span className="cc-code">{c.subject_code}</span>
        {showSection && <span className="cc-sec">{c.section}</span>}
      </span>
      {showTime && <span className="cc-time">{c.timeslot}</span>}
      <span className="cc-name">{c.subject_name}</span>
      <span className="cc-meta"><User className="ico" aria-hidden="true" />{c.teacher_name}</span>
      <span className="cc-meta"><MapPin className="ico" aria-hidden="true" />{c.room_name}</span>
      {flags}
      {c.has_clash === 1 && c.clash_reason && <span className="cc-clash">{c.clash_reason}</span>}
    </>
  );
  return (
    <article className={`class-card theme-${c.subject_id % 6}${compact ? ' is-compact' : ''}${selected ? ' is-selected' : ''}${c.has_clash === 1 ? ' has-clash' : ''}`}>
      {onSelect ? (
        <button
          type="button" className="cc-main" aria-pressed={selected}
          aria-label={`${selectLabel ?? 'Select'}: ${c.subject_name}, ${c.section}, ${c.timeslot}`}
          title={`${c.subject_code} · ${c.subject_name}`}
          onClick={() => onSelect(c)}
        >{body}</button>
      ) : <div className="cc-main" title={`${c.subject_code} · ${c.subject_name}`}>{body}</div>}
    </article>
  );
}
