import { useRef, useState, type FormEvent, type KeyboardEvent } from 'react';
import { ChevronRight, Eye, EyeOff, Loader2 } from 'lucide-react';
import { useAuth } from '../context/Auth';
import { useToast } from '../context/Toast';
import { ApiError } from '../lib/api';
import { Navigate, useLocation } from 'react-router-dom';
import { homeFor } from '../context/Auth';
import { useDocumentTitle } from '../hooks';
import './login.css';

type Mode = 'login' | 'register';
type Errors = Partial<Record<'name' | 'email' | 'password', string>>;

const SECTIONS = ['MCA A', 'MCA B', 'MCA C', 'MCA D'];
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

interface Demo { label: string; role: 'Student' | 'Teacher' | 'Admin'; note: string; email: string; password: string; name?: string; section?: string }
export const DEMOS: Demo[] = [
  { label: 'Student MCA A', role: 'Student', note: 'Student · sees the MCA A week', email: 'student.a@college.edu', password: 'student123', name: 'Student MCA A', section: 'MCA A' },
  { label: 'Student MCA B', role: 'Student', note: 'Student · sees the MCA B week', email: 'student.b@college.edu', password: 'student123', name: 'Student MCA B', section: 'MCA B' },
  { label: 'Dr. Ananya Sharma', role: 'Teacher', note: 'Teacher · Data Structures & Algorithms', email: 'ananya@college.edu', password: 'faculty123' },
  { label: 'Prof. Ravi Kumar', role: 'Teacher', note: 'Teacher · Operating Systems', email: 'ravi.k@college.edu', password: 'faculty123' },
  { label: 'Ms. Priya Nair', role: 'Teacher', note: 'Teacher · Database Management Systems', email: 'priya.nair@college.edu', password: 'faculty123' },
  { label: 'Administrator', role: 'Admin', note: 'Admin · schedules classes, decides requests', email: 'admin@college.edu', password: 'admin123' },
];

function Field({ id, label, value, onChange, error, type = 'text', auto, help }: {
  id: string; label: string; value: string; onChange: (v: string) => void; error?: string; type?: string; auto?: string; help?: string;
}) {
  const [show, setShow] = useState(false);
  const isPw = type === 'password';
  const desc = [error && `${id}-err`, help && `${id}-help`].filter(Boolean).join(' ') || undefined;
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <div className="auth-pw">
        <input id={id} className="input" type={isPw && show ? 'text' : type} autoComplete={auto} value={value}
          onChange={e => onChange(e.target.value)} aria-invalid={!!error} aria-describedby={desc} />
        {isPw && (
          <button type="button" className="auth-eye" aria-label={show ? 'Hide password' : 'Show password'} aria-pressed={show} onClick={() => setShow(s => !s)}>
            {show ? <EyeOff size={18} aria-hidden="true" /> : <Eye size={18} aria-hidden="true" />}
          </button>
        )}
      </div>
      {help && <span id={`${id}-help`} className="help">{help}</span>}
      {error && <span id={`${id}-err`} className="field-error">{error}</span>}
    </div>
  );
}

