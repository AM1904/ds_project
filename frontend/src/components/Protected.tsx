import { Navigate, useLocation } from 'react-router-dom';
import { homeFor, useAuth } from '../context/Auth';
import type { Role } from '../lib/types';
import type { ReactNode } from 'react';

export function Protected({ roles, children }: { roles: Role[]; children: ReactNode }) {
  const { user, ready } = useAuth();
  const loc = useLocation();
  if (!ready) return <div className="page"><div className="empty card card-flat" aria-busy="true">Loading…</div></div>;
  if (!user) return <Navigate to="/login" replace state={{ from: loc.pathname + loc.search }} />;
  if (!roles.includes(user.role)) return <Navigate to={homeFor(user)} replace />;
  return <>{children}</>;
}
