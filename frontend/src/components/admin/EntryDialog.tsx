import { useState } from 'react';
import { Dialog } from '../Dialog';
import { useToast } from '../../context/Toast';
import type { ScheduleEntry } from '../../lib/types';
import { EntryForm, type FormValues } from './EntryForm';
import type { AdminRefs } from './useAdminRefs';

interface Props { entry: ScheduleEntry | null; refs: AdminRefs; onClose: () => void; onSaved: () => void; onRemove?: (e: ScheduleEntry) => void }

export function EntryDialog({ entry, refs, onClose, onSaved, onRemove }: Props) {
  return (
    <Dialog open={!!entry} onClose={onClose} title="Edit class" size="lg">
      {entry && <Body entry={entry} refs={refs} onClose={onClose} onSaved={onSaved} onRemove={onRemove} />}
    </Dialog>
  );
}

function Body({ entry, refs, onClose, onSaved, onRemove }: Omit<Props, 'entry'> & { entry: ScheduleEntry }) {
  const toast = useToast();
  const [v, setV] = useState<FormValues>({
    section: entry.section, date: entry.date, subjectId: String(entry.subject_id),
    teacherEmail: entry.teacher_email, timeslot: entry.timeslot, classroomId: String(entry.classroom_id),
  });
  return (
    <EntryForm
      refs={refs} entry={entry} value={v} onChange={p => setV(s => ({ ...s, ...p }))}
      submitLabel="Save changes" onCancel={onClose}
      leading={onRemove && <button type="button" className="btn btn-danger" onClick={() => onRemove(entry)}>Remove class</button>}
      onSaved={r => {
        toast(r.has_clash ? r.message : 'Class updated.', r.has_clash ? 'error' : 'success');
        onClose();
        onSaved();
      }}
    />
  );
}
