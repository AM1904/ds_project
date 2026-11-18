import { useEffect, useState } from 'react';
import { useAuth } from '../context/Auth';
import { useToast } from '../context/Toast';
import { useDocumentTitle, useWeekParam } from '../hooks';
import { api, ApiError } from '../lib/api';
import type { WeekData } from '../lib/types';
import { WeekGrid } from '../components/WeekGrid';
import { WeekNav } from '../components/WeekNav';

export default function Student() {
  useDocumentTitle('My timetable');
  const { user } = useAuth();
  const toast = useToast();
  const [date, setDate] = useWeekParam();
  const [data, setData] = useState<WeekData | null>(null);
  const [loading, setLoading] = useState(true);
  const section = user?.section || 'MCA A';

  useEffect(() => {
    let live = true;
    setLoading(true);
    api.weekly({ date, section })
      .then(d => live && setData(d))
      .catch(e => live && toast(e instanceof ApiError ? e.message : 'Could not load timetable', 'error'))
      .finally(() => live && setLoading(false));
    return () => { live = false; };
  }, [date, section, toast]);

  return (
    <div className="page">
      <header className="page-head">
        <h1>My timetable</h1>
        <p className="muted">{section} · Your classes for the week. Moved classes carry an “Updated” tag.</p>
      </header>
      <WeekNav date={date} meta={data?.week_meta} onChange={setDate} />
      <WeekGrid data={data} loading={loading} />
    </div>
  );
}
