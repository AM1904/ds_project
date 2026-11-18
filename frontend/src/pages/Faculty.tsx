import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { PlusCircle } from 'lucide-react';
import { useAuth } from '../context/Auth';
import { useToast } from '../context/Toast';
import { useDocumentTitle, useWeekParam } from '../hooks';
import { api, ApiError } from '../lib/api';
import type { ScheduleEntry, WeekData } from '../lib/types';
import { WeekGrid } from '../components/WeekGrid';
import { WeekNav } from '../components/WeekNav';
import './faculty.css';

export default function Faculty() {
  useDocumentTitle('My timetable');
  const { user } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();
  const [date, setDate] = useWeekParam();
  const [data, setData] = useState<WeekData | null>(null);
  const [loading, setLoading] = useState(true);
  const email = user?.email ?? '';

  useEffect(() => {
    let alive = true;
    setLoading(true);
    api.weekly({ date, teacher_email: email })
      .then(d => alive && setData(d))
      .catch(e => alive && toast(e instanceof ApiError ? e.message : 'Could not load timetable', 'error'))
      .finally(() => alive && setLoading(false));
    return () => { alive = false; };
  }, [date, email, toast]);

  const select = (c: ScheduleEntry) => navigate('/faculty/requests', { state: { scheduleId: c.id, fromGrid: true } });

  return (
    <div className="page">
      <header className="page-head">
        <h1>My timetable</h1>
        <div className="row spread">
          <p className="muted" id="fac-hint">Select a class to request a change</p>
          <Link to="/faculty/requests?type=extra" className="btn">
            <PlusCircle className="ico" aria-hidden="true" /> Request an extra hour
          </Link>
        </div>
      </header>
      <WeekNav date={date} meta={data?.week_meta} onChange={setDate} />
      <WeekGrid data={data} loading={loading} showSection hideTeacher onSelect={select} selectLabel="Request a change for" />
    </div>
  );
}
