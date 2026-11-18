import { useState } from 'react';
import { Link, NavLink, Outlet } from 'react-router-dom';
import { LogOut } from 'lucide-react';
import { useAuth, homeFor } from '../context/Auth';
import { useBadges } from '../context/Badges';
import { useToast } from '../context/Toast';
import { ProfileDialog } from './ProfileDialog';

export function AppShell() {
  const { user, logout } = useAuth();
  const { pending, newDecisions } = useBadges();
  const toast = useToast();
  const [profileOpen, setProfileOpen] = useState(false);
  if (!user) return null;

  const initials = user.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
  const links: { to: string; label: string; end?: boolean; badge?: number }[] =
    user.role === 'Admin' ? [
      { to: '/admin', label: 'Timetable', end: true },
      { to: '/admin/new', label: 'Schedule a class' },
      { to: '/admin/requests', label: 'Requests', badge: pending },
    ] : user.role === 'Faculty' ? [
      { to: '/faculty', label: 'My timetable', end: true },
      { to: '/faculty/requests', label: 'Requests', badge: newDecisions },
    ] : [{ to: '/student', label: 'My timetable', end: true }];

  return (
    <>
      <a className="skip-link" href="#main">Skip to content</a>
      <header className="shell-header">
        <div className="shell-inner">
          <Link to={homeFor(user)} className="brand">Campus Timetable</Link>
          <nav aria-label="Main" className="shell-nav">
            <ul>
              {links.map(l => (
                <li key={l.to}>
                  <NavLink to={l.to} end={l.end}>
                    {l.label}
                    {!!l.badge && <span className="nav-badge" aria-label={`${l.badge} ${user.role === 'Admin' ? 'pending' : 'new'}`}>{l.badge}</span>}
                  </NavLink>
                </li>
              ))}
            </ul>
          </nav>
          <div className="shell-user">
            <button type="button" className="user-btn" onClick={() => setProfileOpen(true)} aria-label={`Your profile, ${user.name}`}>
              <span className="avatar" aria-hidden="true">{initials}</span>
              <span className="user-text"><strong>{user.name}</strong><span>{user.role}{user.role === 'Student' && user.section ? ` · ${user.section}` : ''}</span></span>
            </button>
            <button type="button" className="btn btn-sm" onClick={async () => { await logout(); toast('Signed out', 'info'); }}>
              <LogOut className="ico" aria-hidden="true" /> Sign out
            </button>
          </div>
        </div>
      </header>
      <main id="main" tabIndex={-1}><Outlet /></main>
      <ProfileDialog open={profileOpen} onClose={() => setProfileOpen(false)} />
    </>
  );
}