export default function Login() {
  useDocumentTitle('Sign in');
  const { user, ready, login, register } = useAuth();
  const location = useLocation();
  const toast = useToast();
  const [mode, setMode] = useState<Mode>('login');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'Student' | 'Faculty'>('Student');
  const [section, setSection] = useState(SECTIONS[0]);
  const [department, setDepartment] = useState('');
  const [errors, setErrors] = useState<Errors>({});
  const [formError, setFormError] = useState('');
  const [busy, setBusy] = useState<string | null>(null);
  const formRef = useRef<HTMLFormElement>(null);


  const switchMode = (m: Mode) => { setMode(m); setErrors({}); setFormError(''); };
  const onTabKey = (e: KeyboardEvent) => {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
      const m = mode === 'login' ? 'register' : 'login';
      switchMode(m);
      document.getElementById(`auth-tab-${m}`)?.focus();
    }
  };

  const validate = (): Errors => {
    const e: Errors = {};
    if (mode === 'register' && !name.trim()) e.name = 'Enter your full name.';
    if (!EMAIL_RE.test(email.trim())) e.email = 'Enter a valid email address.';
    if (mode === 'login' ? !password : password.length < 6) e.password = mode === 'login' ? 'Enter your password.' : 'Password must be at least 6 characters.';
    return e;
  };

  const submit = async (ev: FormEvent) => {
    ev.preventDefault();
    setFormError('');
    const e = validate();
    setErrors(e);
    const first = (['name', 'email', 'password'] as const).find(k => e[k]);
    if (first) { formRef.current?.querySelector<HTMLElement>(`#auth-${first}`)?.focus(); return; }
    setBusy('form');
    try {
      if (mode === 'login') await login(email.trim(), password);
      else await register({ name: name.trim(), email: email.trim(), password, role, ...(role === 'Student' ? { section } : { department: department.trim() }) });
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : 'Something went wrong.');
      setBusy(null);
    }
  };

  const demo = async (d: Demo) => {
    setFormError('');
    setBusy(d.email);
    try {
      try {
        await login(d.email, d.password);
      } catch (err) {
        if (!(err instanceof ApiError) || err.status !== 401 || !d.section) throw err;
        await register({ name: d.name!, email: d.email, password: d.password, role: 'Student', section: d.section });
        toast(`Demo account created: ${d.email} / ${d.password}`, 'success');
      }
    } catch (err) {
      setFormError(err instanceof ApiError ? err.message : 'Something went wrong.');
      setBusy(null);
    }
  };

  if (ready && user) {
    const from = (location.state as { from?: string } | null)?.from;
    const home = homeFor(user);
    return <Navigate to={from && from.startsWith(home) ? from : home} replace />;
  }

  const isReg = mode === 'register';
  return (
    <main id="main" className="login">
      <div className="login-card card">
        <div className="login-main">
          <header className="login-head">
            <h1>Campus Timetable</h1>
            <p className="muted">{isReg ? 'Create an account' : 'Sign in to continue'}</p>
          </header>
      <div className="segmented" role="tablist" aria-label="Account access" onKeyDown={onTabKey}>
        {(['login', 'register'] as const).map(m => (
          <button key={m} type="button" role="tab" id={`auth-tab-${m}`} aria-selected={mode === m} aria-controls="auth-panel"
            tabIndex={mode === m ? 0 : -1} onClick={() => switchMode(m)}>
            {m === 'login' ? 'Sign in' : 'Create account'}
          </button>
        ))}
      </div>
      <form ref={formRef} id="auth-panel" role="tabpanel" aria-labelledby={`auth-tab-${mode}`} className="stack" onSubmit={submit} noValidate>
        {isReg && <Field id="auth-name" label="Full name" value={name} onChange={setName} error={errors.name} auto="name" />}
        <Field id="auth-email" label="Email" type="email" value={email} onChange={setEmail} error={errors.email} auto="email" />
        <Field id="auth-password" label="Password" type="password" value={password} onChange={setPassword} error={errors.password}
          auto={isReg ? 'new-password' : 'current-password'} help={isReg ? 'At least 6 characters.' : undefined} />
        {isReg && (
          <>
            <div className="field">
              <label htmlFor="auth-role">I am a</label>
              <select id="auth-role" className="select" value={role} onChange={e => setRole(e.target.value as 'Student' | 'Faculty')}>
                <option value="Student">Student</option>
                <option value="Faculty">Teacher</option>
              </select>
            </div>
            {role === 'Student' ? (
              <div className="field">
                <label htmlFor="auth-section">Section</label>
                <select id="auth-section" className="select" value={section} onChange={e => setSection(e.target.value)}>
                  {SECTIONS.map(s => <option key={s}>{s}</option>)}
                </select>
              </div>
            ) : (
              <div className="field">
                <label htmlFor="auth-dept">Department (optional)</label>
                <input id="auth-dept" className="input" value={department} onChange={e => setDepartment(e.target.value)} autoComplete="organization-title" />
              </div>
            )}
          </>
        )}
        {formError && <p className="alert alert-error" role="alert">{formError}</p>}
        <button type="submit" className="btn btn-primary" disabled={!!busy} aria-busy={busy === 'form'}>
          {busy === 'form' && <Loader2 size={18} className="auth-spin" aria-hidden="true" />}
          {isReg ? 'Create account' : 'Sign in'}
        </button>
      </form>
        </div>
        <aside className="demo" aria-labelledby="demo-title">
          <div className="demo-head">
            <h2 id="demo-title">Demo accounts</h2>
            <p className="muted">Open the app as any role. No password needed.</p>
          </div>
          <ul className="demo-list">
            {DEMOS.map(d => (
              <li key={d.email}>
                <button type="button" className="demo-row" disabled={!!busy} aria-busy={busy === d.email} onClick={() => demo(d)}>
                  <span className="demo-name">{d.label}</span>
                  <span className="demo-note">{d.note}</span>
                  {busy === d.email
                    ? <Loader2 size={16} className="auth-spin" aria-hidden="true" />
                    : <ChevronRight size={16} className="demo-go" aria-hidden="true" />}
                </button>
              </li>
            ))}
          </ul>
        </aside>
      </div>
    </main>
  );
}
