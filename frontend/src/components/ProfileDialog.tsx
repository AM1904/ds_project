import { useState, type FormEvent } from 'react';
import { useAuth } from '../context/Auth';
import { useToast } from '../context/Toast';
import { api, ApiError } from '../lib/api';
import { Dialog } from './Dialog';

export function ProfileDialog({ open, onClose }: { open: boolean; onClose: () => void }) {
  const { user, setUser } = useAuth();
  const toast = useToast();
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  if (!user) return null;
  const isStudent = user.role === 'Student';

  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const f = new FormData(e.currentTarget);
    setBusy(true); setError('');
    try {
      const r = await api.updateProfile({
        name: String(f.get('name') ?? ''), phone: String(f.get('phone') ?? ''),
        department: String(f.get('department') ?? user!.department), section: user!.section,
      });
      setUser(r.user);
      toast('Profile saved', 'success');
      onClose();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : 'Could not save profile.');
    } finally { setBusy(false); }
  }

  return (
    <Dialog open={open} onClose={onClose} title="Your profile">
      <form className="stack" onSubmit={submit} noValidate>
        <div className="field"><label htmlFor="pf-email">Email</label>
          <input id="pf-email" className="input" value={user.email} readOnly aria-describedby="pf-email-h" />
          <span id="pf-email-h" className="help">Email can't be changed.</span></div>
        <div className="field"><label htmlFor="pf-name">Full name</label>
          <input id="pf-name" name="name" className="input" defaultValue={user.name} required autoComplete="name" /></div>
        {!isStudent && (
          <div className="field"><label htmlFor="pf-dept">Department</label>
            <input id="pf-dept" name="department" className="input" defaultValue={user.department} /></div>
        )}
        {isStudent && (
          <div className="field"><label htmlFor="pf-sec">Section</label>
            <input id="pf-sec" className="input" value={user.section} readOnly aria-describedby="pf-sec-h" />
            <span id="pf-sec-h" className="help">Your section is set by the admin.</span></div>
        )}
        <div className="field"><label htmlFor="pf-phone">Phone</label>
          <input id="pf-phone" name="phone" className="input" defaultValue={user.phone} type="tel" autoComplete="tel" /></div>
        {error && <p className="alert alert-error" role="alert">{error}</p>}
        <div className="dialog-actions">
          <button type="button" className="btn" onClick={onClose}>Cancel</button>
          <button type="submit" className="btn btn-primary" disabled={busy}>{busy ? 'Saving…' : 'Save changes'}</button>
        </div>
      </form>
    </Dialog>
  );
}
