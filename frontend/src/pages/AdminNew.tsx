import { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useToast } from '../context/Toast';
import { useDocumentTitle } from '../hooks';
import { formatDay, isPastDay, isValidISO, isWeekend, toWeekday, todayISO } from '../lib/dates';
import { DayPreview } from '../components/admin/DayPreview';
import { EntryForm, type FormValues } from '../components/admin/EntryForm';
import { useAdminRefs, type AdminRefs } from '../components/admin/useAdminRefs';
import './admin.css';

export default function AdminNew() {
  useDocumentTitle('Schedule a class');
  const { refs, error, retry } = useAdminRefs();
  return (
    <div className="page">
      <header className="page-head">
        <h1>Schedule a class</h1>
        <p className="muted">Fill in the class below. The day's timetable on the right shows what is free.</p>
      </header>
      {error && <p className="alert alert-error" role="alert">{error} <button type="button" className="btn btn-sm" onClick={retry}>Retry</button></p>}
      {!refs && !error && <p className="muted" aria-busy="true">Loading…</p>}
      {refs && <Body refs={refs} />}
    </div>
  );
}

function Body({ refs }: { refs: AdminRefs }) {
  const toast = useToast();
  const navigate = useNavigate();
  // Opened from an empty slot in the timetable: ?date=&timeslot=&section= prefill the form.
  const [params] = useSearchParams();
  const qDate = params.get('date'), qSlot = params.get('timeslot'), qSection = params.get('section');
  const [v, setV] = useState<FormValues>({
    section: qSection && refs.sections.includes(qSection) ? qSection : refs.sections[0] ?? '',
    date: isValidISO(qDate) && !isWeekend(qDate) && !isPastDay(qDate) ? qDate : toWeekday(todayISO()),
    subjectId: '', teacherEmail: '',
    timeslot: qSlot && refs.timeslots.includes(qSlot) ? qSlot : '',
    classroomId: '',
  });
  const [version, setVersion] = useState(0);

  return (
    <div className="adm-new">
      <div className="card">
      <EntryForm
        refs={refs} value={v} version={version} onChange={p => setV(s => ({ ...s, ...p }))}
        submitLabel="Add to timetable"
        onSaved={(r, p) => {
          toast(`Added for ${formatDay(p.date)}. Open the timetable to see it.`, 'success', {
            label: 'View week', onClick: () => navigate(`/admin?week=${p.date}`),
          });
          if (r.has_clash) toast(r.message, 'error');
          setV(s => ({ ...s, timeslot: '', classroomId: '' }));
          setVersion(n => n + 1);
        }}
      />
      </div>
      <DayPreview
        section={v.section} date={v.date} timeslots={refs.timeslots} version={version}
        onUse={ts => setV(s => ({ ...s, timeslot: ts }))}
      />
    </div>
  );
}
