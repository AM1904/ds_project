import { Plus, UtensilsCrossed } from 'lucide-react';
import { useMediaQuery } from '../hooks';
import type { ScheduleEntry, WeekData } from '../lib/types';
import { formatDay, formatSlot, isPastDay, isSlotNow } from '../lib/dates';
import { ClassCard } from './ClassCard';

interface Props {
  data: WeekData | null;
  loading?: boolean;
  showSection?: boolean;
  hideTeacher?: boolean;
  /** Click a class (teacher: request a change, admin: edit). */
  onSelect?: (c: ScheduleEntry) => void;
  selectedId?: number | null;
  selectLabel?: string;
  /** Admin: click an empty slot to add a class there. */
  onEmpty?: (date: string, timeslot: string) => void;
}

/** Weekly timetable. Wide screens: time x day table. Narrow screens: one card per day (agenda). */
export function WeekGrid({ data, loading, showSection, hideTeacher, onSelect, selectedId, selectLabel, onEmpty }: Props) {
  const narrow = useMediaQuery('(max-width: 820px)');
  if (!data) return <div className="card card-flat empty" aria-busy={loading}>{loading ? 'Loading timetable…' : 'No data.'}</div>;

  const total = data.days.reduce((n, d) => n + d.classes.length, 0);
  const card = (c: ScheduleEntry, compact: boolean) => (
    <ClassCard
      key={c.id} entry={c} showSection={showSection} hideTeacher={hideTeacher} showTime={!compact} compact={compact}
      onSelect={isPastDay(c.date) ? undefined : onSelect} selected={selectedId === c.id} selectLabel={selectLabel}
    />
  );

  return (
    <div className="weekgrid-wrap" aria-busy={loading}>
      {total === 0 && (
        <div className="empty card card-flat">
          <strong>No classes this week</strong>
          <span>Try another week or change the filters.</span>
        </div>
      )}
      {narrow ? (
        <div className="agenda">
          {data.days.map(d => (
            <section key={d.date} className={`agenda-day${d.is_today ? ' is-today' : ''}${isPastDay(d.date) ? ' is-past' : ''}`} aria-label={d.full_formatted}>
              <h3>{formatDay(d.date, { weekday: 'long', day: 'numeric', month: 'short' })}{d.is_today && <span className="pill pill-updated">Today</span>}</h3>
              {d.classes.length === 0 ? <p className="muted">No classes.</p> : <div className="agenda-list">{d.classes.map(c => card(c, false))}</div>}
            </section>
          ))}
        </div>
      ) : (
        <div className="weekgrid-scroll">
          <table className="weekgrid">
            <thead>
              <tr>
                <th scope="col" className="wg-time"><span className="sr-only">Time</span></th>
                {data.days.map(d => (
                  <th key={d.date} scope="col" className={`${d.is_today ? 'is-today' : ''}${isPastDay(d.date) ? ' is-past' : ''}`.trim() || undefined} title={isPastDay(d.date) ? 'Past day, read-only' : undefined}>
                    <span className="wg-day">{d.short_day}</span>
                    <span className="wg-date">{d.formatted}</span>
                    {d.is_today && <span className="wg-today">Today</span>}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.timeslots.flatMap(ts => {
                const row = (
                  <tr key={ts}>
                    <th scope="row" className="wg-time">{formatSlot(ts)}</th>
                    {data.days.map(d => {
                      const here = d.classes.filter(c => c.timeslot === ts);
                      const now = isSlotNow(d.date, ts);
                      return (
                        <td key={d.date} className={`${d.is_today ? 'is-today' : ''}${now ? ' is-now' : ''}${isPastDay(d.date) ? ' is-past' : ''}`.trim() || undefined}>
                          {here.length > 0 && <div className="wg-stack">{here.map(c => card(c, true))}</div>}
                          {onEmpty && !isPastDay(d.date) && (
                            <button type="button" className={`wg-add${here.length ? ' is-below' : ''}`}
                              aria-label={`Add a class on ${formatDay(d.date)}, ${ts}`} onClick={() => onEmpty(d.date, ts)}>
                              <Plus className="ico" aria-hidden="true" />
                            </button>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                );
                // Lunch break sits after the 11:15 slot
                return ts.startsWith('11:15')
                  ? [row, (
                    <tr key="lunch" className="wg-lunch">
                      <th scope="row" className="wg-time">12:15–1:00 PM</th>
                      <td colSpan={data.days.length}><UtensilsCrossed className="ico" aria-hidden="true" /> Lunch</td>
                    </tr>)]
                  : [row];
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
