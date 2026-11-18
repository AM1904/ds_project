import { useCallback, useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useBadges } from '../context/Badges';
import { useConfirm } from '../context/Confirm';
import { useToast } from '../context/Toast';
import { useDocumentTitle } from '../hooks';
import { api, ApiError } from '../lib/api';
import type { FacultyRequest } from '../lib/types';
import { RequestCard } from '../components/requests/RequestCard';
import './adminrequests.css';

const STATUSES = ['pending', 'approved', 'rejected', 'cancelled', 'all'] as const;
const label = (s: string) => s[0].toUpperCase() + s.slice(1);
const msg = (e: unknown, fallback: string) => (e instanceof ApiError || e instanceof Error ? e.message : fallback);

export default function AdminRequests() {
  useDocumentTitle('Requests');
  const toast = useToast();
  const confirm = useConfirm();
  const badges = useBadges();
  const [params, setParams] = useSearchParams();
  const raw = params.get('status');
  const status = STATUSES.find(s => s === raw) ?? 'pending';
  const [items, setItems] = useState<FacultyRequest[] | null>(null);
  const [error, setError] = useState('');
  const [busyId, setBusyId] = useState<number | null>(null);
  const [tick, setTick] = useState(0);
  const reload = useCallback(() => setTick(t => t + 1), []);

  useEffect(() => {
    let alive = true;
    api.requests(status === 'all' ? {} : { status })
      .then(r => { if (alive) { setItems(r); setError(''); } })
      .catch(e => { if (alive) setError(msg(e, 'Could not load requests')); });
    return () => { alive = false; };
  }, [status, tick]);

  const choose = (s: string) => {
    setItems(null); setError('');
    setParams(prev => { const n = new URLSearchParams(prev); n.set('status', s); return n; }, { replace: true });
  };

  const run = async (id: number, op: () => Promise<{ message?: string }>, fallback: string) => {
    setBusyId(id);
    try {
      toast((await op()).message || fallback, 'success');
    } catch (e) {
      toast(msg(e, 'Request failed'), 'error');
    } finally {
      setBusyId(null);
      reload();
      badges.refresh();
    }
  };

  const resolve = (id: number, action: 'approve' | 'reject', note: string) =>
    run(id, () => api.resolveRequest(id, action, note), action === 'approve' ? 'Request approved' : 'Request rejected');

  const revert = async (id: number) => {
    const ok = await confirm('Revert this approval? The schedule goes back to how it was and the request returns to pending.',
      { title: 'Revert approval', confirmText: 'Revert' });
    if (ok) run(id, () => api.revertRequest(id), 'Approval reverted');
  };

  return (
    <div className="page">
      <header className="page-head">
        <h1>Faculty requests</h1>
        <p className="muted">Review schedule changes and extra hours teachers have asked for.</p>
      </header>

      <div className="segmented ar-filter" role="group" aria-label="Filter by status">
        {STATUSES.map(s => (
          <button key={s} type="button" aria-pressed={s === status} onClick={() => choose(s)}>{label(s)}</button>
        ))}
      </div>

      <section aria-label="Requests" aria-busy={!items && !error}>
        {error ? <p className="alert alert-error" role="alert">{error}</p>
          : !items ? <p className="muted" role="status">Loading requests…</p>
          : items.length === 0 ? <div className="empty"><strong>No {status === 'all' ? '' : status + ' '}requests</strong><span>New requests from teachers show up here.</span></div>
          : (
            <div className="ar-list">
              {items.map(r => (
                <RequestCard key={r.id} req={r} busy={busyId === r.id} onResolve={resolve} onRevert={revert} />
              ))}
            </div>
          )}
      </section>
    </div>
  );
}
