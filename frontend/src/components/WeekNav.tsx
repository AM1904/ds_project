import { ChevronLeft, ChevronRight } from 'lucide-react';
import { addDays, todayISO } from '../lib/dates';
import type { WeekMeta } from '../lib/types';

interface Props {
  /** Currently selected date (any day inside the week). */
  date: string;
  meta?: WeekMeta;
  onChange: (date: string) => void;
}

export function WeekNav({ date, meta, onChange }: Props) {
  return (
    <div className="weeknav" role="group" aria-label="Choose week">
      <button type="button" className="btn btn-sm" onClick={() => onChange(addDays(date, -7))}>
        <ChevronLeft className="ico" aria-hidden="true" /> Prev
      </button>
      <span className="weeknav-label" aria-live="polite">{meta?.label ?? 'Loading week…'}</span>
      <button type="button" className="btn btn-sm" onClick={() => onChange(addDays(date, 7))}>
        Next <ChevronRight className="ico" aria-hidden="true" />
      </button>
      <button type="button" className="btn btn-sm" onClick={() => onChange(todayISO())}>This week</button>
      <label className="weeknav-jump">
        <span>Jump to</span>
        <input type="date" className="input" value={date} onChange={e => e.target.value && onChange(e.target.value)} />
      </label>
    </div>
  );
}
