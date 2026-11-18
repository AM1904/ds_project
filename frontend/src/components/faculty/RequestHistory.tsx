import { useConfirm } from '../../context/Confirm';
import { useToast } from '../../context/Toast';
import { api, ApiError } from '../../lib/api';
import { formatDay, formatStamp } from '../../lib/dates';
import type { FacultyRequest } from '../../lib/types';

interface Props { items: FacultyRequest[] | null; onChanged: () => void }

const day = (s: string) => (/^\d{4}-\d{2}-\d{2}$/.test(s) ? formatDay(s) : s);

/** One line that says what was asked, e.g. "Data Structures (MCA B), Wed 18 Nov, 9:00 AM -> Tue 24 Nov, Systems Lab-1". */
function summary(r: FacultyRequest) {
  if (r.request_type === 'extra_hour') {
    return [r.preferred_section || 'Any section', day(r.requested_date), r.requested_timeslot].filter(Boolean).join(' · ');
  }
  const from = [`${r.class_subject ?? 'Removed class'}${r.class_section ? ` (${r.class_section})` : ''}`, r.class_date && day(r.class_date), r.class_timeslot].filter(Boolean).join(' · ');
  const to = [r.requested_date && day(r.requested_date), r.requested_timeslot, r.requested_classroom].filter(Boolean).join(' · ');
  return `${from} → ${to || 'no change given'}`;
}

export function RequestHistory({ items, onChanged }: Props) {
  const confirm = useConfirm();
  const toast = useToast();

  const cancel = async (r: FacultyRequest) => {
    if (!await confirm('Cancel this request?', { title: 'Cancel request', confirmText: 'Cancel request', cancelText: 'Keep it', danger: true })) return;
    try {
      await api.cancelRequest(r.id);
      toast('Request cancelled', 'success');
    } catch (e) {
      toast(e instanceof ApiError ? e.message : 'Could not cancel', 'error');
    }
    onChanged();
  };

  return (
    <section className="stack" aria-labelledby="fac-hist">
      <h2 id="fac-hist">Sent requests</h2>
      {items === null ? <p className="muted" aria-busy="true">Loading requests…</p>
        : items.length === 0 ? <div className="card card-flat empty"><strong>No requests yet</strong><span>Pick a class and send your first one.</span></div>
        : (
          <div className="table-wrap">
            <table className="table fac-table">
              <caption className="sr-only">Requests you have sent</caption>
              <thead>
                <tr><th scope="col">Request</th><th scope="col">Status</th><th scope="col">Sent</th><th scope="col"><span className="sr-only">Actions</span></th></tr>
              </thead>
              <tbody>
                {items.map(r => (
                  <tr key={r.id}>
                    <td className="fac-main">
                      <strong>{r.request_type === 'extra_hour' ? 'Extra hour' : 'Change a class'}</strong>
                      <span>{summary(r)}</span>
                      <span className="muted">“{r.reason}”</span>
                      {r.admin_note && <span className="fac-note"><strong>Admin:</strong> {r.admin_note}</span>}
                    </td>
                    <td><span className={`pill pill-${r.status}`}>{r.status}</span></td>
                    <td className="nowrap muted">{formatStamp(r.created_at)}</td>
                    <td className="nowrap">
                      {r.status === 'pending' && <button type="button" className="btn btn-sm btn-danger" onClick={() => cancel(r)}>Cancel</button>}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
    </section>
  );
}
