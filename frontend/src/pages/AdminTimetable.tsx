import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { LayoutGrid, List } from 'lucide-react';
import { useConfirm } from '../context/Confirm';
import { useToast } from '../context/Toast';
import { useDocumentTitle, useWeekParam } from '../hooks';
import { api, ApiError } from '../lib/api';
import { formatDay, formatSlot, isPastDay } from '../lib/dates';
import type { ScheduleEntry, WeekData } from '../lib/types';
import { WeekGrid } from '../components/WeekGrid';
import { WeekNav } from '../components/WeekNav';
import { EntryDialog } from '../components/admin/EntryDialog';
import { useAdminRefs } from '../components/admin/useAdminRefs';
import './admin.css';

export default function AdminTimetable() {
  useDocumentTitle('Academic timetable');
  const toast = useToast();
  const confirm = useConfirm();
  const navigate = useNavigate();
  const [params, setParams] = useSearchParams();
  const [date, setDate] = useWeekParam();
  const section = params.get('section') ?? '';
  const faculty = params.get('faculty') ?? '';
  const view = params.get('view') === 'list' ? 'list' : 'grid';
  const setParam = (k: string, v: string) =>
    setParams(prev => { const n = new URLSearchParams(prev); if (v) n.set(k, v); else n.delete(k); return n; }, { replace: true });

  const { refs, error: refsError, retry } = useAdminRefs();
  const [data, setData] = useState<WeekData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [version, setVersion] = useState(0);
  const [editing, setEditing] = useState<ScheduleEntry | null>(null);
  const reload = () => setVersion(n => n + 1);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    setError('');
    api.weekly({ date, section, teacher_email: faculty })
      .then(d => alive && setData(d))
      .catch(e => alive && setError(e instanceof ApiError ? e.message : 'Could not load the timetable.'))
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, [date, section, faculty, version]);

  async function remove(c: ScheduleEntry) {
    const ok = await confirm('Remove this class from the schedule?', { title: 'Remove class', confirmText: 'Remove', danger: true });
    if (!ok) return;
    try {
      const { entry } = await api.entry(c.id);
      await api.deleteEntry(c.id);
      toast(`Removed ${entry.subject_name}.`, 'success', {
        label: 'Undo',
        onClick: () => {
          api.createEntry({
            section: entry.section, date: entry.date, timeslot: entry.timeslot, subject_id: entry.subject_id,
            classroom_id: entry.classroom_id, teacher_name: entry.teacher_name, teacher_email: entry.teacher_email, allow_clash: true,
          })
            .then(() => toast('Class restored.', 'success'))
            .catch(e => toast(e instanceof ApiError ? e.message : 'Could not restore the class.', 'error'))
            .finally(reload);
        },
      });
    } catch (e) {
      toast(e instanceof ApiError ? e.message : 'Could not remove the class.', 'error');
    }
    reload();
  }

  return (
    <div className="page">
      <header className="page-head">
        <h1>Academic timetable</h1>
        <p className="muted">Every section's week. Click a class to edit, or an empty slot to add. Past days are read-only.</p>
      </header>

      {refsError && <p className="alert alert-error" role="alert">{refsError} <button type="button" className="btn btn-sm" onClick={retry}>Retry</button></p>}

      <div className="adm-toolbar">
        <WeekNav date={date} meta={data?.week_meta} onChange={setDate} />
        <div className="adm-controls">
          <select aria-label="Section" className="select" value={section} onChange={e => setParam('section', e.target.value)}>
            <option value="">All sections</option>
            {refs?.sections.map(s => <option key={s}>{s}</option>)}
          </select>
          <select aria-label="Faculty" className="select" value={faculty} onChange={e => setParam('faculty', e.target.value)}>
            <option value="">All faculty</option>
            {refs?.faculty.map(f => <option key={f.id} value={f.email}>{f.name}</option>)}
          </select>
          <div className="segmented" role="group" aria-label="View">
            <button type="button" aria-pressed={view === 'grid'} onClick={() => setParam('view', '')}>
              <LayoutGrid className="ico" aria-hidden="true" /> Grid
            </button>
            <button type="button" aria-pressed={view === 'list'} onClick={() => setParam('view', 'list')}>
              <List className="ico" aria-hidden="true" /> List
            </button>
          </div>
        </div>
      </div>

      {error && <p className="alert alert-error" role="alert">{error}</p>}

      {view === 'grid' ? (
        <WeekGrid
          data={data} loading={loading} showSection
          onSelect={c => refs && setEditing(c)} selectLabel="Edit"
          onEmpty={(d, ts) => navigate(`/admin/new?date=${d}&timeslot=${encodeURIComponent(ts)}${section ? `&section=${encodeURIComponent(section)}` : ''}`)}
        />
      ) : !data ? (
        <div className="card card-flat empty" aria-busy={loading}>{loading ? 'Loading timetable…' : 'No data.'}</div>
      ) : data.classes.length === 0 ? (
        <div className="empty card card-flat"><strong>No classes this week</strong><span>Try another week or change the filters.</span></div>
      ) : (
        <div className="table-wrap" aria-busy={loading}>
          <table className="table adm-list">
            <caption className="sr-only">Classes this week, grouped by day</caption>
            <thead>
              <tr><th scope="col">Time</th><th scope="col">Section</th><th scope="col">Subject</th><th scope="col">Teacher</th><th scope="col">Room</th></tr>
            </thead>
            {data.days.filter(d => d.classes.length > 0).map(d => (
              <tbody key={d.date}>
                <tr className="day-row">
                  <th scope="colgroup" colSpan={5}>
                    {formatDay(d.date, { weekday: 'long', day: 'numeric', month: 'long' })}
                    <span>{d.classes.length} {d.classes.length === 1 ? 'class' : 'classes'}</span>
                  </th>
                </tr>
                {d.classes.map(c => (
                  <tr key={c.id} className={`${isPastDay(d.date) ? 'is-past' : 'is-click'}${c.has_clash ? ' row-clash' : ''}`} onClick={isPastDay(d.date) ? undefined : () => refs && setEditing(c)}>
                    <td className="nowrap">{formatSlot(c.timeslot)}</td>
                    <td className="nowrap">{c.section}</td>
                    <td>
                      {isPastDay(d.date) ? <span>{c.subject_name}</span> : (
                        <button type="button" className="row-link" disabled={!refs}
                          aria-label={`Edit ${c.subject_name}, ${c.section}, ${c.timeslot}`}
                          onClick={e => { e.stopPropagation(); setEditing(c); }}>{c.subject_name}</button>
                      )}
                      <span className="muted"> {c.subject_code}</span>
                      {c.has_clash === 1 && <span className="pill pill-clash adm-clash-pill">Clash</span>}
                      {c.has_clash === 1 && c.clash_reason && <span className="adm-clash">{c.clash_reason}</span>}
                    </td>
                    <td className="nowrap">{c.teacher_name}</td>
                    <td className="nowrap">{c.room_name}</td>
                  </tr>
                ))}
              </tbody>
            ))}
          </table>
        </div>
      )}

      {refs && <EntryDialog entry={editing} refs={refs} onClose={() => setEditing(null)} onSaved={reload} onRemove={c => { setEditing(null); remove(c); }} />}
    </div>
  );
}
