import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { isValidISO, todayISO } from './lib/dates';

export function useMediaQuery(query: string) {
  const [match, setMatch] = useState(() => window.matchMedia(query).matches);
  useEffect(() => {
    const m = window.matchMedia(query);
    const on = () => setMatch(m.matches);
    on();
    m.addEventListener('change', on);
    return () => m.removeEventListener('change', on);
  }, [query]);
  return match;
}

/** The selected date lives in the URL (?week=YYYY-MM-DD) so refresh and links keep your place. */
export function useWeekParam(): [string, (d: string) => void] {
  const [params, setParams] = useSearchParams();
  const raw = params.get('week');
  const date = isValidISO(raw) ? raw : todayISO();
  const set = (d: string) => setParams(prev => { const n = new URLSearchParams(prev); n.set('week', d); return n; }, { replace: true });
  return [date, set];
}

export function useDocumentTitle(title: string) {
  useEffect(() => { document.title = `${title} · Campus Timetable`; }, [title]);
}
