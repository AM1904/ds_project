import { useCallback, useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/Auth';
import { useBadges } from '../context/Badges';
import { useToast } from '../context/Toast';
import { useDocumentTitle } from '../hooks';
import { api, ApiError } from '../lib/api';
import { todayISO, toWeekday } from '../lib/dates';
import type { FacultyRequest, RequestType, ScheduleEntry } from '../lib/types';
import { ClassPicker } from '../components/faculty/ClassPicker';
import { RequestForm } from '../components/faculty/RequestForm';
import { RequestHistory } from '../components/faculty/RequestHistory';
import './faculty.css';

export default function FacultyRequests() {
  useDocumentTitle('Requests');
  const { user } = useAuth();
  const toast = useToast();
  const { refresh, markDecisionsSeen } = useBadges();
  const navigate = useNavigate();
  const loc = useLocation();
  const [params] = useSearchParams();
  const email = user?.email ?? '';
  const state = loc.state as { scheduleId?: number; fromGrid?: boolean } | null;

  const [type, setType] = useState<RequestType>(params.get('type') === 'extra' ? 'extra_hour' : 'change_request');
  const [canExtra, setCanExtra] = useState(true);
  const [date, setDate] = useState(() => toWeekday(todayISO()));
  const [selected, setSelected] = useState<ScheduleEntry | null>(null);
  const [history, setHistory] = useState<FacultyRequest[] | null>(null);
  const decisionsChecked = useRef(false);

  useEffect(() => {
    let alive = true;
    api.subjects()
      .then(s => {
        if (!alive) return;
        const ok = s.some(x => x.faculty_email?.toLowerCase() === email.toLowerCase());
        setCanExtra(ok);
        if (!ok) setType('change_request');
      })
      .catch(() => {});
    return () => { alive = false; };
  }, [email]);

  // Arrived from the timetable grid: load that class and show its day.
  useEffect(() => {
    const id = state?.scheduleId;
    if (!id) return;
    let alive = true;
    api.entry(id)
      .then(r => { if (alive) { setSelected(r.entry); setDate(r.entry.date); } })
      .catch(e => alive && toast(e instanceof ApiError ? e.message : 'Could not load that class', 'error'));
    return () => { alive = false; };
  }, [state?.scheduleId, toast]);

  const load = useCallback(() => {
    let alive = true;
    api.requests({ faculty_email: email })
      .then(r => {
        if (!alive) return;
        setHistory([...r].sort((a, b) => (b.created_at > a.created_at ? 1 : b.created_at < a.created_at ? -1 : b.id - a.id)));
        if (!decisionsChecked.current) {
          decisionsChecked.current = true;
          const seen = localStorage.getItem(`reqSeen:${email}`) ?? '';
          const n = r.filter(x => x.resolved_at && x.resolved_at > seen).length;
          markDecisionsSeen();
          if (n > 0) toast(`${n} of your requests were decided`, 'info');
        }
      })
      .catch(e => { if (alive) { setHistory([]); toast(e instanceof ApiError ? e.message : 'Could not load requests', 'error'); } });
    return () => { alive = false; };
  }, [email, markDecisionsSeen, toast]);

  useEffect(() => load(), [load]);

  const reload = () => { load(); refresh(); };

  return (
    <div className="page">
      <header className="page-head">
        <h1>Requests</h1>
        <p className="muted">Ask the admin to move a class, or add an extra hour.</p>
      </header>
      <div className={`fac-cols${type === 'extra_hour' ? ' fac-cols-single' : ''}`}>
        {type === 'change_request' && (
          <ClassPicker email={email} date={date} onDate={setDate} selected={selected} onSelect={c => { setSelected(c); setType('change_request'); }} />
        )}
        <RequestForm
          type={type} onType={setType} canExtra={canExtra} selected={selected}
          onSent={() => { setSelected(null); reload(); if (state?.fromGrid) navigate('/faculty'); }}
        />
      </div>
      <RequestHistory items={history} onChanged={reload} />
    </div>
  );
}
