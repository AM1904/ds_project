import { useRef, useState } from 'react';
import { Check, Undo2, X } from 'lucide-react';
import type { FacultyRequest } from '../../lib/types';
import { formatDay, formatStamp } from '../../lib/dates';

interface Props {
  req: FacultyRequest;
  busy: boolean;
  onResolve: (id: number, action: 'approve' | 'reject', note: string) => void;
  onRevert: (id: number) => void;
}

function Block({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="ar-block">
      <p className="ar-label">{label}</p>
      {children}
    </div>
  );
}

export function RequestCard({ req, busy, onResolve, onRevert }: Props) {
  const [note, setNote] = useState('');
  const [error, setError] = useState('');
  const ref = useRef<HTMLInputElement>(null);
  const pending = req.status === 'pending';
  const extra = req.request_type === 'extra_hour';
  const requested = [req.requested_date && formatDay(req.requested_date), req.requested_timeslot, req.requested_classroom].filter(Boolean);
  const titleId = `ar-title-${req.id}`;
  const noteId = `ar-note-${req.id}`;

  const reject = () => {
    if (!note.trim()) {
      setError('Add a note explaining the rejection.');
      ref.current?.focus();
      return;
    }
    onResolve(req.id, 'reject', note.trim());
  };

  return (
    <article className={`card ar-card`} aria-labelledby={titleId}>
      <header className="ar-head">
        <div>
          <h2 id={titleId} className="ar-name">{req.faculty_name}</h2>
          <p className="muted">{extra ? 'Extra hour' : 'Schedule change'} · Sent {formatStamp(req.created_at)}</p>
        </div>
        <span className={`pill pill-${req.status}`}>{req.status}</span>
      </header>

      <div className="ar-blocks">
        {extra ? (
          <Block label="Extra hour for"><p>Section {req.preferred_section}</p></Block>
        ) : (
          <Block label="Current class">
            {req.class_subject ? (
              <>
                <p><strong>{req.class_subject}</strong> · {req.class_section}</p>
                <p className="muted">{[req.class_date && formatDay(req.class_date), req.class_timeslot, req.class_room].filter(Boolean).join(' · ')}</p>
              </>
            ) : <p className="muted">This class no longer exists</p>}
          </Block>
        )}
        <Block label="Requested">
          {requested.length ? <p>{requested.join(' · ')}</p> : <p className="muted">No change specified</p>}
        </Block>
      </div>

      <blockquote className="ar-reason">{req.reason}</blockquote>

      {req.admin_note && (
        <p className="ar-admin">
          <strong>{pending ? 'Last attempt:' : 'Admin note'}</strong> {req.admin_note}
          {!pending && req.resolved_at && <span className="muted"> · {formatStamp(req.resolved_at)}</span>}
        </p>
      )}

      {pending && (
        <div className="ar-actions">
          <div className="field">
            <label htmlFor={noteId}>Note to teacher <span className="muted">(required to reject)</span></label>
            <input
              id={noteId} ref={ref} className="input" value={note} disabled={busy}
              aria-invalid={!!error} aria-describedby={error ? `${noteId}-err` : undefined}
              onChange={e => { setNote(e.target.value); setError(''); }}
            />
            {error && <p id={`${noteId}-err`} className="field-error">{error}</p>}
          </div>
          <div className="row">
            <button type="button" className="btn btn-primary" disabled={busy} onClick={() => onResolve(req.id, 'approve', note.trim())}>
              <Check className="ico" aria-hidden="true" /> Approve
            </button>
            <button type="button" className="btn btn-danger" disabled={busy} onClick={reject}>
              <X className="ico" aria-hidden="true" /> Reject
            </button>
          </div>
        </div>
      )}

      {req.status === 'approved' && !!req.can_revert && (
        <div className="row">
          <button type="button" className="btn" disabled={busy} onClick={() => onRevert(req.id)}>
            <Undo2 className="ico" aria-hidden="true" /> Revert
          </button>
        </div>
      )}
    </article>
  );
}
